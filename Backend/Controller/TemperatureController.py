from Backend.Enums.HeatingStates import HeatingStates
class TemperatureController():
    def __init__(self,targetTemperature):
        self.__targetTemperature = int(targetTemperature)
        self.__state = HeatingStates

    def checkTemperature(self,measuredTemperature):
        self.__measuredTemperature = int(measuredTemperature)
        if self.__measuredTemperature < self.__targetTemperature:
            self.__state = HeatingStates.ON
        elif self.__measuredTemperature > self.__targetTemperature:
            self.__state = HeatingStates.OFF
        else:
            self.__state = HeatingStates.SET
        return self.__state


    def TargetTemperature(self,value):
        self.__targetTemperature = value






