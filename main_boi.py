import time
import explorerhat


import joshuas_code




class My_bool:
    def __init__(self):
        self.boolean = True

def blink182(times = 10, wait_time = 0.5):
    for i in range(times):
        explorerhat.output.one.on()
        time.sleep(wait_time/2)
        explorerhat.output.one.off()
        time.sleep(wait_time/2)

def blink183(times = 10, wait_time = 0.5):
    clock = time.time()
    bolli = True
    for i in range(1, times + 1):
        bolli = True
        while True:
            if time.time() - clock >= wait_time * i - (wait_time/2):
                explorerhat.output.one.on()
                while True:
                    if time.time() - clock >= wait_time * i:
                        explorerhat.output.one.off()
                        break
                break
def drive(motor1 = 50, motor2 = 50, length = 2):
    explorerhat.motor.one.forwards(motor1)
    explorerhat.motor.two.forwards(motor2)
    time.sleep(length)
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()

def on_line(r_set, g_set, b_set):
    tolerance = 8
    r_read, g_read, b_read = sensor.color_rgb_bytes
    r_diff = r_set - r_read
    g_diff = g_set - g_read
    b_diff = b_set - b_read
    print("The set values are red: {0} , green {1} , blue:  {2}".format(r_read, g_read, b_read))
    if (tolerance > r_diff > -tolerance and
            tolerance > g_diff > -tolerance and
            tolerance > b_diff > -tolerance):
        return True
    else:
        return False

def find_line(r_set, g_set, b_set):

    ret_bool = False

    if check_direction(r_set, g_set, b_set):
        return True
    my_bool.boolean = not my_bool.boolean
    if check_direction(r_set, g_set, b_set):
        return True
    if check_direction(r_set, g_set, b_set):
        return True
    my_bool.boolean = not my_bool.boolean
    if check_direction(r_set, g_set, b_set):
        return True
    my_bool.boolean = not my_bool.boolean
    return ret_bool

def check_direction(r_set, g_set, b_set):

    speed = 60
    # Go left
    for i in range(8):
        if my_bool.boolean:
            explorerhat.motor.one.backwards(speed)
            explorerhat.motor.two.forwards(speed)
        else:
            explorerhat.motor.one.forwards(speed)
            explorerhat.motor.two.backwards(speed)
        time.sleep(0.1)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        time.sleep(0.1)
        if on_line(r_set, g_set, b_set):
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            return True
        time.sleep(0.1)

def follow_line(r_set, g_set, b_set):
    keep_running = True
    r_read, g_read, b_read = 0, 0, 0
    while keep_running:
        if on_line(r_set, g_set, b_set):
            time.sleep(0.2)
            explorerhat.motor.two.forwards(62)
            explorerhat.motor.one.forwards(55)
            time.sleep(0.2)
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
        else:
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            keep_running = find_line(r_set, g_set, b_set)
    return False


def test_loop():
    const = 0.2
    power = 100
    start = time.time()
    while True:
        explorerhat.motor.two.forwards(70)
        explorerhat.motor.one.forwards(60)
        print(time.time() - start)
        if time.time() - start > 5.0:
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            break
    return


my_bool = My_bool()
def main():
    explorerhat.light.on()
    keep_running = True



    red, green, blue = 0, 0, 0
    while keep_running:
        if explorerhat.touch.one.is_pressed():
            blink183()
            joshuas_code.main()
        elif explorerhat.touch.two.is_pressed(): # set the color
            red, green, blue = sensor.color_rgb_bytes
            blink183(1, 0.2)
            print("The read values are red: {0} , green {1} , blue: {2}".format(red, green, blue))
        elif explorerhat.touch.three.is_pressed():
            blink182(3, 1)
            follow_line(red, green, blue)
            blink182(20, 0.1)
        elif explorerhat.touch.four.is_pressed():
            keep_running = False
            """
            explorerhat.motor.one.forwards(50)
            explorerhat.motor.two.forwards(50)
            blink182(1, 1)
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            """
    return

if __name__ == "__main__":
    main()



