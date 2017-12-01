## This file contains modules for operation of MeArm robotic arm with 4 servos using Picon Zero hat
## on Raspberry Pi Zero (v1.3)-

import piconzero as pz, time    # get the servo module

import hcsr04       # get the ultrasonic module

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
        elif keyp == 'w' or ord(keyp) == 16:
            tilt(manualSpeed)
        elif keyp == 'd' or ord(keyp) == 18:
            rotate(-manualSpeed)
        elif keyp == 'a' or ord(keyp) == 19:
            rotate(manualSpeed)
        elif keyp == 'q':
            lift(-manualSpeed)
        elif keyp == 'e':
            lift(manualSpeed)
        elif keyp == 'g':
            grip(-manualSpeed)
        elif keyp == 'h':
            grip(manualSpeed)
        elif keyp == ' ':       # 'space' resets to the initial position
            resetPosition()
        elif ord(keyp) == 3:
            break
    return 0
#=================================================================

#==============================================================================
# Identifies objects close by (20cm) and their coordinates within the grabbing range (10cm) 
# TODO: add grabbing
def automaticMode():

    # Initialization : moves the robot to the rightmost position
    initUltrasonic()
    print "Initialization of target practice"
    setRotation(rotMin)
    setTilt(tiltMin)
    setLift(liftMin)
    setGrip(gripMax)
    # end initialization

    
    targetPos=[]    # Keeps track of detected target locations (robot arm position)

    
    # scanning
    flagClose = 0   # a "click", flips to 1 when a target within grabbing distance (10 cm) is detected
    flagFar = 0     # a "click", flips to 1 if a target within 20 cm is detected
    
    increment=15    # rotation and lift position increment for scanning
    
    liftRange=range(liftMin,liftMax,increment)  # scanning range : lifting
    rotRange=range(rotMin,rotMax,increment)
    
    for liftPos in liftRange: # goes through the lifting range
        for rotPos in rotRange: # goes through the rotation range
        
            distance=texasRanger()
            print distance
            
            if (distance<10) and (flagClose==0):
                print "A target within range detected"
                flagClose=1
                targetPos.append([getRotation(),getTilt(),getLift(),getGrip()])
            elif (distance<=20) and (flagFar==0):
                print "A target out of range detected"
                flagFar=1
            elif (distance>20):
                flagFar=0
                flagClose=0
            setRotation(rotPos)
            time.sleep(.02)
          
        setLift(liftPos)
        rotRange=rotRange[::-1]      # reverse scanning direction for rotation, makes the scanning continuous
    print "Initialization finished"
    
    #---- eliminate false readings------------
    # monitors position of neighbouring "clicks", if they are at the same rotation or lift value, eliminate one of them as redundant.
    ind=0
    while ind <len(targetPos)-1:
        print targetPos
        print ind
        if (targetPos[ind+1][0]==targetPos[ind][0]) or (targetPos[ind+1][2]==targetPos[ind][2]):
            del targetPos[ind]
        ind+=1
    #---- end eliminate false readings--------
    
    print "Number of targets within reach: "+str(len(targetPos))    
    print targetPos
    
    return 0
#==============================================================================