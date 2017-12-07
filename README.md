# RobotArm v1.0

The project helps to setup and use MeArm v1.0 robot controlled via Raspberry Pi Zero v1.3 (RPi) with PiconZero hat. 


# Included files
| File                 | Description |
| :------------------- | :---------- |
| README.md            | You are reading it right now. Busted! |
| init.py              | Contains operational angles of RobotArm limited by the hardware setup. |
| robotArm.py          | Main project file. Run it to get your robotic arm swinging. |
| operationModes.py    | Contains modules for manual and automatic operation of RobotArm. |
| behaviours.py        | Standalone module with anthropomorphic behaviours |
| robotController.py   | The robot controlling interface |
| keyboardio.py        | Contains functions for keyboard I/O |
| motorTest.py         | Simple test for driving the wheels |
| inverseKinematics.py | Module for finding angles based on coordinates |
| wpa_supplicant.conf  | Local WiFi info. DO NOT SHARE. |
| *piconzero.py*       | External file commited for simplicity |
| *hcsr04.py*          | External file commited for simplicity |

	
# Features

* It can rotate and grab things in the manual mode, controlled via keyboard.
* It can detect things via an ultrasonic sensor in the automatic mode.
* It can grab things, watch your back!
* It can drive around, noisily.
* It can be shy, or threatening!


# Installation

Make sure your RPi is compatible with the project:

    Enable GPIO and i2c for your raspbian on RPi.
	Connect PiconZero robotics controller to RPi's GPIO pins, see https://4tronix.co.uk/blog/?p=1224 .
	Install piconzero.

If you connect to RPi through a new WiFi network, edit the configuration of wpa_supplicant.conf and, together with an empty file named "ssh", add to the root directory on your RPi. 

To connect to it you need to install bonjour print service (https://support.apple.com/downloads/bonjour_for_windows).
Then use ssh <username>@pie.local, and enter the password you set on the robot.

Sometimes the connection to the pi can drop, and it is no longer possible to connect. When this happen you can try to restart the bonjour print service application.



# Robotic arm hardware setup
Your robot arm is controlled by 4 microservos, connected to corresponding GPIO 0,1,2 and 3 logic pins on PiconZero controller:
* 0 = base servo, rotates the arm Left/Right
* 1 = left servo, moves the arm Forward/Backward
* 2 = right servo, moves the arm Up/Down
* 3 = head servo, Opens/Closes the grip

There are also two wheels controlled by two motors, connected to the Motor A and Motor B pins on the PiconZero.

# Usage
Run robotArm.py and follow the on-screen instructions. 

Rember that when you run it it will instanly go to it's start positon (which most likily is not the same as you have it now), if it's blocked in any way it may break!

Never move parts by hand, this will damage the servos!

The grip does not have a spring or sensor to detect if it has grabbed something, so make sure to configure grip angle to fit the object you're trying to grab.

behaviours.py is another module that can be run as-is, and features some anthropomorphic behaviours.

# HC-SR04 limitations and grabbability
According to HC-SR04 specs it can detect objects between 40 m and 2 cm from the sensor. However, when the object becomes too thin it seems it will not register reliably. The robot grip on the other hand cannot grab things that are too thick. So in order to have reliable grabbing an object is needed that is 2 - 3 cm wide, at least 10 cm tall, and preferrably soft in order to be easier to grab and be kinder to the grabbing servo. A styrofoam block has so far been used fairly sucessfully for this purpose.


# Changing parts
Servos: Unfortantly you will most likily need to disasemble large part of the robot while doing this. Make sure the new servos is a pretty good type (the blue). If you use theese you don't need the screws while for some other you need to because the plastic arms is sligthly to thick. 

Before assembly, use some code to set an angle on the servo, perhaps in center. Then assemble it in approx center (or whatever you chose) position. Then open init.py, set xxxInit to this same angle. start the code, and change the xxxMin and xxxMax accordingly, you should never make the servos trying to get to a position that's not reachable, this will break the servos.




# Missing features, hopes, ideas and random thoughts
*Software:*
* Lift and Tilt min and max values depends on the current values of Lift and Tilt. Method could be added to calculate dynamic min and max values
* Integrate driving with other mode?
* Measuring dimensions of objects to estimate their grabbability(?). Probably not doable with sonar, need laser or camera.
* Currently we have a problem that the wifi randomly drops.
* Add support for XBox 360 controller or similar?

*Structure:*
* Powerbank, so it is possible to drive around unconstrained. Easiest should be a powerbank with two ports. Remember to check amp output: a setup with ~900mA to the pi and 1.2A to the Picon Zero is known to work.
* Attach pi to wheel frame. This together with powerbank should grant full autonomy.
* More appropriate fastening between arm and wheels. (Current setup is four picture hooks and three cable strips)
* The current structure is pretty weak, so a better structure etc would be great. Also better servos (blue ones), or step motors!

*Capabilities:*
* Attacing a (3D) camera instead of the ultrasonic module will likely improve the detection capability greatly. 
* Have two ultrasonic sensors for 3D vision. (well, it's really hard to actually get something 3Dish useful from these sonars.)
Remeber, if using 2 sonars, you can't use them "at the same time" both recieve signal from each other. But one can switch left/right approx every 30-40 ms (Never ever go too short inbetween, it can couse lots of trouble.)
* Upgrade to Raspberry pi 3
* Add a camera module and deep learning (rasberry pi zero is not good enough to do this). Maybe even NVidia Jetson TX2?


A case to get more cooler stuff could be to build the robot to be used at career fairs.

Phase 2: object recognition and deep learning. Phase 3: human extinction.
 

# Useful Links
[Robot arm assembly instructions](http://www.instructables.com/id/MeArm-Robot-Arm-Your-Robot-V10/)

[Picon Zero API](https://4tronix.co.uk/blog/?p=1224)


# Support

If everything else fails, poke me: yevgeniy.korniyenko at sigma.se or simon.ivarsson at sigma.se


# License
Feel free to dominate the world with this.
Part of the code is based on a version of http://mime.co.uk/blog/2016/01/26/mearm-on-the-raspberry-pi/
