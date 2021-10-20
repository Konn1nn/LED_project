import time
import board
import adafruit_tcs34725

class ColorSensor:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.lux = 0
        self.kelvin = 0

    def read_rgb(self):
        self.red, self.green, self.blue = self.sensor.color_rgb_bytes
        return self.red, self.green, self.blue

    def read_lux(self):
        self.lux = self.sensor.lux
        return self.lux

    def read_kelvin(self):
        self.kelvin = self.sensor.color_temperature

    def set_gain(self, gain = 1):
        legal_gains = [1, 4, 16, 60]
        if gain in legal_gains:
            self.sensor.gain = gain
        else:
            print("Not a valid gain, try 1, 4, 16, 60")

    def set_integral(self, integral = 2.4):
        if (integral >= 2.4) and (integral <= 614.4):
            self.sensor.integration_time = integral
        else:
            print("The integral has to be between 2.4 and 614.4")