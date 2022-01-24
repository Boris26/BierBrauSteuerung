import datetime
import json
import threading
import time

import board
#import busio
#import digitalio

from adafruit_bme280 import basic as adafruit_bme280
class BMP280PressureController(threading.Thread):
    def __init__(self):
        self.__numberOfMeasurements =1
        threading.Thread.__init__(self)
        self.__isRunning = False
        self.__oldMeasureValue = 0
        self.__measuredPressuresValues =[]
        self.__measuredTimeValues=[]
        self.__measuredTemperatureValues=[]
        self.__measuredPressures={}
        self.__oldPressure=0
        i2c = board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,0x76)

    def run(self):
        self.__isRunning = True
        self.__run()

    def getPressure(self):
        return self.__readJsonFile()



    def Stop(self):
        self.__isRunning = False
    def __run(self):
        while self.__isRunning:
            pressur = self.__readPressur()
            pressureHoch = pressur+0.0001
            pressurUnten = pressur-0.0001
            pressurUnten = round(pressurUnten,4)
            pressureHoch = round(pressureHoch,4)


            if self.__oldPressure > pressurUnten or self.__oldPressure < pressureHoch:
                #if self.__oldPressure != pressur:
                    print("New Pressur: " + str(pressur) + " OLd: " + str(self.__oldPressure))
                    self.__measuredPressuresValues.append(pressur)
                    self.__measuredTimeValues.append(time.time())
                    self.__measuredTemperatureValues.append(self.__readTemperature())
                    self.__writeJsonFile()
                    self.__oldPressure = pressur

    def __writeJsonFile(self):
        measured = [self.__measuredTimeValues, self.__measuredPressuresValues,self.__measuredTemperatureValues]
        self.__measuredPressures.update({self.__numberOfMeasurements: measured})
        self.__numberOfMeasurements = self.__numberOfMeasurements + 1
        jsonString = json.dumps(measured)
        jsonFile = open("data.json", "w+")
        jsonFile.write(jsonString)
        jsonFile.close()
    def __readJsonFile(self):
        with open('data.json', 'r') as myfile:
            data = myfile.read()
        return json.loads(data)
    def clibration(self):
        print("Starte Kalibrierung")
        measuredPressures = [0]
        measureTime = 1
        endTime = time.time() + measureTime
        while endTime > time.time():
            measuredPressures.append(self.__readPressur())
        tmpMean = sum(measuredPressures)/len(measuredPressures)
        self.__mean = round(tmpMean, 4)
        return self.__mean



    def __readPressur(self):
        pressur = self.__bme280.pressure
        mBar = pressur/1000
        mbar = round(mBar,4)
        return mbar
    def __readTemperature(self):
        return self.__bme280.temperature


















