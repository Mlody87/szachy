import hashlib
import uuid
import mysql.connector as mariadb
import conf

class LoginUser:

    def remove_html_tags(self, text):
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def login(self, email, password):

        remail = self.remove_html_tags(email)
        rpassword = password

        if((remail=='')or(rpassword=='')):
            return

        info = {}
        info['type'] = 'userlogin'

        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(buffered=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (remail,))

        if(cursor.rowcount==0):
            info['result'] = 'false'

        else:

            myresult = cursor.fetchall()

            for row in myresult:

                rsalt = row[4]
                hash = hashlib.sha512()
                hash.update(('%s%s' % (rsalt, rpassword)).encode('utf-8'))
                rpassword = hash.hexdigest()

                if(rpassword != row[2]):
                    info['result'] = 'false'
                else:
                    info['result'] = 'true'
                    info['userid'] = row[0]
                    info['login'] = row[1]
                    info['sessionId'] = str(uuid.uuid4())
                    #tutaj dac wszystkie dane jakie beda o userze

        dbconn.close()
        print(info)
        return info