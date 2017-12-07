## This file contains modules for operation of MeArm robotic arm with 4 servos using Picon Zero hat
## on Raspberry Pi Zero (v1.3)-

import piconzero as pz, time    # get the servo module

from init import *   # hardware configuration
from keyboardio import *   # Keyboard reader
from robotController import * # Hardware controller
from inverseKinematics import *

#=================================================================
# Main loop for the manual operation via keyboard
def manualMode():

    print "Test the servos by using the following controls:"
    print "Press W or S to move the arm forward or backward"
    print "Press A or D to rotate the arm"
    print "Press Q or E to move the arm up or down"
    print "Press G or H to control the grip"
    print "Press <space> key to centre"
    print "Press Ctrl-C to end"
    print " "

    manualSpeed = 5
    
    while True:         
        keyp = readkey()
        if keyp == 's' or ord(keyp) == 17:
            tilt(-manualSpeed)
            print('Backward: ',getTilt())
        elif keyp == 'w' or ord(keyp) == 16:
            tilt(manualSpeed)
            print('Forward: ',getTilt())
        elif keyp == 'd' or ord(keyp) == 18:
            rotate(-manualSpeed)
            print('Right: ',getRotation())
        elif keyp == 'a' or ord(keyp) == 19:
            rotate(manualSpeed)
            print('Left: ',getRotation())
        elif keyp == 'q':
            lift(-manualSpeed)
            print('Up: ',getLift())
        elif keyp == 'e':
            lift(manualSpeed)
            print('Down: ',getLift())
        elif keyp == 'g':
            grip(-manualSpeed)
            print('Open: ',getGrip())
        elif keyp == 'h':
            grip(manualSpeed)
            print('Close: ',getGrip())
        elif keyp == ' ':       # 'space' resets to the initial position
            resetPosition()
        elif ord(keyp) == 3:
            break
    return 0
#=================================================================

#==============================================================================
# Identifies objects close by (20cm) and their coordinates within the grabbing range (10cm) 
def automaticMode():

    # Initialization : moves the robot to the rightmost position
    initUltrasonic()
    print "Initializating scan..."
    setRotation(rotMin)
    setTilt(tiltMin)
    setLift(liftMax)
    setGrip(gripMin)
    # end initialization
    
    targetPos = []    # Keeps track of detected target locations (robot arm position)

    # scanning    
    increment = 10    # rotation and lift position increment for scanning
    
    liftRange = range(liftMax,liftMin,-increment)  # scanning range : lifting
    rotRange = range(rotMin,rotMax,increment)
    
    print "Scanning..."
    for liftPos in liftRange: # goes through the lifting range
        setLift(liftPos)
        for rotPos in rotRange: # goes through the rotation range
        
            distance = texasRanger()
            if distance<10:
                print "A target within range detected"
                targetPos.append((
                    getRotation(), 
                    getLift(),
                    True)) # Within range
            elif distance<=20:
                print "A target out of range detected"
                targetPos.append((
                    getRotation(),
                    getLift(),
                    False)) # Out of range

            setRotation(rotPos)
            time.sleep(.02)

        rotRange=rotRange[::-1]      # reverse scanning direction for rotation, makes the scanning continuous
    print "Scan finished."
    print " "
    
    suggestions = generateGrabSuggestions(targetPos, increment, increment)

    if len(suggestions) == 0:
        print "No objects found."
    else:
        print "Number of targets within reach: "+str(len(suggestions))    
        print " "
        print "Press a number between 1 and "+str(len(suggestions))+" to grab target"

        while True:         
            keyp = readkey()
            if keyp >= '1' and keyp <= str(len(suggestions)):
                print "Grabbing target " + keyp
                setRotation(suggestions[int(keyp) - 1][0])
                setLift(suggestions[int(keyp) - 1][1])
                bestRotation=findClosest()
                setRotation(bestRotation)
                grabIK()
                return 0
            else:
                print "That was not a number between 1 and "+str(len(objects))
    
    return 0
#==============================================================================

#==============================================================================
# Tries to grab the object in front of the arm
# TODO: Move function somewhere else
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
# TODO: Move function somewhere else
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
# Tries to find the rotation angle pointing at the center of a detected object
# TODO: Move function somewhere else
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

#==============================================================================
# Generates suggestions of tilt and rotation for grabbing
# Returns array of (suggestedTilt, suggestedRotation)
# TODO: Move function somewhere else
def generateGrabSuggestions(positions, rotationRes, tiltRes):
    if len(positions) == 0:
        return []

    groups = []
    positions = sorted(positions)
    groups.append([
        positions[0][0],  # Minimum Rotation
        positions[0][0],  # Maximum Rotation
        positions[0][1],  # Minimum Tilt
        positions[0][1],  # Maximum Tilt
        positions[0][2]]) # At least one point in group within range

    # ------ Make groups from positions ------
    groupId = 0
    ind = 1
    while ind < len(positions):
        if positions[ind][0] == groups[groupId][1]:
            groups[groupId][2] = min(groups[groupId][2], positions[ind][1]) # Set minTilt
            groups[groupId][3] = max(groups[groupId][3], positions[ind][1]) # Set maxTilt
            groups[groupId][4] = groups[groupId][4] | positions[ind][2] # Set in range
        elif positions[ind][0] == (groups[groupId][1] + rotationRes):
            groups[groupId][1] = positions[ind][0] # Set maxRotation
            groups[groupId][2] = min(groups[groupId][2], positions[ind][1]) # Set minTilt
            groups[groupId][3] = max(groups[groupId][3], positions[ind][1]) # Set maxTilt
            groups[groupId][4] = groups[groupId][4] | positions[ind][2] # Set in range
        else:
            # New group
            groups.append([
                positions[ind][0],  # Minimum Rotation
                positions[ind][0],  # Maximum Rotation
                positions[ind][1],  # Minimum Tilt
                positions[ind][1],  # Maximum Tilt
                positions[ind][2]]) # At least one point in group within range
            groupId+=1
        ind+=1
    # ----------------------------------------

    # ----- Find suggestions from groups -----
    returnArray = []
    ind = 0
    while ind < len(groups):
        # If any point of group is in range
        if groups[ind][4]:
            # Suggested rotation and tilt is in the middle of min and max values
            returnArray.append([
                (groups[ind][0] + groups[ind][1])/2, 
                (groups[ind][2] + groups[ind][3])/2])
        ind += 1
    # ----------------------------------------

    return returnArray
#==============================================================================