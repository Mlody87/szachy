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
from conf import connections
from loginFunctions import LoginUser
from registrationFunctions import RegisterUser
import conf
import mysql.connector as mariadb


class userThread(threading.Thread):

    def __init__(self, connId):
        threading.Thread.__init__(self)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever)

        self.userInfo = {'logged':'false', 'sessionId':'0', 'userid': '-1'}


        self.stopThread = False

        self.connectionId = connId

        self.receiveMsg = queue.Queue()
        self.sendMsg = queue.Queue()

        self.nextPing = 0;

    def stopThread(self):
        self.stopThread = True

    def setConnectionId(self, connId):
        self.connectionId = connId

    def addReceiveMsg(self, msg):
        self.receiveMsg.put(msg)

    def addSendMsg(self, msg):
        self.sendMsg.put(msg)

    def getTime(self):
        url = 'http://szachy.io/gettime/'
        r = requests.get(url)
        data = json.loads(r.content.decode())
        return data['time']

    def sendPing(self):
        now = time.time()
        if(now >= self.nextPing):
            msg = {}
            msg['type'] = 'ping'
            json_data = json.dumps(msg)
            self.addSendMsg(json_data)
            self.nextPing = time.time() + (30)

    async def sendMessage(self, msg):
        try:
            connections[self.connectionId].write_message(msg)
        except:
            self.stopThread = True
            pass

    def userlogin(self, msg):
        login = LoginUser()
        result = login.login(msg['email'], msg['password'])

        if(result['result']=='true'):
            self.userInfo['logged'] = 'true'
            self.userInfo['userid'] = result['userid']
            self.userInfo['login'] = result['login']
            self.userInfo['sessionId'] = result['sessionId']

            dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
            cursor = dbconn.cursor(dictionary=True, buffered=True)
            cursor.execute("UPDATE sessions SET sessionId = %s, userid = %s WHERE connectionId = %s", (self.userInfo['sessionId'], self.userInfo['userid'], msg['connectionId']))
            dbconn.commit()

            dbconn.close()

        json_data = json.dumps(result)
        self.addSendMsg(json_data)

    def delDbConnection(self):
        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)
        cursor.execute("DELETE FROM sessions WHERE connectionId = %s", (self.connectionId,))
        dbconn.commit()
        dbconn.close()


    def userregistration(self, msg):
        register = RegisterUser()
        result = register.register(msg['email'], msg['login'], msg['password'], msg['name'], msg['surname'])
        json_data = json.dumps(result)
        self.addSendMsg(json_data)

    def run(self):
        self.nextPing = time.time()+(30)
        while True:

            #sending message
            if not self.sendMsg.empty():
                if(self.connectionId in connections):
                    sendM = self.sendMsg.get()
                    self._loop.run_until_complete(self.sendMessage(sendM))

            #check received message
            if not self.receiveMsg.empty():
                message = self.receiveMsg.get()

                type = message['type']

                if(type=='userlogin'):
                    self.userlogin(message)

                if(type=='userregistration'):
                    self.userregistration(message)

                if(type=='gameslobby'):
                    conf.gamesLobbyControler.msg(message)

                if(type=='game'):
                    print("Serwer dostał:",message)
                    if(message['gameid'] in conf.games):
                        conf.games[message['gameid']].msg(message)
                    #dorobic zakonczone i historyczne gry

                if (type == 'tournamentslobby'):
                    conf.tournamentsLobbyControler.msg(message)


            self.sendPing()
            if(self.stopThread):
                self.delDbConnection()
                break
            time.sleep(0.01)