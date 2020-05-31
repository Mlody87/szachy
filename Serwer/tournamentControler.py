import json
import queue
import threading
import time
import mysql.connector as mariadb
from gamecontroler import GameControler
import conf
from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player
import copy
from swiss import SwissEngine
from player import Player


class tournamentControler(threading.Thread):

    def getColor(self):
        return Colour.white

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.q = queue.Queue()
        self.tourInfo = {}
        self.id = id
        self.input_players = list()
        self.players = {}
        self.rounds = {}
        self.gamesId = set()

        self.engine = None

        self.create(self.id)

    def create(self, id):
        self.setInfo(id)
        self.setPlayers(id)

    def setInfo(self, id):
        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT * FROM tournaments WHERE id = %s", (id,))

        if (cursor.rowcount == 0):
            return False

        else:

            myresult = cursor.fetchall()

            for row in myresult:
                self.tourInfo['id'] = row['id']
                self.tourInfo['time'] = int(row['time'])
                self.tourInfo['rounds'] = int(row['rounds'])
                self.tourInfo['round'] = 0
                self.tourInfo['status'] = row['status']
                self.tourInfo['price'] = row['price']
                self.tourInfo['system'] = row['system']
                self.tourInfo['descrition'] = row['description']
                self.tourInfo['organizer'] = row['organizer']
                self.tourInfo['roundsplayed'] = int(row['roundsplayed'])
                self.tourInfo['standing'] = row['standing']
                self.tourInfo['date'] = row['date']

            return True

        dbconn.close()

    def setPlayers(self, id):
        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT * FROM tournamentsregistrations WHERE tournamentid = %s", (id,))

        if (cursor.rowcount == 0):
            return False

        else:

            myresult = cursor.fetchall()

            usersId = []

            for row in myresult:
                usersId.append(row['playerid'])

        print("Zarejestrowanych graczy: ",cursor.rowcount)
        dbconn.close()

        self.setPlayersInfo(usersId)

    def setPlayersInfo(self, usersId):
        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)

        dictId = tuple(usersId)
        sql = "SELECT * FROM users WHERE id IN {}".format(dictId)

        cursor.execute(sql)

        if (cursor.rowcount == 0):
            return False

        else:

            myresult = cursor.fetchall()

            for row in myresult:
                player = {}
                player['playerid'] = row['id']
                player['name'] = row['login']
                player['rating'] = row['rank']
                player['score'] = 0
                player['opponents'] = ()
                player['colour_hist'] = ()

                self.players[row['id']] = player

        dbconn.close()

    def assignPairingNo(self):
        i = 0
        for k in self.players:
            i += 1
            self.players[k]['pairing_no'] = i

    def prepareInputPlayers(self):
        self.input_players = list()
        for k in self.players:
            player = Player(name=self.players[k]['name'],
                            rating=self.players[k]['rating'],
                            pairing_no=self.players[k]['pairing_no'],
                            score=self.players[k]['score'],
                            opponents=self.players[k]['opponents'],
                            colour_hist=self.players[k]['colour_hist']
                            )
            self.input_players.append(player)

        print("INPUT PLAYERS")
        print(self.input_players)

    def getPlayerKey(self, pairing_no):
        # player key = player id
        for k in self.players:
            if pairing_no == self.players[k]['pairing_no']:
                return k

    def updatePlayers(self, round):
        for row in round:
            key = self.getPlayerKey(row.pairing_no)

            self.players[key]['opponents'] = row.opponents
            self.players[key]['colour_hist'] = row.colour_hist
            self.players[key]['score'] = row.score

    def notAdded(self, pair, pairs):
        change = (pair[1], pair[0])
        if change in pairs:
            return False
        else:
            return True

    def getPairs(self, round):
        # player key = player id

        pairs = set()
        for row in round:

            if (row.opponents[-1] != 0):
                myId = self.getPlayerKey(row.pairing_no)
                mycolor = row.colour_hist[-1]
                opponentId = self.getPlayerKey(row.opponents[-1])
                if (mycolor > 0):
                    pair = (myId, opponentId)
                else:
                    pair = (opponentId, myId)
                # check if already pair added opposite way
                if (self.notAdded(pair, pairs)):
                    pairs.add(pair)

        return pairs

    def getConnId(self, userid):

        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT connectionId FROM sessions WHERE userid = %s", (userid,))

        id = '-1'
        if (cursor.rowcount > 0):
            myresult = cursor.fetchall()

            for row in myresult:
                id = row['connectionId']

        dbconn.close()
        return id

    def createGames(self, round):
        pairs = self.getPairs(round)
        print(pairs)
        self.gamesId = set()
        roundInfo = {}

        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(buffered=True)
        i=0
        for pair in pairs:
            pairInfo = {}
            fen = ''
            p1 = str(pair[0])
            p2 = str(pair[1])
            cursor.execute(
                "INSERT INTO games (fen, time, tournamentid, round, whiteid, blackid, date) VALUES (%s,%s,%s,%s,%s,%s,CURDATE())",
                (fen, self.tourInfo['time'], self.tourInfo['id'], self.tourInfo['round'], p1, p2))
            dbconn.commit()

            gameid = cursor.lastrowid
            self.gamesId.add(gameid)

            conf.games[str(gameid)] = GameControler(gameid, self.tourInfo['time'])

            whiteconnection = self.getConnId(pair[0])
            blackconnection = self.getConnId(pair[1])


            conf.games[str(gameid)].addPlayers(pair[0], whiteconnection, pair[1], blackconnection)
            conf.games[str(gameid)].start()

            pairInfo['whiteid'] = pair[0]
            pairInfo['blackid'] = pair[1]
            pairInfo['gameid'] = str(gameid)
            roundInfo[i] = pairInfo
            i += 1

            info = {}
            info['type'] = 'notification'
            info['action'] = 'gamestart'
            info['value'] = gameid
            json_data = json.dumps(info)

            if (whiteconnection in conf.users):
                conf.users[whiteconnection].addSendMsg(info)
            if (blackconnection in conf.users):
                conf.users[blackconnection].addSendMsg(info)


        dbconn.close()
        return roundInfo

    def sendPreparation(self):

        round = self.rounds[self.tourInfo['round']]

        for i in round:
            msg = {}
            msg['type'] = 'game'
            msg['action'] = 'closestart'
            msg['gameid'] = round[i]['gameid']
            json_data = json.dumps(msg)

            if(round[i]['gameid'] in conf.games):
                conf.games[round[i]['gameid']].sendRandomMsg(json_data)

    def sendRoundStart(self):
        round = self.rounds[self.tourInfo['round']]

        for i in round:
            if (round[i]['gameid'] in conf.games):
                conf.games[round[i]['gameid']].startgame()

    def waitForGamesEnd(self):
        tmpGames = copy.deepcopy(self.gamesId)
        removeId = set()

        while True:
            removeId.clear()
            for id in tmpGames:
                if(str(id) in conf.games):
                    if(conf.games[str(id)].status == 'ended'):
                        removeId.add(id)

            for remove in removeId:
                tmpGames.remove(remove)

            if (len(tmpGames) == 0):
                return False

            time.sleep(5)

    def updateScore(self):
        for id in self.gamesId:
            id = str(id)
            if(id in conf.games):
                self.players[int(conf.games[id].whitedata['playerid'])]['score'] += conf.games[id].whitedata['result']
                self.players[int(conf.games[id].blackdata['playerid'])]['score'] += conf.games[id].blackdata['result']

    def run(self):

        # zmien status turnieju

        self.assignPairingNo()

        self.tourInfo['round'] += 1

        while self.tourInfo['round'] <= self.tourInfo['rounds']:

            print("Rusza runda: ",self.tourInfo['round'])

            self.prepareInputPlayers()
            round = SwissEngine(self.tourInfo['round'], self.input_players)
            print(round)

            self.updatePlayers(round)

            roundInfo = self.createGames(round)
            self.rounds[self.tourInfo['round']] = roundInfo

            pi = json.dumps(self.players)
            ri = json.dumps(roundInfo)

            dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'],
                                     database=conf.dbconf['db'])
            cursor = dbconn.cursor(buffered=True)

            cursor.execute(
                "INSERT INTO rounds (tournamentid, roundnr, details, tables) VALUES (%s,%s,%s,%s)",
                (self.tourInfo['id'], self.tourInfo['round'], pi, ri))
            dbconn.commit()
            dbconn.close()

            time.sleep(5)

            self.sendPreparation()

            time.sleep(10)


            self.sendRoundStart()


            time.sleep(8)
            self.waitForGamesEnd()

            print("Skonczyly sie!")

            self.updateScore()

            self.tourInfo['round'] += 1


        #posortuj wyniki i zapisz
        #wyslij wyniki turnieju