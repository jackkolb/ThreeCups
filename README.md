# ThreeCups
A robot that solves the classic "three cup shuffle" game!

This is the source code for my team's CutieHack hackathon project. It is raw, a little buggy, likely unoptimized, yet works!

Materials:
- computer :: to power the code
- camera (we used a USB webcam, although tilting a laptop's forward camera also works) :: the observing "eye"
- breadboards, lights, buttons, and resistors :: to take in inputs and return outputs
- arduino :: to manage lights/buttons, 

How it works:
1. button/LED pins initialize, flashs LEDs thrice when complete
2. waits for a button to be pressed: this corresponds to the starting cup
3. begins tracking the cups:
   a. read an image from the webcam
   b. filters out all but a hardcoded color range (in our project, whites), turns into binary (whites: white, non: black)
   c. blurs and opens the remaining patches to solidify patches
   d. finds blobs
   e. compares current blob positions to previous positions, to determine with blob corresponds to which cup object
   f. updates cup object positions
4. if a specified button is pressed, stop tracking
5. light up the LED corresponding to the tracked cup's position
6. repeat

Requirements:
- code written in Python 2.7.12 (although should be easily modifiable to support Python 3.x, with a few minor changes)
- arduino-python :: Serial interfacing with the Arduino board
- OpenCV :: camera interfacing, image processing, blob detection, image viewing

Notes:
- the code is very rough, with several raw fixes that can definitely be optimized

Bugs:
- if you have the three cups lined up, and quickly pull the ends apart, you may result with the three cup objects following one cup.
- sometimes, usually due to moving one cup too fast for the camera, two cup objects will track one cup.
* We did our best within the time allotment (12h) to mitigate these bugs' occurances, hence some raw fixes

Best of luck!
