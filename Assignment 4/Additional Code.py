import requests
import re
import json
import time
from math import *

#definitions
url_base = "https://api.interactions.ics.unisg.ch/cherrybot/"
session = requests.Session()

operator = {"name": "Tim Neuenschwander", "email": "tim.neuenschwander@students.unisg.ch"}
response_initiate_operator = session.post(url_base+"operator", json=operator)
response_header = (response_initiate_operator.headers["location"])
token = response_header[57:]
aut = {"Authentication": token}


#Retrieves the current operator - Get request
def current_operator():
    response_current_operator = requests.get(url_base+"operator")
    if response_current_operator.status_code == 204:
        print("Nobody is operating the robo at the moment.")
    if response_current_operator.status_code == 200:
        data = response_current_operator.json()
        print(data)
    print("")

def delete_operator(token):
    response_delete_operator = session.delete(url_base+"operator/"+token)
    print("Operator deleted.")      
    print("")
def initialize_robo(aut):
    response_robo_in = session.put(url_base+"initialize", headers=aut)
    print("Iniltialize the robot: done!")
    print("")
def get_robo_pos(aut):
    response_robo_pos = session.get(url_base+"tcp", headers=aut)
    print("This is the robots position:", response_robo_pos.text)
    print("")
#≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
#extend
def change_robo_pos_extend(aut):
    response_robo_pos = session.get(url_base+"tcp", headers=aut)
    print("This is the robots position:", response_robo_pos.text)
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    new_x = x + 50 * sin(atan(x/abs(y)))
    new_y = y + 50 * cos(atan(x/abs(y)))
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    payload_robo_extend = {"target": {"coordinate": {"x":new_x,"y":new_y,"z":z},"rotation": {"roll":180,"pitch":0,"yaw":0}},"speed": 50}
    response_set_extend = session.put(url_base+"tcp/target", headers=aut, json=payload_robo_extend)
    print(response_set_extend)
    print("Turn the robot: done!")
    print("")

#clockwise
def turn_robo_pos_clockwise(aut):
    response_robo_pos = session.get(url_base+"tcp", headers=aut)
    print("This is the robots position:", response_robo_pos.text)
    response_robo_pos = response_robo_pos.json()
    x = response_robo_pos['coordinate']['x']
    y = response_robo_pos['coordinate']['y']
    z = response_robo_pos['coordinate']['z']
    print("This is the x coordinate:", x)
    print("This is the y coordinate:", y)
    print("")
    time.sleep(7)
    grad = radians(-12)
    new_x = x * cos(grad) - y * sin(grad)
    new_y = x * sin(grad) + y * cos(grad)
    print("This is the new x coordinate:", new_x)
    print("This is the new y coordinate:", new_y)
    print("")
    payload_robo_turn = {"target": {"coordinate": {"x": new_x,"y": new_y,"z": z},"rotation": {"roll": 180,"pitch": 0,"yaw": 0}},"speed": 50}
    response_set_turn = session.put(url_base+"tcp/target", headers=aut, json=payload_robo_turn)
    print("Turn the robot: done!")
    print("")

#≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
def get_robo_target(aut):
    response_get_target = session.get(url_base+"tcp/target", headers=aut)
    print("This is the robots target:", response_get_target.text)
    print("")
def set_robo_target(aut):
    payload_robo_target = {"target": {"coordinate": {"x": 300,"y": 200,"z": 400},"rotation": {"roll": 180,"pitch": 0,"yaw": 0}},"speed": 50}
    response_set_target = session.put(url_base+"tcp/target", headers=aut, json=payload_robo_target)
    print("Set the robot's target: done!")
    print("")
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
#------------------------------------------------------------------------


current_operator()

time.sleep(12)
get_robo_pos(aut)
time.sleep(12)
change_robo_pos_extend(aut)
time.sleep(12)
initialize_robo(aut)
time.sleep(12)
delete_operator(token)
time.sleep(3)
current_operator()



