# Operation setup. Check that your hardware is in the same configuration.

speed = 60

# Define which pins (GPIO) are the servos
rot = 0 # bottom servo, responsible for rotation in the ground plane. Left/Right.
tilt = 1 # left servo, moves the claw Forward/Backward
lift = 2 # right servo, moves the claw Up/Down
grip = 3 # head servo, Opens/Closes the grip
channels=[rot,tilt,lift,grip]


# Operational angles of servos (between 0 and 180) limited by device geometry
rotMin=0 
rotMax=180

tiltMax=115
tiltMin=55

liftMax=65
liftMin=0

gripMin=0
gripMax=110

limMax=[rotMax, tiltMax, liftMax, gripMax]
limMin=[rotMin, rotMin, liftMin, gripMin]

# Initial position of all servos before operation start
rotInit = 90    # 90 degrees = center of servo operation range.
tiltInit = 105
liftInit = 20
gripInit = 90

positions=[rotInit,tiltInit,liftInit,gripInit]      # Position variable that the program operates on


