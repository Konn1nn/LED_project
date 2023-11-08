#!/usr/bin/python3
import sys
import signal
import time
import board
import busio
import pygame
import random
import numpy as np
from simple_pid import PID
from explorerhat import motor, light, touch, output
from distancesensor import DistanceSensor
from colorsensor2 import TCS34725

# Constants
BASE_THROTTLE = 30
OFFSET = 1  # Offset for motor power inequality
PUNCH_TIME = 0.03
MIN_DISTANCE = 10
SOUND_INTERVAL = 3
COLOR_LOWER_LIMIT = 0.74
COLOR_NAMES = ["red", "green", "blue"]
COLOR_SCORES = {"red": -0.5, "green": 0, "blue": 0.5, "table": 1}
SOUND_FILES_DIR = "/home/pi/Documents/LED_project/"
SOUND_FILES = {
    "startup": ["ps1.mp3"],
    "shutdown": ["r2d2.mp3"],
    "maggisounds": [
        "Maggimix1.mp3", "Maggimix2.mp3", "Maggimix3.mp3",
        "Maggimix4.mp3", "Maggimix5.mp3", "Maggimix6.mp3",
        "Maggimix7.mp3", "maggimixoskur.mp3"
    ],
    "rusounds": ["hakon.mp3", "joi.mp3", "krissi.mp3"]
}

# Initialization
i2c = busio.I2C(board.SCL, board.SDA)
pygame.mixer.init()

# Helper Functions
def normalize(rgb):
    """Create a normalized vector from the RGB triplet."""
    magnitude = (rgb[0] ** 2 + rgb[1] ** 2 + rgb[2] ** 2) ** 0.5
    return tuple(map(lambda x: x / magnitude if magnitude else 0, rgb))

def get_color(rgb):
    """Determine the color from an RGB vector."""
    if all(component < COLOR_LOWER_LIMIT for component in rgb):
        return "table"
    else:
        return COLOR_NAMES[np.argmax(rgb)]

def get_score(rgb, last_valid_score):
    """Calculate the score for the color reading."""
    color = get_color(rgb)
    print(f"{color}  and values {rgb}")
    score = COLOR_SCORES[color]
    if color == "table":
        score = 1 #if last_valid_score > 0 else -1
    else:
        score = sum(COLOR_SCORES[COLOR_NAMES[i]] * rgb[i] for i in range(3))
    return score

def stop_motors():
    """Stop all motors."""
    motor.one.stop()
    motor.two.stop()
    light.off()

def signal_handler(sig, frame):
    """Handle interrupt signal to stop motors and exit program."""
    stop_motors()
    print("User interrupt!")
    shutdown_sequence()
    sys.exit(0)

def constrain(value, min_value, max_value):
    """Constrain a value to within a minimum and maximum range."""
    return max(min_value, min(value, max_value))

def set_throttles(left, right):
    """Set the left and right motor throttles with constraints."""
    left = constrain(left, -100, 100)
    right = constrain(right, -100, 100)
    if left >= 0:
        motor.one.forward(left)
    else:
        motor.one.backward(abs(left))
    if right >= 0:
        motor.two.forward(right)
    else:
        motor.two.backward(abs(right))

def punch_throttles(left=40, right=43, left_punch=100, right_punch=100):
    """Boost the motors temporarily before setting to target throttle."""
    sign_difference = left * right < 0
    if sign_difference:
        if left < 0:
            left_punch *= -1
        else:
            right_punch *= -1
    set_throttles(left_punch, right_punch)
    time.sleep(PUNCH_TIME)
    set_throttles(left, right)

def play_sound(sound_type="maggisounds"):
    """Play a random sound from the specified set."""
    sounds = SOUND_FILES.get(sound_type, [])
    if not sounds:
        return  # No sounds to play for the given type
    sound_file = SOUND_FILES_DIR + random.choice(sounds)
    pygame.mixer.music.load(sound_file)
    #pygame.mixer.music.play()
    print(f"Playing sound: {sound_file}")

def startup_sequence():
    """Perform the startup sequence with lights and sound."""
    light.blue.off()
    light.yellow.off()
    light.red.off()
    light.green.off()
    play_sound("startup")
    light.blue.fade(0,100,2)
    time.sleep(2)
    light.yellow.fade(0, 100, 2)
    time.sleep(2)
    light.red.fade(0, 100, 2)
    time.sleep(2)
    light.green.fade(0, 100, 2)
    time.sleep(2)
    output.one.blink(0.2,0.2)
    time.sleep(2)
    output.one.off()

def shutdown_sequence():
    """Perform the shutdown sequence with lights and sound."""
    play_sound("shutdown")
    output.one.blink(0.1, 0.1)
    time.sleep(2)

# Main Functionality
def main():
    # Signal handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Hello, world!")
    startup_sequence()
    
   # PID controller setup
    pid_controller = PID(20, 4, 2.5, setpoint=0)
    pid_controller.sample_time = 0.01
    pid_controller.output_limits = (-40, 40)
    
    # Motor startup
    punch_throttles(33, 31)
    motor.one.invert()

    # Initialize variables
    last_valid_score = 0
    time_since_last_sound = 0
    keep_running = True
    color_sensor = TCS34725(i2c)

    distance_sensor = DistanceSensor()

    while keep_running:
        if touch.two.is_pressed():
            keep_running = False
            stop_motors()
            shutdown_sequence()
            break

        # Get a color reading
        color_reading = color_sensor.color_rgb_bytes
        blue_bias_reading = (color_reading[0], color_reading[1], color_reading[2] *5)
        normalized_rgb = normalize(blue_bias_reading)
        score = get_score(normalized_rgb, last_valid_score)
        
        # Update last valid score if it's not a 'table' color
        if score not in (-1, 0, 1):
            last_valid_score = score
            print(f"Last valid score: {last_valid_score}")

        # PID control
        control_effort = pid_controller(score)
        left_throttle = BASE_THROTTLE + OFFSET + control_effort
        right_throttle = BASE_THROTTLE - OFFSET - control_effort
        set_throttles(left_throttle, right_throttle)

        print(f"Throttles set to: Left={left_throttle}, Right={right_throttle} ")
        #print(f"{normalized_rgb} ({color_sensor.color_rgb_bytes}) -> {score}")

        # Check for obstacles using the distance sensor
        distance = distance_sensor.distance()
        #print(distance)
        while distance < MIN_DISTANCE:
            output.one.blink(0.1, 0.1)
            set_throttles(0, 0)
            print(f"There is a big thing {distance:.1f} cm in front of me")
            # Sleep briefly to avoid tight loop with no delay
            time.sleep(0.02)
            distance = distance_sensor.distance()
            if time.time() - time_since_last_sound > SOUND_INTERVAL:
                play_sound()
                time_since_last_sound = time.time()
        output.one.off()

        # Play sound periodically
        

        # Sleep briefly to avoid tight loop with no delay
        time.sleep(0.01)

if __name__ == "__main__":
    main()
