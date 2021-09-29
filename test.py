import explorerhat
import time

def printer(self, value):
    print(value, time.time())


if __name__ == "__main__":
    keep_running = True
    explorerhat.light.on()
    distance_sensor = explorerhat.analog.one.changed(printer)
    trigger = explorerhat.output.two

    trigger_time = 0.00002
    interval = 0.02

    while keep_running:
        trigger.off() # actually on
        time.sleep(trigger_time)
        trigger.on() # Actually off
        time.sleep(interval - trigger_time)
        #distance = distance_sensor.read()

        #print(distance)
        #time.sleep(1)
        if explorerhat.touch.four.is_pressed():
            keep_running = False