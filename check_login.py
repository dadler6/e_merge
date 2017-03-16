import sqlite3
import sys

# Command python login.py username password

class Login:

    # Initialize class and store information
    def __init__(self, username, password):
        self.conn = sqlite3.connect('emergency.db')
        self.c = self.conn.cursor()
        self.username = str(username);
        self.password = str(password);

    # Query data
    def queryData(self):
            self.c.execute("SELECT * FROM LOGIN;")
            fetchall = self.c.fetchall()
            self.usernames_all = [i[0] for i in  fetchall]
            self.passwords_all = [i[1] for i in  fetchall]

    # Check user name
    # Return true if found
    # return false else
    def checkUsername(self):
        try:
            for i in range(len(self.usernames_all)):
                if self.username == self.usernames_all[i]:
                    return i
            else:
                return False
        except:
            return False


    def checkPassword(self, i):
        try:
            if self.password == self.passwords_all[i]:
                return True
            else:
                return False
        except:
            return False


def main():
    try:
        login = Login(sys.argv[1],sys.argv[2])
        login.queryData()
        i = login.checkUsername()
        if login.checkPassword(i):
            return True
    except:
        return False

main()

