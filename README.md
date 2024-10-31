# Computer_Vision
Hand Gesture Controlled Servo Motor using Computer Vision and Arduino Uno
This project demonstrates the use of computer vision to control a servo motor through hand gestures. The system leverages a Python program on a PC to recognize hand gestures and sends corresponding commands to an Arduino Uno via serial communication. The Arduino Uno then translates these commands into servo motor movements, allowing for a seamless interaction between the PC and hardware components.

Table of Contents
Project Overview
Features
Hardware and Software Requirements
Installation
Usage
Code Explanation
Future Improvements
License
Project Overview
The goal of this project is to create a system that can detect and interpret hand gestures using a computer vision model on a PC, which then communicates the appropriate action to an Arduino Uno. The Arduino interprets these commands and controls a servo motor accordingly, demonstrating how computer vision and embedded systems can work together in real-time for gesture-controlled interactions.

Features
Real-time Hand Gesture Recognition: Uses computer vision on the PC to recognize specific hand gestures.
Serial Communication: Utilizes serial communication between Python and Arduino for seamless command transfer.
Servo Motor Control: Arduino receives commands and adjusts the servo motor angle based on hand gestures.
Modular Codebase: Separate codebases for PC (Python) and Arduino (C++), making it easy to expand and modify.
Hardware and Software Requirements
Hardware
PC with camera (for computer vision and hand gesture recognition)
Arduino Uno
Servo Motor
Jumper wires and USB cable
Software
Python 3.x
OpenCV (Python library for computer vision)
PySerial (Python library for serial communication)
Arduino IDE
Installation
Clone the Repository

bash
Copy code
git clone <repository-url>
cd hand-gesture-controlled-servo
Install Python Dependencies
Install the required libraries for Python:

bash
Copy code
pip install opencv-python pyserial
Upload Arduino Code

Open the Arduino IDE.
Load the provided Arduino C++ code (servo_control.ino).
Select the correct board and port.
Upload the code to the Arduino Uno.
Usage
Start the Python Script
Run the Python script (gesture_recognition.py) on the PC to begin hand gesture recognition:

bash
Copy code
python gesture_recognition.py
Hand Gesture Recognition

Position your hand in front of the camera.
The program will detect specific gestures and send corresponding commands to the Arduino.
Servo Motor Movement

The Arduino receives commands through serial communication and adjusts the servo motor angle accordingly.
Code Explanation
Python Code (gesture_recognition.py)
The Python code handles:

Hand Gesture Detection: Uses OpenCV to detect gestures and interpret them as commands.
Serial Communication: Sends commands to the Arduino via serial functions.
Arduino Code (servo_control.ino)
The Arduino code:

Receives Commands: Reads data from the serial port.
Controls Servo: Adjusts the servo motor position based on the received commands.
Future Improvements
Enhanced Gesture Recognition: Implement more gestures or improve the accuracy of gesture detection.
Multi-Servo Control: Add the ability to control multiple servos based on different gestures.
Wireless Communication: Replace USB serial communication with wireless options, such as Bluetooth.
License
This project is licensed under the MIT License.
