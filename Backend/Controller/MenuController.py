from Backend.Controller.Menu.StartMenu import StartMenu
from Backend.Controller.Menu.MainMenu import MainMenu
from Backend.Controller.Menu.RecipeMenu import RecipeMenu
from Backend.Controller.Menu.KYController import KYController


class MenuController(KYController):
    def __init__(self,display,gpio):
        super(self).__init__(self,gpio)
        self.__display = display
    def showMenu(self,menu):
        if menu == "Start":
           self.__menu = StartMenu(self.__display)
        if menu == "Main":
            self.__menu = MainMenu(self.__display)
        if menu == "Recipe":
            self.__menu = RecipeMenu(self.__display)


    def update(self,pos):
        self.__menu.update(pos)
    def clickUpdate(self):
        self.__menu.clickUpdate()










