import threading


class WaterFillingController():
    def __init__(self,GPIO,mainController):
        self.mainController=mainController
        self.__openClose = False
        self.__liters = 0
        self.__waterFlow =0
        self.__count = 0
        self.__GPIO = GPIO
        self.__FLOW_SENSOR_GPIO=24
        self.__WATER_VALVE=26
        self.__GPIO.setup(self.__FLOW_SENSOR_GPIO, self.__GPIO.IN, pull_up_down = self.__GPIO.PUD_UP)
        self.__GPIO.setup(self.__WATER_VALVE,self.__GPIO.OUT)
        self.__status={'liters':"", 'openClose':""}
        self.__thread=threading.Thread(target = self.__running)
        self.__isRunning = False
        self.__setCounter()

    @property
    def Liters(self) :
        return self.__liters

    @Liters.setter
    def Liters(self, value):
        self.__liters=value

    @property
    def WaterFlow(self):
        return self.__waterFlow

    def __setCounter(self):
        self.__count = self.__liters*400
    def __decreasCount(self,channel):
        self.__count = self.__count+1

    def start(self):
        self.__thread.start()

    def stop(self):
        self.__isRunning = False
    def __update(self):
        self.mainController.WaterStatus = {'liters' :self.__waterFlow, 'openClose' :self.__openClose}
    def __running(self):
        self.__GPIO.add_event_detect(self.__FLOW_SENSOR_GPIO, self.__GPIO.FALLING, callback = self.__decreasCount)
        self.__GPIO.output(self.__WATER_VALVE, self.__GPIO.HIGH)
        self.__openClose = True
        while self.__waterFlow <= self.__liters:
            self.__waterFlow = round(self.__count/420,4)
            self.__update()
        self.__GPIO.output(self.__WATER_VALVE, self.__GPIO.LOW)
        self.__openClose = False
        self.__GPIO.remove_event_detect(self.__FLOW_SENSOR_GPIO)
        self.__update()
    def fillManuelStart(self):
        self.__GPIO.output(self.__WATER_VALVE, self.__GPIO.HIGH)
    def fillManuelStop(self):
        self.__GPIO.output(self.__WATER_VALVE, self.__GPIO.LOW)













