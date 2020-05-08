import json
import threading
from datetime import time
import asyncio
import queue
import timers
import time
import chess
import requests
import ast
import conf



class GameControler(threading.Thread):
    def __init__(self, GameId, GameTime, interval=1.000):
        threading.Thread.__init__(self)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever)

        self.players = {}
        self.watchers = set()

        self.board = chess.Board()
        self.q = queue.Queue()

        self.status = 'open'

        self.history = {}
        self.movenr = 0;

        self.drawofer = False

        self.whitedata = {}
        self.blackdata = {}

        self.whitedata = {
            'playerid': '',
            'connectionId': '',
            #'sessionId': ''
        }
        self.blackdata = {
            'playerid': '',
            'connectionId': '',
            #'sessionId': ''
        }

        self.whomoving = 'white'

        #self.running = False
        self.id = GameId
        self.whitetime = GameTime
        self.blacktime = GameTime

        self.gametime = GameTime
        self.whitetime = timers.SecondCounter(self.whitetime, callback=self.endoftime)
        self.blacktime = timers.SecondCounter(self.blacktime, callback=self.endoftime)

    def msg(self, msg):
        self.q.put(msg)

    def sendRandomMsg(self, msg):
        print("Dostalem przekazana wiadomosc, wysylam do wszystkich watcherow")
        self._loop.run_until_complete(self.sendmsg(msg))

    def addPlayers(self, whiteid, whiteconnection, blackid, blackconnection):
        self.whitedata['playerid'] = str(whiteid)
        self.whitedata['connectionId'] = whiteconnection

        self.blackdata['playerid'] = str(blackid)
        self.blackdata['connectionId'] = blackconnection

        if(self.whitedata['connectionId'] in conf.users):
            conf.users[self.whitedata['connectionId']].userInfo['running'] = 'true'
            conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = str(self.id)

        if (self.blackdata['connectionId'] in conf.users):
            conf.users[self.blackdata['connectionId']].userInfo['running'] = 'true'
            conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = str(self.id)

        print("Dodałem graczy do partii")

    def getTime(self):
        url = 'http://szachy.io/gettime/'
        r = requests.get(url)
        data = json.loads(r.content.decode())
        return data['time']

    def sendtoall(self, msg):
        for key in self.watchers:
            conf.users[key].addSendMsg(msg)

    async def sendmsg(self, msg, connectionId='0'):
        if(connectionId != '0'):
            if(connectionId in conf.users):
                conf.users[connectionId].addSendMsg(msg)
        else:
            self.sendtoall(msg)

    def addnewwatcher(self, connectionId):
        self.watchers.add(connectionId)

    def removewatcher(self, connectionId):
        self.watchers.remove(connectionId)

    def updateplayerstate(self, msg):

         #if(msg['playerid'] in usersInfo):
        #    user = usersInfo[msg['playerid']]

        #    if (msg['sessionId'] == user['session_id']):

                if(msg['playerid'] == self.whitedata['playerid']):
                    self.whitedata['sessionId'] = msg['sessionId']

                if(msg['playerid'] == self.blackdata['playerid']):
                    self.blackdata['sessionId'] = msg['sessionId']

    def givefirstgameinfo(self, message):
        msg = message

        #self.updateplayerstate(msg)

        sessionId =  msg['sessionId']

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'gamefirstinfo'
        gameinfo['status'] = self.status
        if (self.whitedata['playerid'] != ''):
            gameinfo['white'] = 'true'
        else:
            gameinfo['white'] = 'false'

        if (self.blackdata['playerid'] != ''):
            gameinfo['black'] = 'true'
        else:
            gameinfo['black'] = 'false'

        gameinfo['timewhite'] = self.whitetime.peek()
        gameinfo['timeblack'] = self.blacktime.peek()
        if(self.status == 'running'):
            gameinfo['running'] = 'true'
        else:
            gameinfo['running'] = 'false'

        #TESTY

        print(self.whitedata)
        print(self.blackdata)


        #KONIEC TESTOW

        if (msg['sessionId'] is not None):
            if (msg['playerid'] == self.whitedata['playerid']):
                if (msg['gameid'] == conf.users[msg['connectionId']].userInfo['runningGameId']):
                    if (conf.users[msg['connectionId']].userInfo['sessionId'] == msg['sessionId']):
                        gameinfo['mycolor'] = 'white'
            if (msg['playerid'] == self.blackdata['playerid']):
                if (msg['gameid'] == conf.users[msg['connectionId']].userInfo['runningGameId']):
                    if (conf.users[msg['connectionId']].userInfo['sessionId'] == msg['sessionId']):
                        gameinfo['mycolor'] = 'black'

        gameinfo['fenposition'] = self.board.fen()
        gameinfo['whomoving'] = self.whomoving

        if(len(self.history)>0):
            gameinfo['history'] = {}
            for self.key in self.history :
                gameinfo['history'][self.key] = self.history[self.key];

        self.addnewwatcher(msg['connectionId'])

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data, message['connectionId']))

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def chat(self, message):
        message['text'] = self.remove_html_tags(message['text'])
        self._loop.run_until_complete(self.sendmsg(message))

    def resign(self, message):
        msg = message

        if(msg['color'] == 'white'):
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return
        else:
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return

        if(self.status!='running'):
            return

        self.blacktime.stopthinking()
        self.whitetime.stopthinking()

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'resign'

        if(msg['color']=='white'):
            gameinfo['result'] = "0-1"
        else:
            gameinfo['result'] = "1-0"

        gameinfo['gameover'] = 'true'

        self.status = 'ended'

        conf.users[self.whitedata['connectionId']].userInfo['running'] = 'false'
        conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = ''

        conf.users[self.blackdata['connectionId']].userInfo['running'] = 'false'
        conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = ''

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data))


    def acceptDraw(self, message):
        msg = message

        if(msg['color'] == 'white'):
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return
        else:
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return

        if(self.status!='running'):
            return

        if(not self.drawofer):
            return

        self.blacktime.stopthinking()
        self.whitetime.stopthinking()

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'accepteddraw'

        gameinfo['gameover'] = 'true'
        gameinfo['result'] = "1/2-1/2"
        self.status = 'ended'

        self.drawofer = False

        conf.users[self.whitedata['connectionId']].userInfo['running'] = 'false'
        conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = ''

        conf.users[self.blackdata['connectionId']].userInfo['running'] = 'false'
        conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = ''

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data))

    def refuseDraw(self, message):
        msg = message

        if (msg['color'] == 'white'):
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return
        else:
            if (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return

        if(self.status!='running'):
            return

        if(not self.drawofer):
            return

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'refuseddraw'

        if(msg['color']=='white'):
            connectionId = self.blackdata['connectionId']
        else:
            connectionId = self.whitedata['connectionId']

        self.drawofer = False

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data, connectionId))

    def offerdraw(self, message):
        msg = message

        if(msg['color'] == 'white'):
            if(msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return
        else:
            if(msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId']):
                return

        if(self.status!='running'):
            return

        if(self.drawofer):
            return

        self.drawofer = True

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'offereddraw'

        if(msg['color']=='white'):
            connectionId = self.blackdata['connectionId']
        else:
            connectionId = self.whitedata['connectionId']

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data, connectionId))

    def registration(self, message):
        msg = message
        if(self.status != 'open'):
            return
        if(conf.users[msg['connectionId']].userInfo['logged'] == 'false'):
            return
            #nie zalogowany
        if(conf.users[msg['connectionId']].userInfo['sessionId'] != msg['sessionId']):
            return
            #zly numer sesji, nie zalogowany?

        if((msg['color'] == 'white')and(self.whitedata['playerid'] != '') or (msg['color'] == 'black')and(self.blackdata['playerid'] != '')):
            return
            #jezeli kolor juz dodany

        if(msg['color'] == 'white'):
            self.whitedata['playerid'] = msg['playerid']
            #self.whitedata['sessionId'] = msg['sessionId']
            self.whitedata['connectionId'] = msg['connectionId']

            conf.users[self.whitedata['connectionId']].userInfo['running'] = 'true'
            conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = str(self.id)

        else:
            self.blackdata['playerid'] = msg['playerid']
            #self.blackdata['sessionId'] = msg['sessionId']
            self.blackdata['connectionId'] = msg['connectionId']

            conf.users[self.blackdata['connectionId']].userInfo['running'] = 'true'
            conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = str(self.id)

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'registration'
        gameinfo['result'] = 'true'
        gameinfo['color'] = msg['color']
        gameinfo['time'] = self.gametime
        gameinfo['sessionId'] = msg['sessionId']

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data))
        self.checkplayers()

    def setWhiteData(self, data):
        self.whitedata['playerid'] = data['playerid']
        self.whitedata['connectionId'] = data['connectionId']

    def setBlackData(self, data):
        self.blackdata['playerid'] = data['playerid']
        self.blackdata['connectionId'] = data['connectionId']

    def checkplayers(self):
        if ((self.whitedata['playerid'] != '') and (self.blackdata['playerid'] != '')):
            self.startgame()

    def endoftime(self):
        self.blacktime.stopthinking()
        self.whitetime.stopthinking()

        self.status = 'ended'

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'endoftime'

        if(float(self.whitetime.peek())<=0):
            gameinfo['color'] = 'white'
        else:
            gameinfo['color'] = 'black'

        if(self.whitedata['connectionId'] in conf.users):
            conf.users[self.whitedata['connectionId']].userInfo['running'] = 'false'
            conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = ''
        if (self.blackdata['connectionId'] in conf.users):
            conf.users[self.blackdata['connectionId']].userInfo['running'] = 'false'
            conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = ''

        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data))

    def startgame(self):
        self.status = 'running'

        #if(self.whitedata['playerid'] in usersInfo):
        #    usersInfo[self.whitedata['playerid']]['running'] = 'true'
        #    usersInfo[self.whitedata['playerid']]['runningGameId'] = self.id
        #if(self.blackdata['playerid'] in usersInfo):
        #    usersInfo[self.blackdata['playerid']]['running'] = 'true'
        #    usersInfo[self.blackdata['playerid']]['runningGameId'] = self.id
        #TUTAJ ZROBIC
        # conf.users[msg['connectionId']].userInfo['sessionId'] RUNNING TRUE

        self.blacktime.start()
        self.whitetime.start()

        self.now = self.getTime()

        gameinfo = {}
        gameinfo['type'] = 'game'
        gameinfo['action'] = 'startthegame'
        gameinfo['gameid'] = str(self.id)
        gameinfo['serverstamp'] = self.now
        json_data = json.dumps(gameinfo)
        self._loop.run_until_complete(self.sendmsg(json_data))

        self.whitetime.startthinking()

        print("Wystartowala partia")

    def move(self, message):
        msg = message
        if(self.status != 'running'):
            return
        if((msg['color'] == 'white') and (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId'])):
            return
        if((msg['color'] == 'black') and (msg['sessionId'] != conf.users[msg['connectionId']].userInfo['sessionId'])):
            return

        self.newmove = {}
        self.newmove['from'] = msg['from']
        self.newmove['to'] = msg['to']
        self.newmove['promotion'] = msg['promotion']

        self.movenr += 1

        self.history[self.movenr] = self.newmove

        m = chess.Move.from_uci(msg['from']+msg['to']+msg['promotion'])
        self.board.push(m)

        self.now = self.getTime()

        self.resDiff = msg['resDiff']
        self.reqDiff = ast.literal_eval(self.now) - ast.literal_eval(msg['clientstamp'])

        self.lag = self.resDiff + self.reqDiff


        if(msg['color']=='white'):

            self.whitetime.stopthinking()

            self.whitetime.addLag(self.lag)

            msg['time']=self.whitetime.peek()
            self.blacktime.startthinking()
            self.whomoving = 'black'
        else:

            self.blacktime.stopthinking()
            self.blacktime.addLag(self.lag)
            msg['time']=self.blacktime.peek()
            self.whitetime.startthinking()
            self.whomoving = 'white'

        if(self.board.is_game_over(claim_draw=True)):
            self.blacktime.stopthinking()
            self.whitetime.stopthinking()
            msg['gameover'] = 'true'
            msg['result'] = self.board.result(claim_draw=True)
            self.status = 'ended'

            conf.users[self.whitedata['connectionId']].userInfo['running'] = 'false'
            conf.users[self.whitedata['connectionId']].userInfo['runningGameId'] = ''

            conf.users[self.blackdata['connectionId']].userInfo['running'] = 'false'
            conf.users[self.blackdata['connectionId']].userInfo['runningGameId'] = ''

        else:
            msg['gameover'] = 'false'

        msg['serverstamp'] = self.getTime()

        json_data = json.dumps(msg)
        self._loop.run_until_complete(self.sendmsg(json_data))

    def run(self):

        while True:

            if not self.q.empty():
                msg = self.q.get()
                #msg = json.loads(message)

                print('GameControler:')
                print(msg)

                action = msg['action']

                if(action=='givefirstgameinfo'):
                    self.givefirstgameinfo(msg)

                if (action=='registration'):
                    self.registration(msg)

                if (action=='move'):
                    self.move(msg)

                if (action=='offerdraw'):
                    self.offerdraw(msg)

                if (action == 'refuseDraw'):
                    self.refuseDraw(msg)

                if (action == 'acceptDraw'):
                    self.acceptDraw(msg)

                if (action == 'resign'):
                    self.resign(msg)

                if (action == 'chat'):
                    self.chat(msg)

                if(action == 'removewatcher'):
                    self.removewatcher(msg['connectionId'])


            time.sleep(0.01)