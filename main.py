import explorerhat
while True:
    explorerhat.light.on()
    if explorerhat.touch.one.is_held():
        explorerhat.output.on()
    else:
        explorerhat.output.off()

    if explorerhat.touch.three.is_pressed():
        explorerhat.light.blue.off()
    else:
        print("you suck")