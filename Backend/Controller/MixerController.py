import RPi.GPIO as GPIO
from time import sleep
class mixerController():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(16,GPIO.OUT)
        GPIO.setup(20,GPIO.OUT)
        GPIO.setup(21,GPIO.OUT)
        GPIO.output(21, GPIO.LOW)
        self.__pwmL = GPIO.PWM(16,90)
        self.__pwmR = GPIO.PWM(20,90)

    def start(self,speed):
        try:
            GPIO.output(21, GPIO.HIGH)
            self.__pwmR.start(int(speed))

            return True
        except ValueError:
            print(ValueError)
            return False

    def stop(self):
        try:
            GPIO.output(21, GPIO.LOW)
            return True
        except:
            return False

    def setSpeedLeft(self,speed):
        self.__pwL.ChangeDutyCycle(speed)

    def setSpeedRight(self,speed):
        self.__pwmR.ChangeDutyCycle(int(speed))
    def setFrq(self,frq):
        self.__pwmR.ChangeFrequency(int(frq))







