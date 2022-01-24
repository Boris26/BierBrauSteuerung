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
        self.__initGPIOs()
        return self.__GPIO
    def __initGPIOs(self):
        self.__GPIO.setup(22, self.__GPIO.OUT)
        self.__GPIO.output(22, self.__GPIO.HIGH)
        self.__GPIO.setup(26, self.__GPIO.OUT)
        self.__GPIO.output(26, self.__GPIO.HIGH)
        self.__GPIO.setup(19, self.__GPIO.OUT)
        self.__GPIO.output(19, self.__GPIO.HIGH)
        self.__GPIO.setup(13, self.__GPIO.OUT)
        self.__GPIO.output(13, self.__GPIO.HIGH)
        self.__GPIO.setup(6, self.__GPIO.OUT)
        self.__GPIO.output(6, self.__GPIO.HIGH)
        self.__GPIO.setup(5, self.__GPIO.OUT)
        self.__GPIO.output(5, self.__GPIO.HIGH)
        self.__GPIO.setup(11, self.__GPIO.OUT)
        self.__GPIO.output(11, self.__GPIO.HIGH)
        self.__GPIO.setup(9, self.__GPIO.OUT)
        self.__GPIO.output(9, self.__GPIO.HIGH)
        self.__GPIO.setup(10, self.__GPIO.OUT)
        self.__GPIO.output(10, self.__GPIO.HIGH)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

