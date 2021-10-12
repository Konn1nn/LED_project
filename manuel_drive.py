import explorerhat
import time



def drive(forward = True):
    motor_one = 100
    motor_two = 98
    if forward:
        explorerhat.motor.one.forwards(motor_one)
        explorerhat.motor.two.forwards(motor_two)
        time.sleep(0.05)
        explorerhat.motor.one.forwards(30)
        explorerhat.motor.two.forwards(25)
    else:
        explorerhat.motor.one.backwards(motor_one)
        explorerhat.motor.two.backwards(motor_two)

def turn(right = True):
    if right:
        explorerhat.motor.one.forwards(100)
        explorerhat.motor.two.backwards(100)
        time.sleep(0.05)
        explorerhat.motor.one.forwards(30)
        explorerhat.motor.two.backwards(30)
    else:
        explorerhat.motor.one.backwards(100)
        explorerhat.motor.two.forwards(100)
        time.sleep(0.05)
        explorerhat.motor.one.backwards(30)
        explorerhat.motor.two.forwards(30)


def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()


def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch






if __name__ == "__main__":
    explorerhat.light.blue.on()
    time.sleep(0.2)
    explorerhat.light.yellow.on()
    time.sleep(0.2)
    explorerhat.light.red.on()
    time.sleep(0.2)
    explorerhat.light.green.on()
    explorerhat.motor.one.invert()
    print("\nchar is '" + getch() + "'\n")

    kb_input = ''
    while kb_input != 'q':
        kb_input = getch()
        if kb_input == 'w':
            drive()
        elif kb_input == 's':
            drive(False)
        elif kb_input == 'a':
            turn(False)
        elif kb_input == 'd':
            turn()
        elif kb_input == 'p':
            stop()
