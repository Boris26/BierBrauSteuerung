import json


class Recipe:
    def __init__(self):
        self.rasten = []
        self.water = []

    @property
    def Rast(self):
        return self.rasten

    @property
    def Water(self):
        return self.water


    class Rast:
        def __init__(self, outerClass, name, type, duration, temperature):
            self.__name = name
            self.__type = type
            self.__duration = duration
            self.__temperature = temperature
            outerClass.rasten.append(self.__dict__)

        @property
        def Name(self):
            return self.__name

        @property
        def Type(self):
            return self.__type

        @property
        def Duration(self):
            return self.__duration

        @property
        def Temperature(self):
            return self.__temperature


    class Water:
        def __init__(self, outerClass, designation, quantity, unit):
            self.__designation = designation
            self.__quantity = quantity
            self.__unit = unit
            outerClass.water.append(self.__dict__)

        @property
        def Quantity(self):
            return self.__quantity

        @property
        def Designation(self):
            return self.__designation

        @property
        def Unit(self):
            return self.__unit
