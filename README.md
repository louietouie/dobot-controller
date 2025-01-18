## Summary

New Bedford Research Robotics Project

A small program to run GCode on Dobot Magician

## Setup

This github repo includes a dynamic library (and ctypes to allow Python to call C functions from the dynamic library). To run with a Dobot Magician arm, it is also necessary to install DobotStudio since it also installs necessary drivers (CP210x USB to to UART Bridge Drive Installer and Silicon Labs VCP Driver).

When running `main.py`, it is necessary to run it from the `dobot-controller/` directory.

Run with Python 3.13

## Running

1. Determine a `.gcode` file path.
2. Enter the file location into `main.py`
3. Make sure the Dobot Magician is not already connected to another platform (like DobotStudio)
4. Run the `main.py` module

## Other Notes

1. Point to Point (PTP)
	1. MOVJ - move joint positions to an XYZ Cartesian position 
	2. MOVL - move end effector positions to XYZ Cartesian position (straight line)
	3. JUMP - MOVL with additional Z lift (like raising pen)
2. The Download command in DobotStudio downloads the commands to the Dobot so that it can run when not connected to USB by pressing the "Key" button on the back of the dobot.
3. The Dobot commands are placed into a queue, and then run with `SetQueuedCmdStartExec` and `SetQueuedCmdStopExe`. There is a limit to how many commands can be placed in the queue before the Dobot will just become unresponsive. I am unsure of what this limit is yet.

## Sources

1. [Dynamic Library and CTypes](https://www.dobot-robots.com/products/education/magician.html): In the *Dobot Demo v2.3* download
2. [Dobot Sample Video](https://www.youtube.com/watch?v=cWcqbuIb0OM&list=PL45kRIwqe_-0G_o5LOpbpWKSBYJwrPnR5&index=6)
3. [Dobot API Description](https://download.dobot.cc/product-manual/dobot-magician/pdf/en/Dobot-Magician-API-DescriptionV1.2.3.pdf)
4. [Dobot Demos](https://wiki.idiot.io/_media/dobot-magician-demo-description.pdf) ([V2](https://download.dobot.cc/product-manual/dobot-magician/Dobot%20Magician%20Demo%20Description.pdf))

