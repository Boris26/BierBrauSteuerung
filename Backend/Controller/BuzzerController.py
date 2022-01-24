

class buzzerController():
    def __init__(self,GPIO,config):
        self.__isOn = False
    def toggle(self):
        if self.__isOn:
            self.__pwm.stopBrewing()
            self.__isOn = False
        else:
            self.__pwm.start(50)
            self.__isOn = True






