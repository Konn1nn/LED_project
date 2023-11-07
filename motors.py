import time
import explorerhat

class Motors:
    def __init__(self):
        self.m1 = explorerhat.motor.one
        self.m2 = explorerhat.motor.two
        self.m1.invert()

    def drive(self, motor1=30, motor2=30, forwards=True):
        if forwards:
            explorerhat.motor.one.forwards(100)
            explorerhat.motor.two.forwards(100)
            time.sleep(0.05)
            explorerhat.motor.one.forwards(motor1)
            explorerhat.motor.two.forwards(motor2)
        else:
            explorerhat.motor.one.backwards(100)
            explorerhat.motor.two.backwards(100)
            time.sleep(0.05)
            explorerhat.motor.one.backwards(motor1)
            explorerhat.motor.two.backwards(motor2)

    def turn(self, right=true, motor1=30, motor2=30):
        if right:
            explorerhat.motor.one.forwards(100)
            explorerhat.motor.two.backwards(100)
            time.sleep(0.05)
            explorerhat.motor.one.forwards(motor1)
            explorerhat.motor.two.backwards(motor2)
        else:
            explorerhat.motor.one.backwards(100)
            explorerhat.motor.two.forwards(100)
            time.sleep(0.05)
            explorerhat.motor.one.backwards(motor1)
            explorerhat.motor.two.forwards(motor2)

    def stop(self):
        self.m1.stop()
        self.m2.stop()