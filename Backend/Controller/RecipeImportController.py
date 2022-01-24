import json
import xmltodict
class recipeImportController():
    def __init__(self):
        self.malt = dict = {}
        self.hops = dict = {}


    def getRecipeFromFile(self,file):
        self.__file = file
        self.__fileType = file.split('.')[1]
        default = "Invalid File Format"
        getattr(self, 'case_' + str(self.__fileType), lambda: default)()
        return self.__recipe

    def case_xml(self):
        with open(self.__file) as recipeXML_File:
            self.__recipe = xmltodict.parse(recipeXML_File.read())


    def case_json(self):
        with open(self.__file) as recipeJSON_File:
            self.__recipe = json.load(recipeJSON_File)
        self.__parsing()

    def __parsing(self):
        numberOfMalt = 1
        numberOfHops = 1
        for key in self.__recipe.keys():
            if key.startswith('Malz' + str(numberOfMalt)):
                self.__parsingMalt(numberOfMalt)
                numberOfMalt +=1

            if key.startswith('Hopfen_' + str(numberOfHops)):
                self.__parsingHops(numberOfHops)
                numberOfHops +=1

        print(self.malt)


    def __parsingHops(self,number):
        nameVWH = self.__recipe.get('Hopfen_VWH_' + str(number)+'_Sorte')
        quantityVWH = self.__recipe.get('Hopfen_VWH_' + str(number) + '_Menge')
        alphaVWH = self.__recipe.get('Hopfen_VWH_' + str(number) + '_alpha')
        #print(quantityVWH)
        name = self.__recipe.get('Hopfen_' + str(number)+'_Sorte')
        quantity = self.__recipe.get('Hopfen_' + str(number) + '_Menge')
        cookingTime = self.__recipe.get('Hopfen_' + str(number) + '_Kochzeit')
        alpha = self.__recipe.get('Hopfen_' + str(number) + '_alpha')
        print(name)



    def __parsingMalt(self,number):
            name = self.__recipe.get('Malz' + str(number))
            quantity = self.__recipe.get('Malz' + str(number) + '_Menge')
            unitOfMessure = self.__recipe.get('Malz' + str(number) + '_Einheit')
            self.malt[number] = (name, quantity, unitOfMessure)






