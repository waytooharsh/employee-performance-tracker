import threading
import time
import connectdb

class activeUser:
    privilege = None
    uid = None
    def __init__(self,uid, privilege):
        self.privilege = privilege
        self.uid = uid
    def getuser(self):
        return self.uid

userList = []

user_db = connectdb.connect()
query = user_db.cursor(buffered=True)

activeStatus = 0

def startTimer(user):
    while(True):
        if activeStatus==0:
            break
        time.sleep(60)
        query.execute("UPDATE perfdata SET uphrs=IF(upmins<60,uphrs+0, uphrs+1) WHERE uid = %s", (user,))
        query.execute("UPDATE perfdata SET upmins=IF(upmins<60, upmins+1,1) WHERE uid = %s", (user,))
        user_db.commit()

counterThread = threading.Thread(target=startTimer, args=userList)

def startSession(userObj):
    user = userObj.getuser()
    userList.append(user)
    counterThread.start()
