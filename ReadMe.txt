$ RobotArm v1.0
========

$ The project helps to setup and use MeArm v1.0 robot controlled via Raspberry Pi Zero v1.3 (RPi) with PiconZero hat. 


Included files
--------------

	ReadMe.txt					$ You are reading it right now. Busted!
	init.py						$ Contains operational angles of RobotArm limited by the hardware setup.
    MeArm.py					$ Main project file. Run it to get your robotic arm swinging.
    operationModes.py			$ Contains modules for manual and automatic operation of RobotArm.
    grab.py                     $ A stand-alone grabbing module for the ultrasonic sensor
    wpa_supplicant.conf			$ Local WiFi info. DO NOT SHARE.
	ssh							$ An empty file for the first ssh connection to RPi

	
Features
--------

    It can rotate and grab things in the manual mode, controlled via keyboard.
    It can detect things via an ultrasonic sensor in the automatic mode.
    It can grab things, watch your back!


Installation
------------

Make sure your RPi is compatible with the project:

    Enable GPIO and i2c for your raspbian on RPi.
	Connect PiconZero robotics controller to RPi's GPIO pins, see https://4tronix.co.uk/blog/?p=1224 .
	Install piconzero.

If you connect to RPi through a new WiFi network, edit the configuration of wpa_supplicant.conf and, together with an empty file named "ssh", add to the root directory on your RPi.

To connect to it you need to install bonjour print service (https://support.apple.com/downloads/bonjour_for_windows).
Then use ssh <username>@pie.local, and enter the password you set on the robot

Robotic arm hardware setup
---------------------------
Your robot is controlled by 4 microservos, connected to corresponding GPIO 0,1,2 and 3 logic pins on PiconZero controller:
	0 = base servo, rotates the arm Left/Right
	1 = left servo, moves the arm Forward/Backward
	2 = right servo, moves the arm Up/Down
	3 = head servo, Opens/Closes the grip


Usage
------------------------
Run MeArm.py and follow the on-screen instructions. 

Rember that when you run it it will instanly go to it's start positon(which most likily is not the same as you have it now), if it's blocked in any way it may break!

Never move parts by hand, this will damage the servos!


Changing parts
-------------
Servos: Unfortantly you will most likily need to disasemble large part of the robot while doing this. make sure the new servos is a pretty good type (the blue). If you use theese you don't need the 

screews while for some other you need to because the plastic arms is sligthly to thick. 
Before assembly, use some code to set an angle on the servo, perhaps in center. Then assembly it in approx center(or whatever you choosed) position. Then open init.py, set xxxInit to this same 

angle. start the code, and change the xxxMin and xxxMax accordingly, you should never make the servos trying to get to a position that's not reachable, this will break the servos.



Missing features, hopes, ideas and random thoughts
---------------------------
    The automatic grabbing module should be integrated with the rest of the automatic mode.
    Measuring dimensions of objects to estimate their grabbability(?).
    Wheels. We need wheels. Got them! just need to assemble. 
    Attacing a camera instead of the ultrasonic module may improve the detection capability greatly. Another idea is to have two ultrasonic sensors for 3D vision. (well, it's really hard to 

actually get something 3Dish useful from these sonars.
also remeber, if using 2 sonars, you can¨t use them "at the same time" both recieve signal from eachother. but one can switch left/right approx every 30-40 ms (Never ever go too short inbetween, it 

can couse lots of trouble.
    Phase 2: object recognition and deep learning. Phase 3: human extinction.


Upgrade to rasberry pi 3, add a camera module and use deeplearning (rasberry pi zero is not good enough to do this). or maybe even nvidia jetson tx2! 
A case to get more cooler stuff could be to build the robot to be used at career fairs.
The current structure is pretty weak, so a better structure etc would be great.
A battery pack should also be needed so we dont have to keep it plugged in, the easiest should be
to just get a powerbank with atleast 2 ports, remember to cheack the amps for the output, currently
it's kinda on the edge with my power adaptor. 


Currently we have a problem that the wife randomly drops, maybe power issue?



Support
-------

If everything else fails, poke me: yevgeniy.korniyenko at sigma.se


License
-------
Feel free to dominate the world with this.
Part of the code is based on a version of mime.co.uk/blog/2016/01/26/mearm-on-the-raspberry-pi/
