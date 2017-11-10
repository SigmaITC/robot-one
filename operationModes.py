## This file contains modules for operation of MeArm robotic arm with 4 servos using Picon Zero hat
## on Raspberry Pi Zero (v1.3)-

# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

import piconzero as pz, time    # get the servo module

import hcsr04       # get the ultrasonic module

from init import *   # hardware configuration

#======================================================================
# A function to make roboArm operation movement smoother, please use for all servo operations

def smoothMotion(channel,stop):
    if (stop>limMax[channel]) or (stop<limMin[channel]):
        print ("Operational range exceeded")
        return 0
    while positions[channel]>stop:
        positions[channel]-=1
        pz.setOutput (channel, positions[channel])
        time.sleep(0.02)        # time.sleep(...) prevents rapid rotation
    while positions[channel]<stop:
        positions[channel]+=1
        pz.setOutput (channel, positions[channel])
        time.sleep(0.02)
    return 0
#=====================================================================

#======================================================================
# Reading input from the keyboard that will control the servos in manual operation
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
#======================================================================



#=================================================================
# Main loop for the manual operation via keayboard: arrows or WASD, G/H for the grip
def manualMode():

    print("Test the servos by using the arrow keys to control")
    print("Press <space> key to centre")
    print("Press Ctrl-C to end")
    print()
    
    while True:         
        keyp = readkey()
        if keyp == 's' or ord(keyp) == 17:
            channel=tilt
            increment=5
            print('Backward', 180-positions[channel])
        elif keyp == 'w' or ord(keyp) == 16:
            channel=tilt
            increment=-5
            print('Forward', 180-positions[channel])
        elif keyp == 'd' or ord(keyp) == 18:
            channel=rot
            increment=-5
            print('Right', positions[channel])
        elif keyp == 'a' or ord(keyp) == 19:
            channel=rot
            increment=5
            print('Left', positions[channel])
        elif keyp == 'q':
            channel=lift
            increment=-5
            print('Up', positions[channel])
        elif keyp == 'e':
            channel=lift
            increment=5
            print('Down', positions[channel])
        elif keyp == 'g':
            channel=grip
            increment=-5
            print('Open', positions[channel])
        elif keyp == 'h':
            channel=grip
            increment=5
            print('Close', positions[channel])
        elif keyp == ' ':       # 'space' resets to the initial position
            channel=0
            increment=0
            smoothMotion(0,rotInit)
            smoothMotion(1,tiltInit)
            smoothMotion(2,liftInit)
            smoothMotion(3,gripInit)
            print('Initial position')
        elif ord(keyp) == 3:
            break
        print positions[channel]
        stop = positions[channel]+increment
        print stop
        smoothMotion(channel, stop)
    return 0
#=================================================================


#=========================================================================================
# Determines range to the nearest object, taking the minimal value of several measurements
# Is used in automaticMode
def texasRanger():
    a=0     # distance sum dummy
    i=0     # measurement counter
    imax=10 # total measurement number
    while i<imax:
        a+=hcsr04.getDistance()
        i+=1
    return a/imax
#=========================================================================================


#==============================================================================
# Identifies objects close by (20cm) and their coordinates within the grabbing range (10cm) 
# NEEDED: add grabbing
def automaticMode():

    # Initialization : moves the robot to the rightmost position
    hcsr04.init()
    print "Initialization of target practice"
    smoothMotion(rot, rotMin)
    smoothMotion(tilt, tiltMin)
    smoothMotion(lift, liftMin)
    smoothMotion(grip, gripMax)
    # end initialization
    
    targetPos=[]    # Keeps track of detected target locations (robot arm position)

    
    # scanning
    flagClose = 0   # a "click", flips to 1 when a target within grabbing distance (10 cm) is detected
    flagFar = 0     # a "click", flips to 1 if a target within 20 cm is detected
    
    increment=15    # rotation and lift position increment for scanning
    
    liftRange=range(liftMin,liftMax,increment)  # scanning range : lifting
    
    for rotPos in range(rotMin,rotMax,increment): # goes through the rotation range
        for liftPos in liftRange:                 # goes through the lifting range
        
            distance=texasRanger()
            print distance
            
            if (distance<10) and (flagClose==0):
                print "A target within range detected"
                flagClose=1
                targetPos.append(positions[:])
            elif (distance<=20) and (flagFar==0):
                print "A target out of range detected"
                flagFar=1
            elif (distance>20):
                flagFar=0
                flagClose=0
            smoothMotion(lift, liftPos)
            positions[lift]=liftPos
            print positions[lift]
            time.sleep(.02)
          
        smoothMotion(rot, rotPos)
        positions[rot]=rotPos
        liftRange=liftRange[::-1]      # reverse scanning direction for lift, makes the scanning continuous
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