import getch
import explorerhat
import time



def drive(forward = True):
    explorerhat.motor.one.forwards(100)
    explorerhat.motor.two.forwards(100)

def turn(right = True):
    if right:
        explorerhat.motor.one.forwards(100)
        explorerhat.motor.two.backwards(100)
    else:
        explorerhat.motor.one.backwards(100)
        explorerhat.motor.two.forwards(100)


def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()




if __name__ == "__main__":
    explorerhat.light.one.on()
    time.sleep(0.2)
    explorerhat.light.two.on()
    time.sleep(0.2)
    explorerhat.light.three.on()
    time.sleep(0.2)
    explorerhat.light.four.on()


    kb_input = ''
    while kb_input != 'q':
        kb_input = getch.getch()
        if kb_input == 'w':
            drive()
        elif kb_input == 's':
            drive(False)
        elif kb_input == 'a':
            turn(False)
        elif kb_input == 'd':
            turn()
        else:
            stop()
