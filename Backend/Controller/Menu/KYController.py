from abc import ABC, abstractmethod
import time
class KYController(ABC):
    def __init__(self,menuController,gpio):
        menuController.update(self,5)
        self.__gpio = gpio
        self.__PIN_CLK = 16
        self.__PIN_DT = 15
        self.__BUTTON_PIN = 14
        self.__gpio.setup(self.__PIN_CLK, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.__gpio.setup(self.__PIN_DT, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.__gpio.setup(self.__BUTTON_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.__Counter = 0
        self.__Richtung = True
        self.__PIN_CLK_LETZTER = 0
        self.__PIN_CLK_AKTUELL = 0
        self.__delayTime = 0.01
        self.__gpio.add_event_detect(self.__PIN_CLK, self.__gpio.BOTH, callback= self.ausgabeFunktion, bouncetime=50)
        self.__gpio.add_event_detect(self.__BUTTON_PIN, self.__gpio.FALLING, callback=self.__click, bouncetime=50)

    def ausgabeFunktion(self,null):
            counter=0
            self.__PIN_CLK_AKTUELL = self.__gpio.input(self.__PIN_CLK)
            if self.__PIN_CLK_AKTUELL != self.__PIN_CLK_LETZTER:
                if self.__gpio.input(self.__PIN_DT) != self.__PIN_CLK_AKTUELL:
                    counter += 1
                else:
                    counter = counter - 1
            self.__updateBase(counter)

        # Initiales Auslesen des Pin_CLK
            self.__PIN_CLK_LETZTER = self.__gpio.input(self.__PIN_CLK)

    def __click(self):
        {
        }
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def clickUpdate(self):
        pass
    def __updateBase(self, encoderPosition):
        self.__menu.update(encoderPosition)
