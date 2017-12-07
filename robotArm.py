# Authors: yevgeniy.korniyenko@sigma.se, henrik.svensson@sigma.se and simon.ivarsson@sigma.se
# Main module of the robot arm

from operationModes import *
import robotController as rc 

# main loop
rc.init()

print "Main loop started"
try:
    print "Select operation mode: automatic (y) or manual (n)"
    keyp = readkey()
    if keyp == 'n':
        manualMode()
    elif keyp == 'y':
        automaticMode()
    else:
        print "You are a smart one, aren't you?"
except KeyboardInterrupt:
    print " "
finally:    # sets the robot back to the initial position
    rc.shutdown()