## This file contains modules for operation of MeArm robotic arm with 4 servos using Picon Zero hat
## on Raspberry Pi Zero (v1.3)-

import piconzero as pz, time    # get the servo module

from init import *   # hardware configuration
from keyboardio import *   # Keyboard reader
from robotController import * # Hardware controller

#=================================================================
# Main loop for the manual operation via keyboard
def manualMode():

    print("Test the servos by using the following controls:")
    print("Press W or S to move the arm forward or backward")
    print("Press A or D to rotate the arm")
    print("Press Q or E to move the arm up or down")
    print("Press G or H to control the grip")
    print("Press <space> key to centre")
    print("Press Ctrl-C to end")
    print()

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
    
    targetPos=[]    # Keeps track of detected target locations (robot arm position)

    
    # scanning
    flagClose = 0   # a "click", flips to 1 when a target within grabbing distance (10 cm) is detected
    flagFar = 0     # a "click", flips to 1 if a target within 20 cm is detected
    
    increment=10    # rotation and lift position increment for scanning
    
    liftRange=range(liftMax,liftMin,-increment)  # scanning range : lifting
    rotRange=range(rotMin,rotMax,increment)
    
    print "Scanning..."
    for liftPos in liftRange: # goes through the lifting range
        setLift(liftPos)
        for rotPos in rotRange: # goes through the rotation range
        
            distance=texasRanger()
            
            if (distance<10) and (flagClose==0):
                print "A target within range detected"
                flagClose=1
                targetPos.append((getRotation(),getLift()))
            elif (distance<=20) and (flagFar==0):
                print "A target out of range detected"
                targetPos.append((getRotation(),getLift()))
                flagFar=1
            elif (distance>20):
                flagFar=0
                flagClose=0
            setRotation(rotPos)
            time.sleep(.02)
        rotRange=rotRange[::-1]      # reverse scanning direction for rotation, makes the scanning continuous
    print "Scan finished."
    print " "
    
    objects = generateGrabSuggestions(targetPos, increment, increment)
    
    print "Number of targets within reach: "+str(len(objects))    
    print " "
    print "Press a number between 1 and "+str(len(objects))+" to grab target"

    while True:         
        keyp = readkey()
        if keyp >= '1' and keyp <= str(len(objects)):
            print "Grabbing target " + keyp
            setRotation(objects[int(keyp) - 1][0])
            setLift(objects[int(keyp) - 1][1])
            bestRotation=findClosest()
            setRotation(bestRotation)
            grab()
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

    print "object "+str(distance)+" far"
    while (distance>gripDistance) and (tiltVal<tiltMax):
        distance =texasRanger()        # distance in cm
        
        tiltVal = min (tiltMax, tiltVal + tiltIncrease)    # moves closer, but within the operational limit
        
        setTilt(tiltVal)

    if (distance>gripDistance):
        print ("object unreachable")
    else:       # grab and move if the object is withing grabbing distance
        setGrip(95) # Size of Object, change to not damage servo
        time.sleep(.5)
        setLift(liftMin)
        setTilt(tiltMin)

    setTiltSpeed(tiltSpeedInit)
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
        if not currentDistance<12:
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
        if not currentDistance<12:
            break
        distances.append([getRotation(), currentDistance])
    # ------------------------

    bestIndex = 0
    ind=0
    while ind <len(distances)-1:
        if(distances[ind][1] < distances[bestIndex][1]):
            bestIndex = ind
        ind+=1

    if len(distances)>0:
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
    groups = [] # Structure: [minRotation, maxRotation, minTilt, maxTilt]
    if len(positions)>1:
        positions = sorted(positions)
        groups.append([positions[0][0], positions[0][0], positions[0][1], positions[0][1]])
        groupId = 0
        ind = 1
        while ind < len(positions):
            if positions[ind][0] == groups[groupId][1]:
                groups[groupId][2] = min(groups[groupId][2], positions[ind][1]) # Set minTilt
                groups[groupId][3] = max(groups[groupId][3], positions[ind][1]) # Set maxTilt
            elif positions[ind][0] == (groups[groupId][1] + rotationRes):
                groups[groupId][1] = positions[ind][0] # Set maxRotation
                groups[groupId][2] = min(groups[groupId][2], positions[ind][1]) # Set minTilt
                groups[groupId][3] = max(groups[groupId][3], positions[ind][1]) # Set maxTilt
            elif positions[ind][0] > (groups[groupId][1] + rotationRes):
                # New group
                groups.append([positions[ind][0], positions[ind][0], positions[ind][1], positions[ind][1]])
                groupId+=1
            else:
                print "What?"
            ind+=1

    returnArray = []
    ind = 0
    while ind < len(groups):
        # Suggested rotation and tilt is in the middle of min and max values
        returnArray.append([(groups[ind][0] + groups[ind][1])/2, (groups[ind][2] + groups[ind][3])/2])
        ind+=1

    return returnArray
#==============================================================================