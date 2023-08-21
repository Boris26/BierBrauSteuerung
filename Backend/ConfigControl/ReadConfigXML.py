import xml.etree.ElementTree as ET


class ReadConfigXML:
    def __init__(self):
        self.__PiConfig = dict()
        self.__DS18B20Config = dict()
        self.__RelaisConfig = dict()
        self.__BuzzerConfig = dict()
        self.__KY040Config = dict()
        self.__BMP180Config = dict()
        self.__WebAppConfig = dict()
        __tree = ET.parse('/home/boris/Brewmaster/App/Backend/ConfigControl/config.xml')
        root = __tree.getroot()
        for elem in root:
            for subelem in elem:
                if elem.tag == "Pi":
                    self.__PiConfig.update({subelem.tag:subelem.text})
                if elem.tag == "DS18B20":
                    self.__DS18B20Config.update({subelem.tag: subelem.text})
                if elem.tag == "KY040":
                    self.__KY040Config .update({subelem.tag: subelem.text})
                if elem.tag == "Buzzer":
                    self.__BuzzerConfig.update({subelem.tag: subelem.text})
                if elem.tag == "Relais":
                    self.__RelaisConfig.update({subelem.tag: subelem.text})
                if elem.tag == "BMP180":
                    self.__BMP180Config.update({subelem.tag: subelem.text})
                if elem.tag =="WebApp":
                    self.__WebAppConfig.update({subelem.tag: subelem.text})
    @property
    def PiConfig(self):
        return self.__PiConfig

    @property
    def DS18B20Config(self):
        return self.__DS18B20Config

    @property
    def RelaisConfig(self):
        return self.__RelaisConfig

    @property
    def BuzzerConfig(self):
        return self.__BuzzerConfig

    @property
    def KY040Config(self):
        return self.__KY040Config

    @property
    def BMP180Config(self):
        return self.__BMP180Config

    @property
    def WebAppConfig(self):
        return self.__WebAppConfig


