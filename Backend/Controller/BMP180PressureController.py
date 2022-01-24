import board
import busio
import adafruit_bmp280

class BMP180PressureController():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
    def __readPressure(self):
        print("Temperature: %0.1f C" % self.bmp280.temperature)
        print("Pressure: %0.1f hPa" % self.bmp280.pressure)
        print("Altitude = %0.2f meters" % self.bmp280.altitude)










