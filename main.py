import time
import explorerhat


def blink182():
    for i in range(10):
        explorerhat.output.one.on()
        time.sleep(0.2)
        explorerhat.output.one.off()
        time.sleep(0.2)
        print(i)


explorerhat.light.on()
while True:
    if explorerhat.touch.one.is_pressed():
        for i in range(5):
            explorerhat.output.one.on()
            time.sleep(0.2)
            explorerhat.output.one.off()
            time.sleep(0.2)
            print(i)
    else:
        explorerhat.output.one.off()

    if explorerhat.touch.three.is_pressed():
        explorerhat.light.blue.off()
    if explorerhat.touch.two.is_pressed():
        explorerhat.light.blue.on()
    if explorerhat.touch.four.is_pressed():
        explorerhat.motor.one.forward()
        explorerhat.motor.two.backwards()
        blink182()
        #time.sleep(3)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()

