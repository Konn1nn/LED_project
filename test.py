import explorerhat


if __name__ == "__main__":
    keep_running = True
    explorerhat.light.on()
    distance_sensor = explorerhat.AnalogInput(1)

    while keep_running:
        distance = distance_sensor.read()
        print(distance)
        if explorerhat.touch.four.is_pressed():
            keep_running = False