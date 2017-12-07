# Simple implementation of Inverse Kinematics using FABRIK algorithm
# Code based on the code described here: http://wiki.roblox.com/index.php?title=Inverse_kinematics

# Basic idea: 
# Transform angles of robot arm to coordinates.
# Each coordinate is the position of a joint (end-points are also joints)
# Use FABRIK algorithm to generate new joint positions
# Get angles from joint positions
# Set angles to servos

from robotController import * # Hardware controller
from keyboardio import *   # Keyboard reader
import math

jointAmount = 3 # Base, elbow and grip
lengths = [9, 9] # Lengths of the arm
tolerance = 0.0001 # How close the the result must be to be accepted

degToRad = math.pi / 180
radToDeg = 180 / math.pi

#=================================================================
# Gets angles arm needs to be to reach coordinates
def getAnglesForCoordinate(x, y):
    target = [x, y]
    coords = getJointCoords()

    # ----- FABRIK -----
    diff = _magnitude(coords[len(coords) - 1], [x, y])
    ind = 0
    while diff > tolerance:
        _backward(target, coords)
        _forward(target, coords)
        diff = _magnitude(coords[len(coords) - 1], [x, y])

        ind+=1
        if ind >= 50:
            break
    # ------------------

    # --- Get angles from joint coordinates ---

    tiltAngle = 180 - (math.atan2(coords[1][1], coords[1][0]) - math.atan2(0, 1)) * radToDeg

    coordDiff = [coords[2][0] - coords[1][0], coords[2][1] - coords[1][1]]
    liftAngle = -((math.atan2(coordDiff[1], coordDiff[0]) - math.atan2(0, 1)) * radToDeg)
    # -----------------------------------------
    
    return [tiltAngle, liftAngle]
#=================================================================


#=================================================================
# Part of FABRIK algorithm, moves arm to target
def _backward(target, coords):
    coords[len(coords) - 1] = target;
    ind = len(coords) - 2
    while ind >= 0:
        r = [coords[ind + 1][0] - coords[ind][0],
             coords[ind + 1][1] - coords[ind][1]]
        length = lengths[ind] / _magnitude([0, 0], r)
        pos = [(1 - length)*coords[ind+1][0] + length*coords[ind][0],
               (1 - length)*coords[ind+1][1] + length*coords[ind][1]]
        coords[ind] = pos
        ind -= 1
#=================================================================

#=================================================================
# Part of FABRIK algorithm, moves arm to origin
def _forward(target, coords):
    coords[0] = [0, 0];
    ind = 0
    while ind < len(coords) - 1:
        r = [coords[ind + 1][0] - coords[ind][0],
             coords[ind + 1][1] - coords[ind][1]]
        length = lengths[ind] / _magnitude([0, 0], r)
        pos = [(1 - length)*coords[ind][0] + length*coords[ind+1][0],
               (1 - length)*coords[ind][1] + length*coords[ind+1][1]]
        coords[ind + 1] = pos
        ind += 1
#=================================================================


#=================================================================
# Get joint coordinates from arm's current angles
# 0 = base
# 1 = elbow
# 2 = grip
def getJointCoords():
    coords = []

    # Base joint
    coords.append([0,0])

    tiltAngle = (180 - getTilt()) * degToRad
    liftAngle = (-getLift()) * degToRad

    # Elbow joint
    coords.append([
        math.cos(tiltAngle)*lengths[0], 
        math.sin(tiltAngle)*lengths[0]])

    # Grip joint
    coords.append([
        math.cos(liftAngle)*lengths[1] + coords[1][0],
        math.sin(liftAngle)*lengths[1] + coords[1][1]])

    return coords
#=================================================================

#=================================================================
# Returns distance between two points
def _magnitude(point1, point2):
    difference = [point1[0]-point2[0], point1[1]-point2[1]]
    return math.sqrt(difference[0]**2 + difference[1]**2)
#=================================================================


# init()
# try:
#     currentCoords = getJointCoords()
#     print getAnglesForCoordinate(currentCoords[2][0], currentCoords[2][1])

#     manualSpeed = 5
#     coordSpeed = 2

#     angles = getAnglesForCoordinate(4, 4)
#     setLift(angles[1])
#     setTilt(angles[0])
    
#     while True:
#         currentCoords = getJointCoords()
#         keyp = readkey()
#         if keyp == 's' or ord(keyp) == 17:
#             angles = getAnglesForCoordinate(currentCoords[2][0]-coordSpeed, currentCoords[2][1])
#             setAll(getRotation(), angles[0], angles[1], getGrip())
#             print angles
#         elif keyp == 'w' or ord(keyp) == 16:
#             angles = getAnglesForCoordinate(currentCoords[2][0]+coordSpeed, currentCoords[2][1])
#             setAll(getRotation(), angles[0], angles[1], getGrip())
#             print angles
#         elif keyp == 'd' or ord(keyp) == 18:
#             rotate(-manualSpeed)
#             print('Right: ',getRotation())
#         elif keyp == 'a' or ord(keyp) == 19:
#             rotate(manualSpeed)
#             print('Left: ',getRotation())
#         elif keyp == 'q':
#             angles = getAnglesForCoordinate(currentCoords[2][0], currentCoords[2][1]+coordSpeed)
#             setAll(getRotation(), angles[0], angles[1], getGrip())
#             print angles
#         elif keyp == 'e':
#             angles = getAnglesForCoordinate(currentCoords[2][0], currentCoords[2][1]-coordSpeed)
#             setAll(getRotation(), angles[0], angles[1], getGrip())
#             print angles
#         elif keyp == 'g':
#             grip(-manualSpeed)
#             print('Open: ',getGrip())
#         elif keyp == 'h':
#             grip(manualSpeed)
#             print('Close: ',getGrip())
#         elif keyp == ' ':       # 'space' resets to the initial position
#             resetPosition()
#         elif ord(keyp) == 3:
#             break
# finally:
#     shutdown()