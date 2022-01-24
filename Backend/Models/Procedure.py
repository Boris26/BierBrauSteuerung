from Backend.Enums.ProcedureTypes import ProcedureTyps
from Backend.Enums.ProcedureStates import ProcedureStates

from Backend.Enums.HeatingStates import HeatingStates


class procedure():
    def __init__(self,  type, name, time, temperature,isLast):
        self.__type = type
        self.__name = name
        self.__time = time
        self.__temperature = temperature
        self.__isLast = isLast
        self.__createMessages()

    def __createMessages(self):
        self.__stateMessages = {ProcedureStates.HEAT_ON: self.__name + ": " + ProcedureStates.HEAT_ON,
                    ProcedureStates.HEAT_OFF: self.__name + ": " + ProcedureStates.HEAT_OFF,
                    ProcedureStates.RUNNING: self.__name + ": " +ProcedureStates.RUNNING,
                     ProcedureStates.FINISHED: self.__name +": "+ ProcedureStates.FINISHED
        }

        if self.__type == ProcedureTyps.MASHING_IN:
            self.__stateMessages.update({ProcedureStates.WAITING: "Warte auf Starten der Rast"})
        if self.__type == ProcedureTyps.MASHING_OUT:
            self.__stateMessages.update({ProcedureStates.WAITING: "Warte auf Prüfen der Jod Probe"})



    @property
    def Type(self):
        return self.__type

    @property
    def Name(self):
        return self.__name

    @property
    def Time(self):
        return self.__time*60

    @property
    def Temperature(self):
        return self.__temperature

    @property
    def StateMessages(self):
        return self.__stateMessages
    @property
    def IsLast(self):
        return self.__isLast
