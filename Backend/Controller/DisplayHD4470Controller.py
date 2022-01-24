import threading
import time

import Backend.Controller.lcddriver

class displayController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__lcd = Backend.Controller.lcddriver.lcd()
        self.__lcd.lcd_clear()
        self.running = False
        self.__intervalText=[]
    def clearDisplay(self):
        self.__lcd.lcd_clear()
    def setTextOnLine1(self,message):
        self.__lcd.lcd_display_string(message,1)
    def setTextOnLine2(self,message):
        self.__lcd.lcd_display_string(message,2)
    def setTextOnLine3(self,message):
        self.__lcd.lcd_display_string(message,3)
    def setTextOnLine4(self,message):
        self.__lcd.lcd_display_string(message,4)
    def setSetIntervalText(self,text):
        self.__intervalText = text

    def showWelcom(self):
        self.clearDisplay()
        self.__lcd.lcd_display_string('   Willkommen zum', 1)
        self.__lcd.lcd_display_string('    Bier Brauer', 2)
        self.__lcd.lcd_display_string('    Viel Spass!!!', 4)
    def run(self):
        self.running = True
        self.__startIntervalText()

    def __startIntervalText(self):
        while self.running == True:
            i=0
            self.clearDisplay()
            self.setTextOnLine1(self.__intervalText[i])
            i=i+1
            self.setTextOnLine2(self.__intervalText[i])
            i = i + 1
            self.setTextOnLine3(self.__intervalText[i])
            i = i + 1
            self.setTextOnLine4(self.__intervalText[i])
            time.sleep(4)
            self.clearDisplay()
            i = i + 1
            self.setTextOnLine1(self.__intervalText[i])
            i = i + 1
            self.setTextOnLine2(self.__intervalText[i])
            i = i + 1
            self.setTextOnLine3(self.__intervalText[i])
            i = i + 1
            self.setTextOnLine4(self.__intervalText[i])
            i = i + 1
            time.sleep(4)








