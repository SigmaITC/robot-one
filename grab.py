# "Detect and grab" test. Place a small object in front of the robot and run the code. The robot should detect it, grab it and move.
# It is a standalone module. NEEDS TO BE INTEGRATED WITH THE REST AND (probably) PACKAGED TOGETHER WITH THE AUTOMATIC MODE IN operationModes.py


import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 50

print("Test the servos by using the arrow keys to control")
print("Press <space> key to centre")
print("Press Ctrl-C to end")
print()

# Define which pins (GPIO) are the servos
rot = 0 # bottom servo, responsible for rotation in the ground plane. Left/Right.
tilt = 1 # left servo, moves the claw Forward/Backward
lift = 2 # right servo, moves the claw Up/Down
grip = 3 # head servo, Opens/Closes the grip

pz.init()

# Set output mode to Servo
pz.setOutputConfig(rot, 2)
pz.setOutputConfig(tilt, 2)
pz.setOutputConfig(lift, 2)
pz.setOutputConfig(grip, 2)

# Operational angles of servos (between 0 and 180) limited by device geometry
tiltMax=115
tiltMin=55
rotMin=0
rotMax=180
liftMax=75
liftMin=0
gripMin=0
gripMax=110

# Initial position of all servos at the beginning of operation
rotVal = 90 # 90 degress = center
tiltVal = 100
liftVal = 0
gripVal = 90
pz.setOutput (rot, rotVal)
pz.setOutput (tilt, tiltVal)
pz.setOutput (lift, liftVal)
pz.setOutput (grip, gripVal)

gripDistance = 3    # the distance to sensor below which the grabbing is commenced
pz.setOutput (grip,gripMin)
time.sleep(.5)

import hcsr04
hcsr04.init()
# main loop
try:
    distance = int(hcsr04.getDistance())
    print "object "+str(distance)+" far"
    while (distance>gripDistance) and (tiltVal>tiltMin):
        distance =int(hcsr04.getDistance())         # distance in cm
        print "object "+str(distance-gripDistance)+" too far"
        
        tiltVal = max (tiltMin, tiltVal - 5)    # moves closer, but within the operational limit
        
        time.sleep(.5)      # gives you time to evacuate, can have zero
        pz.setOutput (rot, rotVal)
        pz.setOutput (tilt, tiltVal)
        pz.setOutput (lift, liftVal)


	
except KeyboardInterrupt:
    print()

finally:
    if (distance>gripDistance):
        print ("object unreachable")
    else:       # grab and move if the object is withing grabbing distance
        print ("EXTERMINATE")
        pz.setOutput (grip,gripMax)
        time.sleep(.5)
        print ("EXTERMINATE")
        pz.setOutput (rot, 40)
        time.sleep(.5)
        pz.setOutput (tilt, tiltVal-10)
        time.sleep(.5)
        pz.setOutput (lift, liftMax)
        time.sleep(.5)
        print ("EXTERMINATE!")
    hcsr04.cleanup()
    pz.cleanup()