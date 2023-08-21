import time, threading
from Backend.Logging.Logger import logging
class DS18B20Controller():
    def __init__(self,config):
        self.__sensorId = config.get('SensorID')
        self.__readingInterval = int(config.get('ReadingInterval'))
        self.__oldMeasuredTemperature = 0
        self.__measuredTemperature =0
        self.__receivers = set()
        self.__isRunning = True
        self.log = logging()
        self.thread = threading.Thread(target=self.__running)
        self.__startThread()

    def __startThread(self):
            try:
                self.thread.start()
                #self.log.writeLog('Sensor Thread wurde gestartet')
                self.thread.daemon = False
                print("run")
            except Exception as e:
                pass
                #self.log.writeLog(str(e))

    def add(self,obj):
        self.__receivers.add(obj)

    def __running(self):
        while self.__isRunning:
            try:
                self.__sensor = open(self.__sensorId, "r")
                self.__readTemparature()
            except  Exception as e:
                print(e)
            time.sleep(self.__readingInterval)


    def __readTemparature(self):
        self.__contents = self.__sensor.readlines()
        index = self.__contents[1].find('t=')
        if index != -1:
            self.__measuredTemperature = self.__formatTemperature(self.__contents[1][index + 2:])
            self.__update()


    def __formatTemperature(self,temperature):
        return round(int(temperature) / 1000)

    def __update(self):
        self.measuredTemperature = self.__measuredTemperature
        for item in self.__receivers:
            item.update(self.__measuredTemperature)

    @property
    def Temperature(self):
        return self.__measuredTemperature

    @property
    def switchOnOff(self,switchState):
        self.__isRunning = switchState

















