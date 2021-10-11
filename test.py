import explorerhat
import time


class DistanceSensor:
    def __init__(self):
        self.high = 0
        self.high_time = 0
        self.low = 0
        self.low_time = 0


#speed of sound: 343 m/s

    def printer(self, object, value):
        if value > 3.0:
            self.high = value
            self.high_time = time.time()
        elif value < 0.5:
            self.low = value
            self.low_time = time.time()
            print("Meters: {0:.2f}".format(self.compute_reading()))
        print(value, time.time())

    def compute_reading(self):
        return 343*(self.low_time - self.high_time)


if __name__ == "__main__":
    ds = DistanceSensor()
    keep_running = True
    explorerhat.light.on()
    explorerhat.analog.one.changed(ds.printer)
    trigger = explorerhat.output.two

    trigger_time = 0.00002
    interval = 0.10 # Should be 60ms or 20ms instead of 100ms

    while keep_running:
        trigger.on() # Actually off, precaution for trigger
        time.sleep(trigger_time)
        trigger.off() # Actually on
        time.sleep(trigger_time)
        trigger.on() # Actually off
        time.sleep(interval)
        #distance = distance_sensor.read()

        #print(distance)
        #time.sleep(1)
        if explorerhat.touch.four.is_pressed():
            keep_running = False