# "Detect and grab" test. Place a small object in front of the robot and run the code. The robot should detect it, grab it and move.
# It is a standalone module. NEEDS TO BE INTEGRATED WITH THE REST AND (probably) PACKAGED TOGETHER WITH THE AUTOMATIC MODE IN operationModes.py


import piconzero as pz, time

from init import *   # hardware configuration
from keyboardio import *   # Keyboard reader
from robotController import * # Hardware controller

init()

tiltVal = tiltMin
gripDistance = 3    # the distance to sensor below which the grabbing is commenced
setGrip(gripMin)
setTilt(tiltVal)
time.sleep(.5)

initUltrasonic()
# main loop
try:
    distance = int(texasRanger())
    print "object "+str(distance)+" far"
    while (distance>gripDistance) and (tiltVal<tiltMax):
        distance =int(texasRanger())         # distance in cm
        print "object "+str(distance-gripDistance)+" too far"
        
        tiltVal = min (tiltMax, tiltVal + 5)    # moves closer, but within the operational limit
        
        time.sleep(.5)      # gives you time to evacuate, can have zero
        setTilt(tiltVal)


	
except KeyboardInterrupt:
    print()

finally:
    if (distance>gripDistance):
        print ("object unreachable")
    else:       # grab and move if the object is withing grabbing distance
        setGrip(gripMax)
        time.sleep(.5)
        setRotation(40)
        setTilt(tiltVal-10)
        setLift(liftMax)

    shutdown()