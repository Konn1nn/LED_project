

"""A HC-SR04 driver for raspberry pi"""

import time
from RPi import GPIO

class HCSR04:
    """A simple driver for the HC-SR04 family of ultra sonic distance
    measurement devices."""

    def __init__(self, _trigger, _echo):
        """Constructor. trigger and echo are the trigger and echo pins.
        This constructor configures the pins to input and output,
        respectively."""
        self.trigger = _trigger
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.output(self.trigger, GPIO.LOW)
        self.echo = _echo
        GPIO.setup(self.echo, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def range(self):
        """This call calculates a range from the sensor. It returns
        a distance in cm or None if a distance could not be estimated.
        If the result is None, the object is most likely to close.

        A call make take over 4ms and can be delayed at any time.
        It is not suited for real-time calculations."""
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.000010) # Delay 10 us
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(0.000010) # Delay 10 us
        result = GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout = 3)
        if result is None:
            # We may have missed the rising edge.
            # Either, the reply was too fast, or there is a wiring error.
            return None
        start = time.time()
        # The time out corresponds to a distance of 459 cm.
        # The chip works for distances of 2 cm to 450 cm.
        GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout = 27)
        if result is None:
            # We may have missed the falling edge.
            # This could indicate a wiring error.
            return None
        end = time.time()
        # Speed of sound in cm/s divided by 2
        return (end - start) * 17000.0
