import json
import threading
import time
from datetime import timedelta
from Backend.Controller.TemperatureController import TemperatureController
from Backend.Enums.HeatingStates import HeatingStates
from Backend.Enums.ProcedureStates import ProcedureStates
from Backend.Enums.ProcedureTypes import ProcedureTyps
from Backend.Logging import Logger

import asyncio


class procedureController(threading.Thread) :
    def __init__(self, mainController, procedure) :
        threading.Thread.__init__(self)
        self.mainController=mainController
        self.__procedure=procedure
        self.switcher={
            ProcedureTyps.MASHING_IN :self.__Einmaischen(self),
            ProcedureTyps.RAST :self.__Rast(self),
            ProcedureTyps.MASHING_OUT :self.__Abmaischen(self),
            ProcedureTyps.COOKING :self.__Cooking(self)
        }
        self._extendRast=False
        self._extendRastMin=0
        self.logger = Logger.logging()
        self.__automatic=False
        self.__iodineTest=False
        self.__lastRast=False
        self.__startCooking=False
        self.__isBoilingPointReached = False
        self.__countdown=0
        self.__measuredTemperature=0
        self.__heatingStates=HeatingStates
        self.heatUp=False
        self.__status={'elapsedTime' :0, 'currentTime' :0,
                       'Temperature' :"0",
                       'TargetTemperature' :"",
                       'StatusText' :"Warte auf erste Daten",
                       'HeatingStates' :"",
                       'Name' :"",
                       'WaitingStatus' :"",
                       'HeatUpStatus' :""}


    @property
    def State(self) :
        return self.__stateMessages

    @State.setter
    def State(self, value) :
        self.__stateMessages=value

    @property
    def LastRast(self) :
        return self.__lastRast

    @LastRast.setter
    def LastRast(self, value) :
        self.__lastRast=value

    @property
    def Automatic(self) :
        return self.__automatic

    @Automatic.setter
    def Automatic(self, value) :
        self.__automatic=value

    @property
    def ExtendLastRast(self) :
        return self._extendRast

    @ExtendLastRast.setter
    def ExtendLastRast(self, value) :
        self._extendRast=value

    @property
    def StartCooking(self) :
        return self.__startCooking

    @StartCooking.setter
    def StartCooking(self, value) :
        self.__startCooking=value
    @property
    def IsBoilingPointReached(self):
        return self.__isBoilingPointReached
    @IsBoilingPointReached.setter
    def IsBoilingPointReached(self,value):
        self.__isBoilingPointReached = value


    @property
    def IodineTest(self) :
        return self.__iodineTest

    @IodineTest.setter
    def IodineTest(self, value) :
        self.__iodineTest=value

    def run(self) :
        #asyncio.run(self.logger.writeLog("Start Procedure"))
        for procedure in self.__procedure :
            self.elapsedTime=0
            self.currentTime=0
            self.__typ=procedure.Type
            proces=self.switcher.get(procedure.Type)
            self.__name=procedure.Name
            self.__time=procedure.Time
            self.__lastRast =procedure.IsLast
            self.__tepmerature=procedure.Temperature
            self._tc=TemperatureController(self.__tepmerature)
            self.__stateMessages=procedure.StateMessages
            self.__stateMessagesText=""
            self.__index=0
            #asyncio.run(self.logger.writeLog("Start "+self.__name))
            proces.start()
            #asyncio.run(self.logger.writeLog("Beended " + self.__name))
            self._sendUpdate()
        self.mainController.turnOFF_HeatingSystem()
        self.mainController.StopMixer()
        #asyncio.run(self.logger.writeLog("ENDE " + ProcedureStates.BREAWINGFINISHED))
        self._sendStatus(ProcedureStates.BREAWINGFINISHED, False)

    def update(self, obj) :
        self.__measuredTemperature=obj

    def _heatingProcess(self) :
        #asyncio.run(self.logger.writeLog("Start Aufheizen: " + self.__name))
        self.heatUp=True
        g=True
        self.__stateMessagesText=ProcedureStates.HEAT_ON
        self._sendUpdate()
        startTime=time.time()
        while g == True :
            self.currentTime=time.time()
            self.elapsedTime=self.currentTime - startTime
            self.__heatingStates=self._tc.checkTemperature(self.__measuredTemperature)
            if self.__heatingStates == HeatingStates.ON :
                self.mainController.turnON_HeatingSystem()
                self._sendUpdate()
            elif self.__heatingStates == HeatingStates.SET or self.__heatingStates == HeatingStates.OFF:
                g=False
            self._sendUpdate()
        self.__stateMessagesText=ProcedureStates.HEAT_OFF
        self.mainController.turnOFF_HeatingSystem()
        self.heatUp=False
        #asyncio.run(self.logger.writeLog("Ende Aufheizen: " + self.__name))
        self._sendUpdate()

    def _rastProcess(self) :
        startTime=time.time()
        self.__stateMessagesText=ProcedureStates.RUNNING
        self._sendUpdate()
        #asyncio.run(self.logger.writeLog("Start Rast: " + self.__name))

        while self.__stateMessagesText == ProcedureStates.RUNNING :
            self.currentTime=time.time()
            self.elapsedTime=self.currentTime - startTime
            self.__heatingStates=self._tc.checkTemperature(self.__measuredTemperature)
            if self.__heatingStates == HeatingStates.ON :
                self.mainController.turnON_HeatingSystem()
                self._sendUpdate()
            else :
                self.mainController.turnOFF_HeatingSystem()
                self._sendUpdate()
            if self.elapsedTime >= self.__time :
                self.__stateMessagesText=ProcedureStates.FINISHED
                self._sendUpdate()
        #asyncio.run(self.logger.writeLog("Ende Rast: " + self.__name))
        self._sendUpdate()

    def _cookingProcess(self):
        self._sendStatus(ProcedureStates.WAITING+"auf Wasser Kocht",True)
        self.mainController.turnON_HeatingSystem()
        while self.__isBoilingPointReached == False:
            pass
        self.__stateMessagesText=ProcedureStates.RUNNING
        startTime=time.time()
        while self.__stateMessagesText == ProcedureStates.RUNNING:
            self.currentTime=time.time()
            self.elapsedTime=self.currentTime - startTime
            self._sendUpdate()
            if self.elapsedTime >= self.__time :
                self.__stateMessagesText=ProcedureStates.FINISHED
        self._sendUpdate()

    def extendedLastRast(self, values) :
        self._extendRast=values

    def _sendStatus(self, ProcedureStates, waitingStatus) :
        self.__stausText=ProcedureStates
        asyncio.run(self.logger.writeLog("Status Text: " + self.__stausText))
        self.__status={'elapsedTime' :self.elapsedTime, 'currentTime' :self.__time,
                       'Temperature' :self.__measuredTemperature, 'TargetTemperature' :self.__tepmerature,
                       'StatusText' :self.__stausText, 'HeatingStates' :str(self.__heatingStates), 'Name' :self.__name,
                       'Type' :self.__typ, 'WaitingStatus' :waitingStatus, 'HeatUpStatus' :self.heatUp}
        self.__statusJson=json.dumps(self.__status)

        self.mainController.Status=self.__status

    def _sendUpdate(self) :
        self.__stausText=self.__stateMessages.get(self.__stateMessagesText)
        self.__status={'elapsedTime' :self.elapsedTime, 'currentTime' :self.__time,
                       'Temperature' :self.__measuredTemperature, 'TargetTemperature' :self.__tepmerature,
                       'StatusText' :self.__stausText, 'HeatingStates' :str(self.__heatingStates), 'Name' :self.__name,
                       'Type' :self.__typ, 'WaitingStatus' :False, 'HeatUpStatus' :self.heatUp}
        self.__statusJson=json.dumps(self.__status)
        #asyncio.run(self.logger.writeLog("Update: "+self.__statusJson))
        self.mainController.Status=self.__status

    def getStatus(self) :
        return self.__statusJson

    class __Einmaischen(object) :
        def __init__(self, outerClass) :
            self.outerClass=outerClass

        def start(self) :
            self.outerClass._heatingProcess()
            self.outerClass._sendStatus(ProcedureStates.WAITING+"Einmaischen", True)
            while self.outerClass.Automatic == False :
                pass

    class __Rast(object) :
        def __init__(self, outerClass) :
            self.outerClass=outerClass

        def start(self) :
            self.outerClass._heatingProcess()
            self.outerClass._rastProcess()
            if self.outerClass.LastRast == True:
                self.outerClass._sendStatus(ProcedureStates.WAITING+"IodineTest", True)
                while self.outerClass.IodineTest != True :
                    if self.outerClass.ExtendLastRast == True :
                        self.outerClass._rastProcess()
                        self.outerClass.ExtendLastRast=False

    class __Abmaischen(object) :
        def __init__(self, outerClass) :
            self.outerClass=outerClass

        def start(self) :
            self.outerClass._heatingProcess()
            self.outerClass._sendStatus(ProcedureStates.FINISHED, False)
            self.outerClass._sendStatus(ProcedureStates.WAITING+"Start Kochen", True)
            while self.outerClass.StartCooking == False :
                pass

    class __Cooking(object) :
        def __init__(self, outerClass) :
            self.outerClass=outerClass

        def start(self) :
            self.outerClass._cookingProcess()
