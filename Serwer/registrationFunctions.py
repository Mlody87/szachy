import hashlib
import os
import mysql.connector as mariadb
import conf

class RegisterUser:

    def remove_html_tags(self, text):
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def register(self, email, login, password, name, surname):

        rlogin = self.remove_html_tags(login)
        rname = self.remove_html_tags(name)
        rsurname = self.remove_html_tags(surname)
        rpassword = password
        remail = email

        info = {}
        info['login'] = ''
        info['email'] = ''
        info['name'] = ''
        info['surname'] = ''
        info['type'] = 'userregistration'

        if((rlogin=='')or(rpassword=='')or(remail=='')or(rname=='')or(rsurname=='')):
            return


        dbconn = mariadb.connect(user=conf.dbconf['user'], password=conf.dbconf['password'], database=conf.dbconf['db'])
        cursor = dbconn.cursor(buffered=True)

        cursor.execute("SELECT * FROM users WHERE login = %s or email = %s", (rlogin, remail))

        if(cursor.rowcount>0):
            info['result'] = 'false'

            myresult = cursor.fetchall()

            for row in myresult:
                print(row)
                if(row[1]==rlogin):
                    info['login'] = 'Podany login już istnieje'
                if(row[3]==remail):
                    info['email'] = 'Podany e-mail już istnieje'

        else:

            rsalt = os.urandom(10).hex()

            hash = hashlib.sha512()
            hash.update(('%s%s' % (rsalt, rpassword)).encode('utf-8'))
            rpassword = hash.hexdigest()

            query = """INSERT INTO users (login, name, surname, pass, email, salt) 
                                        VALUES (%s, %s, %s, %s, %s, %s) """

            recordTuple = (rlogin, rname, rsurname, rpassword, remail, rsalt)
            cursor.execute(query, recordTuple)

            dbconn.commit()

            info['result'] = 'true'

        dbconn.close()
        print(info)
        return info