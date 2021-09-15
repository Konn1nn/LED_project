import explorerhat
import time


if __name__ == "__main__":
    keep_running = True
    explorerhat.light.on()
    distance_sensor = explorerhat.analog.one
    trigger = explorerhat.output.two

    while keep_running:
        trigger.on()
        time.sleep(0.00001)
        trigger.off()
        distance = distance_sensor.read()

        print(distance)
        #time.sleep(1)
        if explorerhat.touch.four.is_pressed():
            keep_running = False