#import MainController
import threading

from Backend import InitGPIO

from Backend.Controller import DS18B20Controller
from Backend.Controller import ProcedureController
from Backend.Controller import RelaisController
from Backend.Controller import MixerController
from Backend.Controller import WaterFillingController
from Backend.Controller import TemperatureReader
#from Backend.Controller import BMP280PressureController
#from Backend.Controller import DisplayHD4470Controller

from Backend.ConfigControl import ReadConfigXML
from Backend.Enums.HeatingStates import HeatingStates
from Backend.Models import Procedure
from Backend.Enums.ProcedureTypes import ProcedureTyps
from Backend.Logging import Logger

class main():
    def __init__(self):
        self.__loadConfig()
        gpio = InitGPIO.initGPIOs(self.__piConfig)
        self.__GPIO = gpio.initGPIOsetup()

        self.__initController()
        self.__status =""
        self.__waterStatus=""
        self.__logger = Logger.logging()

    @property
    def Status(self):
        return self.__status

    @Status.setter
    def Status(self, value):
        self.__status = value

    @property
    def WaterStatus(self):
        return self.__waterStatus

    @WaterStatus.setter
    def WaterStatus(self,value):
        self.__waterStatus = value

    def getPressure(self):
        pass
        #return self.__BMP280Controler.getPressure()

    def __loadConfig(self):
        config = ReadConfigXML.ReadConfigXML()
        self.__piConfig = config.PiConfig
        self.__dS18B20Config = config.DS18B20Config
        print("Load DS18B20 Config")
        self.__relaisConfig = config.RelaisConfig
        print("Load Relais Config")

    def __initController(self):
        print("Load BMP280 Controller")
        self.__mixerController = MixerController.mixerController(self.__GPIO)
        print("Load Mixer Controller")
        self.__relaisController = RelaisController.RelaisController(self.__GPIO, self.__relaisConfig)
        print("Load Relais Controller")
        self.__TemperatureReader = DS18B20Controller.DS18B20Controller(self.__dS18B20Config)
        print("Load DS18B20 Controller")
        #self.__TemperatureReader = TemperatureReader.ReadTemperature()
        #print("Load TemperatureReader Controller")



    def getTemp(self):
        return self.__TemperatureReader.Temperature

    def addProcedure(self,procedure):
        print(procedure);
        self.__createProcedures(procedure)

    def extendedLastRast(self,time):
        self.__procedureController.extendedLastRast(time)

    def startFermentMeasur(self):
        print("Load Display Controller")
        #self.__BMP280Controler = BMP280PressureController.BMP280PressureController()
        self.displayController.clearDisplay()
        self.displayController.setTextOnLine1("Gaerung")
        self.displayController.setTextOnLine2("Ueberwachung")
        pressure = self.__BMP280Controler.clibration()
        self.__BMP280Controler.start()
        return pressure

    def getType(self):
        a = ProcedureTyps.MASHING_IN
        return a;

    def getStatus(self):
        return self.Status

    def getWaterStatus(self):
        return self.__waterStatus

    def __createProcedures(self, procedure_data) :
        rastCounter=0
        self.__procedures=[]
        MashdownTemperature=procedure_data["MashdownTemperature"]
        MashupTemperature=procedure_data["MashupTemperature"]
        self.__procedures.append(
            Procedure.procedure(ProcedureTyps.MASHING_IN, 'Einmaischen', 0, MashupTemperature, False))
        Rasten=procedure_data["Rasten"]
        self.numberOfRasten=len(Rasten)
        for rast in Rasten :
            rastCounter+=1
            isLast=rastCounter == self.numberOfRasten
            rast_type=rast["type"]
            rast_temperature=rast["temperature"]
            rast_time=rast["time"]
            self.__procedures.append(
                Procedure.procedure(ProcedureTyps.RAST, rast_type, rast_time, rast_temperature, isLast))
        self.__procedures.append(
            Procedure.procedure(ProcedureTyps.MASHING_OUT, 'Abmaischen', 0, MashdownTemperature, False))
        self.__procedures.append(Procedure.procedure(ProcedureTyps.COOKING, 'Kochen', procedure_data['CookingTime'],
                                                     procedure_data['CookingTemperature'], False))
        self.__procedureController=ProcedureController.procedureController(self, self.__procedures)
        self.__TemperatureReader.add(self.__procedureController)

    def turnON_HeatingSystem(self):
        self.__relaisController.turnon()
        self.__mixerController.toggleHeatingAndStirringTurnOn(True)
    def turnOFF_HeatingSystem(self):
        self.__relaisController.turnoff()
        self.__mixerController.toggleHeatingAndStirringTurnOn(False)
    def setSpeed(self,speed):
        self.__mixerController.setSpeedRight(speed)
    def StopMixer(self):
        self.__mixerController.stop()

    def StartMixer(self, intervalValues):
        print(intervalValues)
        self.__mixerController.start(intervalValues)

    def StopMixerInterval(self):
        self.__mixerController.stopInterval()
    def StartCooking(self):
        print("confirmIStartCooking")
        self.__procedureController.StartCooking = True

    def SetIsBoilingPointReached(self):
        self.__procedureController.IsBoilingPointReached = True

    def setFrq(self,speed):
        self.__mixerController.setFrq(speed)
    def go(self):
        self.__procedureController.start()
        self.turnOFF_HeatingSystem()

    def __run(self):
        pass
    def toggleAutomatic(self):
        self.__procedureController.Automatic = True
    def toggleAgiator(self):
        print("Rührwerk")
    def confirmIodineTest(self):
        print("confirmIodineTest")
        self.__procedureController.IodineTest = True
    def confirmMashup(self):
        print("confirmMashup")
        self.__procedureController.Automatic = True
    def fillWater(self,liters):
        self.__waterFillingController=WaterFillingController.WaterFillingController(self.__GPIO,self)
        self.__waterFillingController.Liters = float(liters)
        self.__waterFillingController.start()

    def fillWaterManuel(self):
        self.__waterFillingController=WaterFillingController.WaterFillingController(self.__GPIO)
        self.__waterFillingController.fillManuel()

    def fillWaterStop(self):
        self.__waterFillingController=WaterFillingController.WaterFillingController(self.__GPIO)
        self.__waterFillingController















