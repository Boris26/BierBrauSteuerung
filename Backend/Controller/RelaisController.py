from time import sleep
from Backend.Logging.Logger import logging

class RelaisController():
    def __init__(self,GPIO,config):
        self.__GPIO = GPIO
        self.__RELAIS_1_GPIO = int(config.get('GPIOPin'))
        self.__toggleTime = int(config.get('GPIOPin'))
        self.__GPIO.setup(self.__RELAIS_1_GPIO, self.__GPIO.OUT)
        self.__GPIO.output(self.__RELAIS_1_GPIO, self.__GPIO.HIGH)
        self.log = logging()
    def turnon(self):
        self.__GPIO.output(self.__RELAIS_1_GPIO, self.__GPIO.LOW)

    def turnoff(self):
        self.__GPIO.output(self.__RELAIS_1_GPIO, self.__GPIO.HIGH)





