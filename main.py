import time
import explorerhat


explorerhat.light.on()
while True:
    if explorerhat.touch.one.is_pressed():
        explorerhat.output.one.on()
        time.sleep(5)
        explorerhat.output.one.off()
    else:
        explorerhat.output.one.off()

    if explorerhat.touch.three.is_pressed():
        explorerhat.light.blue.off()
    if explorerhat.touch.two.is_pressed():
        explorerhat.light.blue.on()