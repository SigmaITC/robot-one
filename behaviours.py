# Module with anthropomorphic behaviours

from init import *   # hardware configuration
from robotController import * # Hardware controller
from inverseKinematics import *
from basicActions import *
import random, time


currentMode = None
timestamp = time.time()
lungeTimer = time.time()

#======================================================================
# Main AI loop, will execute state until interrupted
#
def AILoop():
    while True:
        currentMode()
        time.sleep(0.01)
#======================================================================

#======================================================================
# Shy behaviour, will try to hide if anything comes too close
def shy():
    global currentMode

    # Init shy behaviour
    currentMode = _afraid
    setAll(getRotation(), tiltMin + 10, liftMax / 2, gripMax / 2)
    print "Afraid"

    AILoop()
#======================================================================

#======================================================================
# Default shy action, will look for dangers
def _afraid():
    global currentMode

    # Is anyone close?
    closest = texasRanger()
    if closest < 9:
        currentMode = _hide
        print "Hiding!"
        return

    # Small, sporadic movements to mimic "life"
    shouldMove = random.randint(1, 6)
    if(shouldMove == 1):
        liftOffset = random.randint(-5, 5)
        rotOffset = random.randint(-5, 5)
        gripOffset = random.randint(-5, 5)

        liftResult = lift(liftOffset)
        if not liftResult:
            lift(-liftOffset)

        rotateResult = rotate(rotOffset)
        if not rotateResult:
            rotate(-rotOffset)

        gripResult = grip(gripOffset)
        if not gripResult:
            grip(-gripOffset)
#======================================================================

#======================================================================
# Hiding action
def _hide():
    global currentMode
    global timestamp

    # Find corner to hide in
    randomRotation = random.randint(rotMin, rotMax)
    setSpeed(0.005)
    setAll(randomRotation, tiltMin, liftMax, gripMax)
    setSpeed(speedInit)

    # Setup for cower
    timestamp = time.time()
    currentMode = _cower
    print ":("
#======================================================================

#======================================================================
# Cowering action, will try to hide again if threatened
def _cower():
    global currentMode

    # Is anyone close?
    closest = texasRanger()
    if closest < 9:
        currentMode = _hide
        return

    # Calm down after five seconds of inactivity
    currentTime = time.time()
    if currentTime - timestamp > 5:
        setAll(getRotation(), tiltMin + 10, liftMax / 2, gripMax / 2)
        currentMode = _afraid
        print "Is it gone?"
#======================================================================

#======================================================================
# Agressive behaviour, will pick fights with whatever is close
def agressive():
    global currentMode

    print "Angry!"
    currentMode = _lookingForTrouble

    # Agressive speed for agressive mode!
    setSpeed(0.007)
    setAll(getRotation(), tiltMin + 30, liftMax / 2, gripMax / 2)

    AILoop()
#======================================================================

#======================================================================
# Default agressive action, will try to look for enemies
def _lookingForTrouble():
    global currentMode
    global timestamp
    global lungeTimer

    # Is there anything to fight?
    closest = texasRanger()
    if closest < 20:
        setAll(getRotation(), tiltMin, getLift() - 20, gripMin)
        timestamp = time.time()
        lungeTimer = time.time()
        print "Fight me!"
        currentMode = _posturing
        return

    # Large, confident movements while looking for baddies
    shouldMove = random.randint(1, 4)
    if shouldMove == 1:
        liftOffset = random.randint(-10, 10)
        rotOffset = random.randint(-30, 30)
        gripOffset = random.randint(-10, 10)

        liftResult = lift(liftOffset)
        if not liftResult:
            lift(-liftOffset)

        rotateResult = rotate(rotOffset)
        if not rotateResult:
            rotate(-rotOffset)

        gripResult = grip(gripOffset)
        if not gripResult:
            grip(-gripOffset)
#======================================================================

#======================================================================
# Agressive posturing, to scare away foes
def _posturing():
    global currentMode
    global timestamp
    global lungeTimer

    # Calms down after three seconds if enemy leaves
    currentTime = time.time()
    if currentTime - timestamp > 3:
        print "Didn't think so!"
        setAll(getRotation(), tiltMin + 30, liftMax / 2, gripMax / 2)
        currentMode = _lookingForTrouble
        return

    # Do various threatening motions
    action = random.randint(1, 6)
    closest = texasRanger()
    if closest < 20:
        # Reset calm down cooldown
        timestamp = time.time()

        # Menacing flailing of mandibles
        if action == 1:
            setGrip(gripMin + 30)
            setGrip(gripMin)

        # Dangerous lunge!
        if action == 2 and currentTime - lungeTimer > 2:
            print "HA!"
            setTilt(tiltMin + 30)
            setTilt(tiltMin)
            lungeTimer = time.time()

    # Look for weaknesses
    if action == 3 or action == 4:
        liftOffset = random.randint(-3, 3)
        lift(liftOffset)
#======================================================================

random.seed()
init()
initUltrasonic()

try:
    print "Select operation mode: agressive (a) or shy (s)"
    keyp = readkey()
    if keyp == 'a':
        agressive()
    elif keyp == 's':
        shy()
    else:
        print "You are a smart one, aren't you?"
except KeyboardInterrupt:
    print " "
finally:    # sets the robot back to the initial position
    shutdown()

