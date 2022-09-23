from .colorsensor2 import TCS34725
import board

def main():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = TCS34725(i2c)

    while True:
        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        print(
            "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
                color, color_rgb
            )
        )


if __name__ == "__main__":
    main()