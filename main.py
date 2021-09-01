import time
import explorerhat


explorerhat.light.on()
while True:
    if explorerhat.touch.one.is_pressed():
        for i in range(3):
            explorerhat.output.one.on()
            time.sleep(0.5)
            explorerhat.output.one.off()
    else:
        explorerhat.output.one.off()

    if explorerhat.touch.three.is_pressed():
        explorerhat.light.blue.off()
    if explorerhat.touch.two.is_pressed():
        explorerhat.light.blue.on()
    if explorerhat.touch.four.is_pressed():
        explorerhat.motor.one.forward()
        explorerhat.motor.two.backwards()
        time.sleep(3)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()