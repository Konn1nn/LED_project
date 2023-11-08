#!/usr/bin/python3

import sys
import signal
import explorerhat
import time
import board
import adafruit_tcs34725
import busio
import digitalio
import simple_pid
import numpy
from distancesensor import DistanceSensor
import pygame
import random
from colorsensor2 import TCS34725

# initializeColorSensor
i2c = busio.I2C(board.SCL, board.SDA)

# score is the input to the pid controller
score = 0
last_valid_score = 0  # placeholder for the most recent time an actual color was seen


# create a normalized vector from the rgb_vector triplet.
# normalizing the vector allows you to easily tell the magnitude of a single component relative to the others
def normalize(rgb_vector):
    r, g, b = rgb_vector[0], rgb_vector[1], rgb_vector[2]

    magnitude = (r ** 2 + g ** 2 + b ** 2) ** 0.5

    r /= magnitude
    g /= magnitude
    b /= magnitude

    return (r, g, b)


# go from an rgb_vector color vector to a high level interpretation of the color
def get_color(rgb_vector):
    result = None
    lower_limit = 0.64

    colors = ["red", "green", "blue"]

    red = rgb_vector[0]
    green = rgb_vector[1]
    blue = rgb_vector[2]

    # if none of the colors are particularly strong then assume it's the table
    if (red < lower_limit and green < lower_limit and blue < lower_limit):
        result = "table"
    else:  # otherwise take the color that is most intense
        max_index = numpy.argmax(rgb_vector)
        result = colors[max_index]

    return result


# determine a score for the color reading
def get_score(rgb_vector):
    global score
    colors = ["red", "green", "blue"]
    scores = {"red": -0.5, "green": 0, "blue": 0.5, "table": 1}

    color = get_color(rgb_vector)
    if (color == "table"):
        global last_valid_score
        if last_valid_score == 0:
            last_valid_score = 0
        elif (last_valid_score > 0):
            score = 1
        else:
            score = -1
    else:
        score = 0
        for i in range(3):
            score += scores[colors[i]] * rgb_vector[i]

    return score


# stop the motors
def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()
    explorerhat.light.off()


# exit if ctrl+c is pressed
def signal_handler(sig, frame):
    stop()
    print("User interrupt!")
    turnoff()
    sys.exit(0)


# limit a value
def constrain(value, minimum, maximum):
    result = value

    if (result < minimum):
        result = minimum
    elif (result > maximum):
        result = maximum

    return result


# set the left and right throttles to some particular values
def set_throttles(left, right):
    left = constrain(left, -100, 100)
    right = constrain(right, -100, 100)

    #    print("control {} : {}".format(left, right))

    if (left >= 0):
        explorerhat.motor.one.forward(left)
    else:
        explorerhat.motor.one.backward(abs(left))

    if (right >= 0):
        explorerhat.motor.two.forward(right)
    else:
        explorerhat.motor.two.backward(abs(right))


# set the throttles to particular values after punching them up to a high throttle for a small amount of time (to make sure it starts moving)
def punch_throttles(left=40, right=43, left_punch=100, right_punch=100, punch_time=0.03):
    sign_difference = left * right < 0
    if (sign_difference):
        if (left < 0):
            left_punch *= -1
        else:
            right_punch *= -1

    set_throttles(left_punch, right_punch)
    time.sleep(punch_time)
    set_throttles(left, right)

def play_sound():
    pygame.mixer.init()
    maggisounds = ["Maggimix1.mp3",
                   "Maggimix2.mp3",
                   "Maggimix3.mp3",
                   "Maggimix4.mp3",
                   "Maggimix5.mp3",
                   "Maggimix6.mp3",
                   "Maggimix7.mp3",
                   "maggimixoskur.mp3"]
    rusounds = ["hakon.mp3",
                "joi.mp3",
                "krissi.mp3"]
    sounds = maggisounds
    rnd_number = random.randint(0,len(sounds)-1)
    sound_file = '/home/pi/Documents/LED_project/' + sounds[rnd_number]
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    print("playing sound")

def startup():
    explorerhat.light.blue.off()
    explorerhat.light.yellow.off()
    explorerhat.light.red.off()
    explorerhat.light.green.off()
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Documents/LED_project/ps1.mp3")
    pygame.mixer.music.play()
    explorerhat.light.blue.fade(0,100,2)
    time.sleep(2)
    explorerhat.light.yellow.fade(0, 100, 2)
    time.sleep(2)
    explorerhat.light.red.fade(0, 100, 2)
    time.sleep(2)
    explorerhat.light.green.fade(0, 100, 2)
    time.sleep(2)
    explorerhat.output.one.blink(0.2,0.2)
    time.sleep(2)
    explorerhat.output.one.off()

def turnoff():
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Documents/LED_project/r2d2.mp3")
    pygame.mixer.music.play()
    explorerhat.output.one.blink(0.1, 0.1)
    time.sleep(2)


def main():
    # initialize
    signal.signal(signal.SIGINT, signal_handler)
    print("Hello, world!")
    startup()

    # instantiate a PID controller with kp=20, ki=4, kd=2.5, and setpoint=0
    pid_controller = simple_pid.PID(20, 4, 2.5, setpoint=0)

    base_throttle = 30
    offset = 1  # the motors do not have equal power, so we offset the throttle slightly to drive in a straight line

    # start moving
    punch_throttles(33, 31)
    explorerhat.motor.one.invert()

    # distance sensor
    ds = DistanceSensor()

    time_since = 0
    keep_running = True
    while (keep_running):
        if explorerhat.touch.two.is_pressed():
            keep_running = False
            stop()
            turnoff()
            break
        # get a color reading
        reading = TCS34725(i2c)

        # normalize the color reading
        normalized_rgb_vector = normalize(reading.color_rgb_bytes)

        # determine the actual color (unused for now)
        color = get_color(normalized_rgb_vector)

        # determine the input to the pid controller
        score = get_score(normalized_rgb_vector)
        if (score != 0 and score != -1 and score != 1):
            global last_valid_score
            last_valid_score = score

        # input the score to the pid controller and get back a control effort
        control = pid_controller(score)

        # set the left and right throttles, with the offset and the control effort from the pid controller
        left = base_throttle + offset + control
        right = base_throttle - offset - control

        # propagate the throttle values to the motors
        set_throttles(left, right)

        # notify
        print(f"{left} , {right}")

        #    print(f"{normalized_rgb_vector} ({color}) -> {score}")

        # we don't want to sleep for very long because we want the pid controller to have as much data as possible
        time.sleep(0.01)
        distance = ds.distance()
        while(distance < 10):
            explorerhat.output.one.blink(0.1,0.1)
            set_throttles(0, 0)
            print("There is a big thing %.1f cm in front of me" % distance)
            time.sleep(0.02)
            distance = ds.distance()
            if (time.time() - time_since) > 3:
                play_sound()
                time_since = time.time()
        explorerhat.output.one.off()

if __name__ == "__main__":
    main()
