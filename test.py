import explorerhat


if __name__ == "__main__":
    keep_running = True
    explorerhat.light.on()
    distance_sensor = explorerhat.AnalogInput(1)
    trigger = explorerhat.Output(8)

    while keep_running:
        trigger.on()
        distance = distance_sensor.read()
        trigger.off()
        print(distance)
        if explorerhat.touch.four.is_pressed():
            keep_running = False