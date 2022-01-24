import RPi.GPIO as GPIO
class initGPIOs():

    def __init__(self,piConfig):
        self.__piConfig = piConfig
    def initGPIOsetup(self):
        self.__GPIO = GPIO
        if self.__piConfig.get('GPIOMode') == 'BCM':
            self.__GPIO.setmode(GPIO.BCM)
        if self.__piConfig.get('GPIOMode') == 'BOARD':
            self.__GPIO.setmode(GPIO.BOARD)
        if self.__piConfig.get('GPIOwarnings') == 'false':
            self.__GPIO.setwarnings(False)
        if self.__piConfig.get('GPIOwarnings') == 'true':
            self.__GPIO.setwarnings(True)
        return self.__GPIO



