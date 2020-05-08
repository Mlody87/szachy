import json
import queue
import threading
import time
import mysql.connector as mariadb
from gamecontroler import GameControler
from conf import games
import conf

class GamesLobbyControler(threading.Thread):
    watchers = set()

    def __init__(self):
        threading.Thread.__init__(self)

        self.q = queue.Queue()

    def addnewwatcher(self, connectionId):
        self.watchers.add(connectionId)

    def removewatcher(self, connectionId):
        self.watchers.remove(connectionId)

    def sendtoall(self, msg):
        for key in self.watchers:
            conf.users[key].addSendMsg(msg)

    def sendfirstinfo(self, msg):

        self.addnewwatcher(msg['connectionId'])

        info = {}
        response = {}

        response['type'] = 'gameslobby'
        response['action'] = 'firstinfo'

        for key in games:
            if(games[key].status == 'open'):
                game = {}
                game['id'] = games[key].id
                game['status'] = games[key].status
                game['time'] = games[key].gametime
                info[key] = game

        response['games'] = info

        json_data = json.dumps(response)
        conf.users[msg['connectionId']].addSendMsg(json_data)

    def msg(self, msg):
        self.q.put(msg)

    def creategame(self, msg):
        rtime = msg['time']
        fen = ''

        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(buffered=True)

        cursor.execute("INSERT INTO games (fen, time) VALUES (%s,%s)", (fen, rtime))

        dbconn.commit()

        gameid = cursor.lastrowid

        info = {}

        info['type'] = 'gameslobby'
        info['action'] = 'newgame'
        info['time'] = msg['time']
        info['gameid'] = gameid

        games[str(gameid)] = GameControler(gameid, int(msg['time']))
        games[str(gameid)].start()

        json_data = json.dumps(info)
        self.sendtoall(json_data)

    def run(self):

        while True:

            if not self.q.empty():
                msg = self.q.get()

                if(msg['action'] == 'firstinfo'):
                    self.sendfirstinfo(msg)

                if(msg['action'] == 'creategame'):
                    self.creategame(msg)

                if(msg['action'] == 'removewatcher'):
                    self.removewatcher(msg['connectionId'])

            time.sleep(0.01)
