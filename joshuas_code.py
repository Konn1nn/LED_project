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

# initializeColorSensor
i2c = busio.I2C(board.SCL, board.SDA)

# score is the input to the pid controller
score = 0
last_valid_score = None  # placeholder for the most recent time an actual color was seen


# create a normalized vector from the rgb triplet.
# normalizing the vector allows you to easily tell the magnitude of a single component relative to the others
def normalize(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]

    magnitude = (r ** 2 + g ** 2 + b ** 2) ** 0.5

    r /= magnitude
    g /= magnitude
    b /= magnitude

    return (r, g, b)


# go from an RGB color vector to a high level interpretation of the color
def get_color(rgb):
    result = None
    lower_limit = 0.64

    colors = ["red", "green", "blue"]

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    # if none of the colors are particularly strong then assume it's the table
    if (r < lower_limit and g < lower_limit and b < lower_limit):
        result = "table"
    else:  # otherwise take the color that is most intense
        max_index = numpy.argmax(rgb)
        result = colors[max_index]

    return result


# determine a score for the color reading
def get_score(rgb):
    global score
    colors = ["red", "green", "blue"]
    scores = {"red": -0.5, "green": 0, "blue": 0.5, "table": 1}

    color = get_color(rgb)
    if (color == "table"):
        global last_valid_score
        if (last_valid_score > 0):
            score = 1
        else:
            score = -1
    else:
        score = 0
        for i in range(3):
            score += scores[colors[i]] * rgb[i]

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
    sounds = rusounds
    rnd_number = random.randint(0,len(sounds)-1)
    pygame.mixer.music.load(sounds[rnd_number])
    pygame.mixer.music.play()
    print("playing sound")

def startup():
    pygame.mixer.init()
    pygame.mixer.music.load("ps1.mp3")
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
    pygame.mixer.music.load("r2d2.mp3")
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
        reading = adafruit_tcs34725.TCS34725(i2c)

        # normalize the color reading
        normalized_rgb = normalize(reading.color_rgb_bytes)

        # determine the actual color (unused for now)
        color = get_color(normalized_rgb)

        # determine the input to the pid controller
        score = get_score(normalized_rgb)
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

        #    print(f"{normalized_rgb} ({color}) -> {score}")

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