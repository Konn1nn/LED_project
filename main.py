import explorerhat
explorerhat.light.on()
while True:
    if explorerhat.touch.one.is_pressed():
        explorerhat.output.on()
    else:
        explorerhat.output.off()

    if explorerhat.touch.three.is_pressed():
        explorerhat.light.blue.off()
    else:
        print("you suck")