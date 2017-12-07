# This module contains basic sets of motions that can be used for various purposes


from init import *   # hardware configuration
from robotController import * # Hardware controller
from inverseKinematics import *

#==============================================================================
# Tries to grab the object in front of the arm
def grab():
    gripDistance = 3
    distance = texasRanger()
    tiltVal = getTilt()
    tiltIncrease = 5

    while distance > gripDistance and tiltVal < tiltMax:
        distance =texasRanger()        # distance in cm
        tiltVal = min (tiltMax, tiltVal + tiltIncrease)    # moves closer, but within the operational limit
        setTilt(tiltVal)

    if (distance>gripDistance):
        print "object unreachable"
    else:       # grab and move if the object is withing grabbing distance
        setGrip(95) # Size of Object, change to not damage servo
        time.sleep(.5)
        setLift(liftMin)
        setTilt(tiltMin)
#==============================================================================

#==============================================================================
# Tries to grab the object in front of the arm
def grabIK():
    distance = texasRanger()

    currentState = getJointCoords()
    currentCoords = currentState[2]
    currentCoords[0] += distance - 0.5
    angles = getAnglesForCoordinate(currentCoords[0], currentCoords[1])
    couldReach = setAll(getRotation(), angles[0], angles[1], getGrip())

    if not couldReach:
        print "object unreachable"
    else:       # grab and move if the object is withing grabbing distance
        setGrip(95) # Size of Object, change to not damage servo
        time.sleep(.5)
        setLift(liftMin)
        setTilt(tiltMin)
#==============================================================================

#==============================================================================
# Tries to find the rotation angle pointing at the closest part of an object
def findClosest():
    distances = []

    startRotation = getRotation()
    currentDistance = texasRanger()

    # ----- Search right -----
    # Rotates once always since if start value is close to edge it might not detect it on the first try
    while(True):
        couldRotate = rotate(-5)
        if not couldRotate:
            break
        time.sleep(.05)
        currentDistance = texasRanger()
        if not currentDistance < 12:
            break
        distances.append([getRotation(), currentDistance])
    # ------------------------

    setRotation(startRotation)
    currentDistance = texasRanger()

    # ----- Search left -----
    # Rotates once always since if start value is close to edge it might not detect it on the first try
    while(True):
        couldRotate = rotate(5)
        if not couldRotate:
            break
        time.sleep(.05)
        currentDistance = texasRanger()
        if not currentDistance < 12:
            break
        distances.append([getRotation(), currentDistance])
    # ------------------------

    bestIndex = 0
    ind=0
    while ind < len(distances) - 1:
        if distances[ind][1] < distances[bestIndex][1]:
            bestIndex = ind
        ind += 1

    if len(distances) > 0:
        return distances[bestIndex][0]
    else:
        print "Target too far away"
        return startRotation
#==============================================================================