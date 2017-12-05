import piconzero as pz, time    # get the servo module

from keyboardio import *   # Keyboard reader

pz.init()

speed = 50

while True:         
    keyp = readkey()
    if keyp == 's' or ord(keyp) == 17:
        pz.reverse(speed)
        print "Reverse..."
    elif keyp == 'w' or ord(keyp) == 16:
        pz.forward(speed)
        print "Forward..."
    elif keyp == 'd' or ord(keyp) == 18:
        pz.spinRight(speed)
        print "Right..."
    elif keyp == 'a' or ord(keyp) == 19:
        pz.spinLeft(speed)
        print "Left..."
    elif keyp == ' ':
    	pz.stop()
    	print "Stop..."
    elif ord(keyp) == 3:
        break

pz.stop()
pz.cleanup()
