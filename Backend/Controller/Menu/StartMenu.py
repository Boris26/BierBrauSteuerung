from BackendApplication.Controller.Menu.IMenuController import IMenuController
class StartMenu(IMenuController):
    def __init__(self,display):
        self.__display = display
        self.__display.clearDisplay()
        self.__display.setTextOnLine1("     Start Menü     ")
        self.__display.setTextOnLine2("--------------------")
    def update(self,id):
        default="case_1"
        getattr(self,'__case_'+str(id), lambda : default)()
    def clickUpdate(self):
        return self.__selectedCase

    def __case_1(self):
        self.__display.setTextOnLine3(">Bier Brauen")
        self.__display.setTextOnLine4(" Nur Motor")
        self.__selectedCase = 'Bier'
    def __case_2(self):
        self.__display.setTextOnLine3(" Bier Brauen")
        self.__display.setTextOnLine4(">Nur Motor")
        self.__selectedCase = 'Motor'





