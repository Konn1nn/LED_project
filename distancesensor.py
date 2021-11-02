import RPi.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self):
        self.setup()
        self.trigger = 12
        self.echo = 22


    def setup(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO Pins
        GPIO_TRIGGER = 12 # output pin 2 on explorerhat
        GPIO_ECHO = 22 # input pin 2 on eplorerhat

        self.trigger = 12
        self.echo = 22

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)


    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        StartTime = time.time()
        StopTime = time.time()
        BreakTime = time.time()

        # save StartTime
        while GPIO.input(self.echo) == 0 and ((time.time() - BreakTime) < 2.0):
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.echo) == 1 and ((time.time() - BreakTime) < 4.0):
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance


if __name__ == '__main__':
    try:
        sensor = DistanceSensor()
        while True:
            dist = sensor.distance()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()