#!/usr/bin/python

import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import os
from rpi_ws281x import *
import time
import requests
import re
import json
from math import *

#definitions
url_base = "https://api.interactions.ics.unisg.ch/cherrybot/"
session = requests.Session()

#log in
operator = {"name": "Tim Neuenschwander", "email": "tim.neuenschwander@students.unisg.ch"}
response_initiate_operator = session.post(url_base+"operator", json=operator)
response_header = (response_initiate_operator.headers["location"])
token = response_header[57:]
aut = {"Authentication": token}
print("The user is now logged in. This is his token:", token)
print("")
#Retrieves the current operator - Get request
def current_operator():
    response_current_operator = requests.get(url_base+"operator")
    if response_current_operator.status_code == 204:
        print("Nobody is operating the robo at the moment.")
    if response_current_operator.status_code == 200:
        data = response_current_operator.json()
        print(data)
#Deletes the current operator - Delete request
def delete_operator(token):
    response_delete_operator = session.delete(url_base+"operator/"+token)
    print("Operator deleted.")
#Initialize the robot
def initialize_robo(aut):
    response_robo_in = session.put(url_base+"initialize", headers=aut)
    print("Iniltializing the robot.")
#Receive the robot's target
def get_robo_target(aut):
    response_get_target = session.get(url_base+"tcp/target", headers=aut)
    print("This is the robots target:", response_get_target.text)
#Set the robot's target
def set_robo_target(aut):
    payload_robo_target = {"target": {"coordinate": {"x": 300,"y": 200,"z": 400},"rotation": {"roll": 180,"pitch": 0,"yaw": 0}},"speed": 50}
    response_set_target = session.put(url_base+"tcp/target", headers=aut, json=payload_robo_target)
    print("Setting the robot's target.")
#Change the grippers position - Get+Put request
def change_gripper_pos(aut):
    response_gripper_pos = requests.get(url_base+"gripper", headers=aut)
    print("This is the gripper's position:",response_gripper_pos.text)
    print("")
    time.sleep(7)
    if int(response_gripper_pos.text) > 200:
        payload_gripper = 120
        set_gripper_pos = session.put(url_base+"gripper", headers=aut, json=payload_gripper)
    else:
        payload_gripper = 280
        set_gripper_pos = session.put(url_base+"gripper", headers=aut, json=payload_gripper)
    time.sleep(7)
    response_gripper_pos_new = requests.get(url_base+"gripper", headers=aut)
    print("This is the gripper's new position:",response_gripper_pos_new.text)
    print("")
#extend the robots arm
def change_robo_pos_extend(aut):
    #step1
    response_robo_pos = requests.get(url_base+"tcp", headers=aut)
    print(response_robo_pos)
    print("This is the robots position:", response_robo_pos.text)
    #step2
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    #step3
    if x >= 0:
        new_x = x + 50 * sin(atan(x/abs(y)))
        time.sleep(2)
    if x < 0:
        new_x = x - 50 * sin(atan(x/abs(y)))
        time.sleep(2)
    if y >= 0:    
        new_y = y + 50 * cos(atan(x/abs(y)))
        time.sleep(2)
    if y < 0:
        new_y = y - 50 * cos(atan(x/abs(y)))
        time.sleep(2)
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    time.sleep(7)
    #step4
    payload_robo_extend = {"target": {"coordinate": {"x":new_x,"y":new_y,"z":z},"rotation": {"roll": 0,"pitch": -90,"yaw": 180}},"speed": 50}
    response_set_extend = requests.put(url_base+"tcp/target", headers=aut, json=payload_robo_extend)
    print(response_set_extend)
    print("Extending the robots arm 5cm.")
    print("")
#retract the robots arm
def change_robo_pos_retract(aut):
    #step1
    response_robo_pos = requests.get(url_base+"tcp", headers=aut)
    print(response_robo_pos)
    print("This is the robots position:", response_robo_pos.text)
    #step2
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    #step3
    if x >= 0:
        new_x = x - 50 * sin(atan(x/abs(y)))
        time.sleep(2)
    if x < 0:
        new_x = x + 50 * sin(atan(x/abs(y)))
        time.sleep(2)
    if y >= 0:
        new_y = y - 50 * cos(atan(x/abs(y)))
        time.sleep(2)
    if y < 0:
        new_y = y + 50 * cos(atan(x/abs(y)))
        time.sleep(2)
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    time.sleep(7)
    #step4
    payload_robo_extend = {"target": {"coordinate": {"x":new_x,"y":new_y,"z":z},"rotation": {"roll": 0,"pitch": -90,"yaw": 180}},"speed": 50}
    response_set_extend = requests.put(url_base+"tcp/target", headers=aut, json=payload_robo_extend)
    print(response_set_extend)
    print("Retracting the robots arm 5cm.")
    print("")
#counterclockwise
def turn_robo_pos_counterclockwise(aut):
    #step1
    response_robo_pos = requests.get(url_base+"tcp", headers=aut)
    print(response_robo_pos)
    print("This is the robots position:", response_robo_pos.text)
    #step2
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    #step3
    grad = radians(12)
    new_x = x * cos(grad) - y * sin(grad)
    time.sleep(3)
    new_y = x * sin(grad) + y * cos(grad)
    time.sleep(3)
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    time.sleep(7)
    #step4
    payload_robo_extend = {"target": {"coordinate": {"x":new_x,"y":new_y,"z":z},"rotation": {"roll": 0,"pitch": -90,"yaw": 180}},"speed": 50}
    response_set_extend = requests.put(url_base+"tcp/target", headers=aut, json=payload_robo_extend)
    print(response_set_extend)
    print("Turning robot counterclockwise.")
    print("")
#clockwise

def turn_robo_pos_clockwise(aut):
    #step1
    response_robo_pos = requests.get(url_base+"tcp", headers=aut)
    print(response_robo_pos)
    print("This is the robots position:", response_robo_pos.text)
    #step2
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    #step3
    grad = radians(-12)
    new_x = x * cos(grad) - y * sin(grad)
    time.sleep(3)
    new_y = x * sin(grad) + y * cos(grad)
    time.sleep(3)
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    time.sleep(7)
    #step4
    payload_robo_extend = {"target": {"coordinate": {"x":new_x,"y":new_y,"z":z},"rotation": {"roll": 0,"pitch": -90,"yaw": 180}},"speed": 50}
    response_set_extend = requests.put(url_base+"tcp/target", headers=aut, json=payload_robo_extend)
    print(response_set_extend)
    print("Turning robot clockwise.")
    print("")
############
# CONSTANTS#
############
# Input pin is 15 (GPIO22)
INPUT_PIN = 15
# To turn on debug print outs, set to 1
DEBUG = 1

###################
# INITIALIZE PINS #
###################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_PIN, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(INPUT_PIN, GPIO.IN)

# Main loop, listen for infinite packets
while True:
    print("\nWaiting for GPIO low")

    # If there was a transmission, wait until it finishes
    #GPIO.wait_for_edge(INPUT_PIN, GPIO.RISING)
    value = 1
    while value:
        sleep(0.001)
        #print("Last read value: {}".format(value))
        value = GPIO.input(INPUT_PIN)       

    # timestamps for pulses and packet reception
    startTimePulse = datetime.now()
    previousPacketTime = 0

    print("\nListening for an IR packet")

    # Buffers the pulse value and time durations
    pulseValues = []
    timeValues = []

    # Variable used to keep track of state transitions
    previousVal = 0

    # Inner loop 
    while True:
        # Measure time up state change
        if value != previousVal:
            # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTimePulse
            startTimePulse = now

            # Record value and duration of current state
            pulseValues.append(value)
            timeValues.append(pulseLength.microseconds)
            
            # Detect short IR packet using packet length and special timing
            if(len(pulseValues) == 3):
                if(timeValues[1] < 3000):
                    print("Detected Short IR packet")
                    #print(pulseValues)
                    #print(timeValues)
                    break;

            # Detect standard IR packet using packet length 
            if(len(pulseValues) == 67):
                if(DEBUG==1):
                    print("Finished receiving standard IR packet")
                    #print(pulseValues)
                    #print(timeValues)
                    
                    #Tim's code
                    
                    address1 = timeValues[2:18]
                    address2 = timeValues[18:34]
                    message1 = timeValues[34:50]
                    message2 = timeValues[50:66]
                    #print("")
                    #print("This is A1:", address1)
                    #print("This is A2:", address2)
                    #print("This is M1:", message1)
                    #print("This is M2:", message2)
                    #print("")
                    
                    del address1[::2]
                    a1 = list(map(int, address1))
                    #print(a1)
                    
                    del address2[::2]
                    a2 = list(map(int, address2))
                    #print(a2)
                    
                    del message1[::2]
                    m1 = list(map(int, message1))
                    #print(m1)
                    
                    del message2[::2]
                    m2 = list(map(int, message2))
                    #print(m2)
                    
                    button = []
                    for i in m1:
                        if i > 1000:
                            button.append(1)
                        else:
                            button.append(0)
                    print("")
                    print("This is the button you pushed:",button)
                    
                    buttonneg = []
                    for i in m2:
                        if i > 1000:
                            buttonneg.append(1)
                        else:
                            buttonneg.append(0)
                    print("This is the negative of the button you pushed:", buttonneg)
                    print("")
                    """The program should then allow you to remote- control the robot with the arrow keys of your IR remote.Specifically, a press of the UP/DOWN arrow keys of the remote should move the robot’s tool center point(TCP) forward/backward by 5cm. Pressing the RIGHT/LEFT arrow key should rotate the robot clockwise/counter-clockwise by approximately 12 degrees. Pressing the OK key should toggle the gripper (open/close).Finally, pressing the # key should release control of the robot (i.e., log off the operator)."""
                    #Buttons:
                    if button == [1, 1, 1, 0, 0, 0, 0, 0]:
                        print("Button number 7")
                        print("")
                        #-->check for current operator of the robot
                        print("This is the user:")
                        current_operator()
                        
                    elif button == [1, 0, 1, 0, 1, 0, 0, 0]:
                        print("Button number 8")
                        #-->initialize the robot
                        initialize_robo(aut)
                        
                    elif button == [1, 0, 0, 1, 0, 0, 0, 0]:
                        print("Button number 9")
                        #-->Get the robot's target
                        get_robo_target(aut)
                    #+OK
                    elif button == [1, 0, 1, 1, 0, 0, 0, 0]:
                        print("Button = #")
                        print("")
                        #-->release control of the robot (i.e., log off the operator)
                        delete_operator(token)
                        
                    elif button == [0, 0, 1, 1, 1, 0, 0, 0]:
                        print("Button = OK")
                        #-->toggle the gripper (open/close)
                        change_gripper_pos(aut)
                        
                    #Arrows
                    elif button == [0, 1, 0, 1, 1, 0, 1, 0]:
                        print("Button Arrow right")
                        #-->rotate the robot clockwise
                        turn_robo_pos_clockwise(aut)

                    elif button == [0, 0, 0, 1, 0, 0, 0, 0]:
                        print("Button Arrow left")
                        #-->rotate the robot counterclockwise
                        turn_robo_pos_counterclockwise(aut)

                    elif button == [0, 0, 0, 1, 1, 0, 0, 0]:
                        print("Button Arrow up")
                        #-->move the robot’s tool center point (TCP) forward by 5cm
                        change_robo_pos_extend(aut)
                            
                    elif button == [0, 1, 0, 0, 1, 0, 1, 0]:
                        print("Button Arrow down")
                        #-->move the robot’s tool center point (TCP) backwards by 5cm
                        change_robo_pos_retract(aut)

                    else:
                        print("Please press button again :)")
                    
                    #TODO: Decode packet and perform task
                    break;

        # save state
        previousVal = value
        # read GPIO pin
        value = GPIO.input(INPUT_PIN)


