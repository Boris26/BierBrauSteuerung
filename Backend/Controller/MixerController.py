import threading
from Backend.Enums.HeatingStates import HeatingStates
from time import sleep


class mixerController() :
    def __init__(self, GPIO) :
        self.__gpio=GPIO
        self.__gpio.setup(16, GPIO.OUT)
        self.__gpio.setup(20, GPIO.OUT)
        self.__gpio.setup(21, GPIO.OUT)
        self.__gpio.output(21, GPIO.LOW)
        self.__pwmL=self.__gpio.PWM(16, 90)
        self.__pwmR=self.__gpio.PWM(20, 90)
        self.__isRunning=False
        self.interval_thread=None
        self.interval_running=False
        self.__rotationsPerMinute=20
        self.__runningTime=""
        self.__breakTime=""
        self.__isTurnOn=False
        self.__isIntervalTurnOn=False
        self.__isHeatingAndStirringTurnOn=False

    def start(self, intervalValues) :
        (self.__isTurnOn,
         self.__rotationsPerMinute,
         self.__runningTime,
         self.__breakTime,
         self.__isIntervalTurnOn,
         self.__isHeatingAndStirringTurnOn)= \
            (intervalValues["isTurnOn"],
             intervalValues["rotationsPerMinute"],
             intervalValues["runningTime"],
             intervalValues["breakTime"],
             intervalValues["isIntervalTurnOn"],
             intervalValues["isHeatingAndStirringTurnOn"]
             )
        if self.__isTurnOn:
            if self.__isIntervalTurnOn :
                self.__startInterval()
            else :
                self.stopInterval()
                self.__run()
        else :
            if self.interval_running :
                self.stopInterval()
            if self.__isRunning :
                self.stop()

    def toggleHeatingAndStirringTurnOn(self,Heating) :
        if self.__isHeatingAndStirringTurnOn == True :
            if Heating==True :
                if self.interval_running or self.__isIntervalTurnOn:
                    self.stopInterval()
                    self.__run()
                else :
                    self.__run()
            else :
                if self.interval_running or self.__isIntervalTurnOn:
                    self.stopInterval()
                if self.__isRunning :
                    self.stop()

    def __run(self) :
        try :
            self.__gpio.output(21, self.__gpio.HIGH)
            self.__pwmR.start(int(self.__rotationsPerMinute))
            self.__isRunning=True

            return True
        except ValueError :
            print(ValueError)
            return False

    def __startInterval(self) :
        if not self.interval_running :
            self.interval_running=True
            self.interval_thread=threading.Thread(target = self._interval_thread_func,
                                                  args = ())
            self.interval_thread.start()

    def _interval_thread_func(self) :
        while self.interval_running :
            self.__run()
            sleep(int(self.__runningTime))
            self.stop()
            sleep(int(self.__breakTime))

    def stopInterval(self) :
        self.interval_running=False
        if self.interval_thread :
            self.interval_thread.join()
            self.interval_thread=None

    def stop(self) :
        try :
            self.__gpio.output(21, self.__gpio.LOW)
            self.__isRunning=False
            return True
        except :
            return False

    def setSpeedLeft(self, speed) :
        self.__pwL.ChangeDutyCycle(speed)

    def setSpeedRight(self, speed) :
        self.__pwmR.ChangeDutyCycle(int(speed))

    def setFrq(self, frq) :
        self.__pwmR.ChangeFrequency(int(frq))
