import explorerhat
while True:
    explorerhat.light.on()
    if explorerhat.touch.one.is_held():
        explorerhat.output.on()
    else:
        explorerhat.output.off()

    if explorerhat.touch.three.is_held():
        explorerhat.light.blue.off()
    else:
        explorerhat.light.blue.on()