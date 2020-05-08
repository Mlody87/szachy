import json
import uuid
import tornado
import conf
from userThread import userThread
import mysql.connector as mariadb


class UserConnection(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(UserConnection, self).__init__(application, request, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self, connId='0'):
        print('New connection')

        message = {}
        message['type'] = 'connected'

        if(connId == '0'):
            self.connectionId = str(uuid.uuid4())
            message['connType'] = 'new'
            self.dbSetConnectionId(self.connectionId)
            conf.users[self.connectionId] = userThread(self.connectionId)
            conf.users[self.connectionId].start()
        else:
            if (connId in conf.connections):
                self.connectionId = connId
                message['connType'] = 'existing'
            else:
                self.connectionId = str(uuid.uuid4())
                message['connType'] = 'new session'

                self.dbSetConnectionId(self.connectionId, connId)

                if(self.connectionId in conf.users):
                    conf.users[self.connectionId].setConnectionId(self.connectionId)
                else:
                    conf.users[self.connectionId] = userThread(self.connectionId)
                    conf.users[self.connectionId].start()


        conf.connections[self.connectionId] = self
        print(conf.connections)

        message['connectionId'] = self.connectionId
        json_data = json.dumps(message)
        self.write_message(json_data)

    def on_message(self, message):
        msg = json.loads(message)
        if(msg['connectionId'] in conf.users):
            conf.users[msg['connectionId']].addReceiveMsg(msg)

    def dbSetConnectionId(self, newConnid, oldConnid='0'):
        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(dictionary=True, buffered=True)

        if(oldConnid == '0'):
            oldConnid = newConnid

        cursor.execute("SELECT * FROM sessions WHERE connectionId = %s", (oldConnid,))

        if (cursor.rowcount == 0):

            query = """INSERT INTO sessions (connectionId) VALUES (%s) """
            recordTuple = (newConnid,)
            cursor.execute(query, recordTuple)
            dbconn.commit()

        else:
            cursor.execute("UPDATE sessions SET connectionId = %s, sessionId = null, userid = null WHERE connectionId = %s", (newConnid,oldConnid))
            dbconn.commit()

        dbconn.close()



    def on_close(self):
        print('Connection closed...')