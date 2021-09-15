import explorerhat


if __name__ == "__main__":
    keep_running = True
    explorerhat.light.on()

    while keep_running:
        some_var = explorerhat.read(1)
        if explorerhat.touch.four.is_pressed():
            keep_running = False