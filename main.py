import explorerhat
while True:
    explorerhat.light.on()
    if explorerhat.touch.one.is_held():
        explorerhat.output.on()
    else:
        explorerhat.output.off()

    if explorerhat.touch.three.is_held():
        explorerhat.blue.off()
    else:
        explorerhat.blue.on()