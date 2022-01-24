#import MainController
import threading

from Backend import InitGPIO

from Backend.Controller import DS18B20Controller
from Backend.Controller import ProcedureController
from Backend.Controller import RelaisController
from Backend.Controller import MixerController
#from Backend.Controller import BMP280PressureController
#from Backend.Controller import DisplayHD4470Controller

from Backend.ConfigControl import ReadConfigXML
from Backend.Models import Procedure
from Backend.Enums.ProcedureTypes import ProcedureTyps

class main():
    def __init__(self):
        #self.displayController = DisplayHD4470Controller.displayController()
        #self.displayController.setTextOnLine1("Initalisierung")
        self.__loadConfig()
        gpio = InitGPIO.initGPIOs(self.__piConfig)
        self.__GPIO = gpio.initGPIOsetup()

        self.__initController()
        self.__status =""
        #self.displayController.showWelcom()

    @property
    def Status(self):
        return self.__status

    @Status.setter
    def Status(self, value):
        self.__status = value

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
        self.__mixerController = MixerController.mixerController()
        print("Load Mixer Controller")
        self.__relaisController = RelaisController.RelaisController(self.__GPIO, self.__relaisConfig)
        print("Load Relais Controller")
        self.__DS18B20Control = DS18B20Controller.DS18B20Controller(self.__dS18B20Config)
        print("Load DS18B20 Controller")

    def getTemp(self):
        return self.__DS18B20Control.Temperature

    def addProcedure(self,procedure):
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

    def __createProcedures(self,procedur):
        rastCounter =0
        isLast= False
        self.__procedures = []
        MashdownTemperature = procedur["Mashdown"]
        MashupTemperature = procedur["Mashup"]
        self.__procedures.append(Procedure.procedure(ProcedureTyps.MASHING_IN, 'Einmaischen', 0, MashupTemperature,False))
        Rasten = procedur["Rasten"]
        self.numberOfRasten= len(Rasten)
        for item in Rasten:
            self.numberOfRasten = self.numberOfRasten -1
            if self.numberOfRasten == 0:
                isLast = True
            self.__procedures.append(Procedure.procedure(ProcedureTyps.RAST,item,Rasten[item][0],Rasten[item][1],isLast))
        self.__procedures.append(Procedure.procedure(ProcedureTyps.MASHING_OUT, 'Abmaischen', 0, MashdownTemperature,False))
        self.__procedures.append(Procedure.procedure(ProcedureTyps.COOKING,'Kochen', procedur['Cooking_Time'],procedur['Cooking_Temperature'],False))
        self.__procedureController = ProcedureController.procedureController(self,self.__procedures)
        self.__DS18B20Control.add(self.__procedureController)
    def turnON(self):
        self.__relaisController.turnon()
    def turnOFF(self):
        self.__relaisController.turnoff()
    def setSpeed(self,speed):
        self.__mixerController.setSpeedRight(speed)
    def Stop(self):
        self.__mixerController.stop()
    def Start(self,speed):
        self.__mixerController.start(speed)
    def StartCooking(self):
        self.__procedureController.StartCooking = True

    def setFrq(self,speed):
        self.__mixerController.setFrq(speed)
    def go(self):
        self.__procedureController.start()
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
















