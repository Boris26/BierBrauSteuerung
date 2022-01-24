from datetime import datetime

class logging():

    def writeLog(self,text):
        log = open('log.txt', 'a')
        log.write(str(datetime.now()) +" "+ text+"\n")
        log.close()
