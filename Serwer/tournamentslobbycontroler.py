import json
import queue
import threading
import time
import mysql.connector as mariadb
from gamecontroler import GameControler
from conf import games
import conf

class TournamentsLobbyControler(threading.Thread):
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

        response['type'] = 'tournamentslobby'
        response['action'] = 'firstinfo'
        response['logged'] = conf.users[msg['connectionId']].userInfo['logged']

        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True,buffered=True)

        cursor.execute("SELECT * FROM tournaments WHERE status <> 'end'")

        if (cursor.rowcount == 0):
            response['result'] = 'false'

        else:

            response['result'] = 'true'

            myresult = cursor.fetchall()

            tournaments = {}
            i=0

            for row in myresult:
                tour = {}
                tour['id'] = row['id']
                tour['time'] = row['time']
                tour['rounds'] = row['rounds']
                tour['status'] = row['status']
                tour['price'] = row['price']
                tour['roundsplayed'] = row['roundsplayed']
                tour['date'] = row['date'].strftime("%m/%d/%Y, %H:%M:%S")

                dbconn2 = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
                cursor2 = dbconn2.cursor(buffered=True)
                cursor2.execute("SELECT * FROM tournamentsregistrations WHERE tournamentid = %s", (row['id'],))

                tour['players'] = cursor2.rowcount
                dbconn2.close()

                if (msg['sessionId'] == conf.users[msg['connectionId']].userInfo['sessionId']):

                    dbconn3 = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
                    cursor3 = dbconn3.cursor(buffered=True)
                    cursor3.execute("SELECT * FROM tournamentsregistrations WHERE tournamentid = %s and playerid = %s", (row[0],msg['userid'],))


                    if(cursor3.rowcount>0):
                        tour['registered'] = 'true'
                    else:
                        tour['registered'] = 'false'

                    dbconn3.close()
                else:
                    tour['registered'] = 'false'


                tournaments[i] = tour
                i +=1

            dbconn2.close()


        response['tournaments'] = tournaments

        json_data = json.dumps(response)
        conf.users[msg['connectionId']].addSendMsg(json_data)

    def msg(self, msg):
        self.q.put(msg)


    #ZAMIENIC NA REJESTRACJE
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

                #zamienic na rejestracje
                if(msg['action'] == 'creategame'):
                    self.creategame(msg)

                if(msg['action'] == 'removewatcher'):
                    self.removewatcher(msg['connectionId'])

            time.sleep(0.01)
