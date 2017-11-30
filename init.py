# Operation setup. Check that your hardware is in the same configuration.

# Define which pins (GPIO) are the servos
rotChannel = 0 # bottom servo, responsible for rotation in the ground plane. Left/Right.
tiltChannel = 1 # left servo, moves the claw Forward/Backward
liftChannel = 2 # right servo, moves the claw Up/Down
gripChannel = 3 # head servo, Opens/Closes the grip

# Operational angles of servos (between 0 and 180) limited by device geometry
rotMin=0 
rotMax=180

tiltMax=115
tiltMin=55

liftMax=65
liftMin=0

gripMin=0
gripMax=110

# Initial position of all servos before operation start
rotInit = 90    # 90 degrees = center of servo operation range.
tiltInit = 105
liftInit = 20
gripInit = 90
