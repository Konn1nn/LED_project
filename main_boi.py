import time
import explorerhat

import board
import adafruit_tcs34725


i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)

def blink182(times = 10, wait_time = 0.5):
    for i in range(times):
        explorerhat.output.one.on()
        time.sleep(wait_time/2)
        explorerhat.output.one.off()
        time.sleep(wait_time/2)

def drive(motor1 = 50, motor2 = 50, length = 2):
    explorerhat.motor.one.forwards(motor1)
    explorerhat.motor.two.backwards(motor2)
    time.sleep(length)
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()

def on_line(r_set, g_set, b_set):
    r_read, g_read, b_read = sensor.color_rgb_bytes
    r_diff = r_set - r_read
    g_diff = g_set - g_set
    b_diff = b_set - b_set
    if (r_diff < 10 and r_diff > -10 and g_diff < 10 and g_diff > -10 and b_diff < 10 and b_diff > -10):
        return True
    else:
        return False

def find_line():
    explorerhat.motor.one.forwards(30)
    for i in range(30):
        if on_line():
            explorerhat.motor.stop()
            return True
        time.sleep(0.03)
    explorerhat.motor.stop()
    explorerhat.motor.one.backward(30)
    time.sleep(1)
    explorerhat.motor.stop()
    explorerhat.motor.two.backwards(30)
    for i in range(30):
        if on_line():
            explorerhat.motor.stop()
            return True
        time.sleep(0.03)
    explorerhat.motor.stop()
    explorerhat.motor.two.forwards(30)
    time.sleep(1)
    explorerhat.motor.stop()
    return False

def follow_line(r_set, g_set, b_set):
    keep_running = True
    r_read, g_read, b_read = 0
    while keep_running:
        if on_line():
            explorerhat.motor.one.forwards(50)
            explorerhat.motor.two.backwards(50)
        else:
            explorerhat.motor.stop()
            keep_running = find_line()
    return False




def main():
    explorerhat.light.on()
    keep_running = True


    red, green, blue = 0, 0, 0
    while keep_running:
        if explorerhat.touch.one.is_pressed():
            blink182()
        elif explorerhat.touch.two.is_pressed(): # set the color
            red, green, blue = sensor.color_rgb_bytes
        elif explorerhat.touch.three.is_pressed():
            blink182(5, 1)
            keep_running = follow_line(red, green, blue)
            blink182(100, 0.1)
        elif explorerhat.touch.four.is_pressed():
            explorerhat.motor.one.forwards()
            explorerhat.motor.two.backwards()
            blink182()
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()

    return

if __name__ == "__main__":
    main()



