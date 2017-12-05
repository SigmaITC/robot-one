import piconzero as pz, time    # get the servo module

from keyboardio import *   # Keyboard reader

pz.init()

speed = 50

while True:         
    keyp = readkey()
    if keyp == 's' or ord(keyp) == 17:
        pz.reverse(speed)
    elif keyp == 'w' or ord(keyp) == 16:
        pz.forward(speed)
    elif keyp == 'd' or ord(keyp) == 18:
        pz.spinRight(speed)
    elif keyp == 'a' or ord(keyp) == 19:
        pz.spinLeft(speed)
    elif ord(keyp) == 3:
        break

pz.stop()
pz.cleanup()
