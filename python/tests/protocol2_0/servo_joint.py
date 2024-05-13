#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os
import struct
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_TORQUE_ENABLE          = 512        # Control table address is different in DYNAMIXEL model
ADDR_GOAL_POSITION          = 564
LEN_GOAL_POSITION           = 4          # Data Byte Length
ADDR_PRESENT_POSITION       = 580
LEN_PRESENT_POSITION        = 4          # Data Byte Length
BAUDRATE                    = 2000000
ADDR_DRIVE_MODE             = 10;

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Make sure that each DYNAMIXEL ID should have unique ID.
DXL_ID = [1, 2, 3, 4, 5, 6]


# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = 'COM1'


TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold
PROFILE_ENABLE              = 0x0;              # Value for enable trajectory profile
PROFILE_DISABLE             = 0x02;             # Value for disable trajectory profile

index = 0
# dxl_goal_position = [0, 1, 5, 10, 18, 28, 41, 56, 73, 92, 114, 137, 164, 192, 223, 256, 291, 328, 368, 410, 455, 501, 550, 601, 655, 710, 768, 828, 891, 956, 1023, 1092, 1164, 1237, 1313, 1388, 1464, 1539, 1614, 1690, 1765, 1840, 1916, 1991, 2067, 2142, 2217, 2293, 2368, 2443, 2519, 2594, 2670, 2745, 2820, 2896, 2971, 3046, 3122, 3197, 3273, 3348, 3423, 3499, 3574, 3649, 3725, 3800, 3872, 3943, 4011, 4077, 4141, 4202, 4261, 4318, 4372, 4425, 4475, 4522, 4568, 4611, 4652, 4691, 4727, 4761, 4793, 4822, 4850, 4875, 4897, 4918, 4936, 4952, 4966, 4977, 4986, 4993, 4997, 5000, 5000, 4997, 4993, 4986, 4977, 4966, 4952, 4936, 4918, 4897, 4875, 4850, 4822, 4793, 4761, 4727, 4691, 4652, 4611, 4568, 4522, 4475, 4425, 4372, 4318, 4261, 4202, 4141, 4077, 4011, 3943, 3872, 3800, 3725, 3649, 3574, 3499, 3423, 3348, 3273, 3197, 3122, 3046, 2971, 2896, 2820, 2745, 2670, 2594, 2519, 2443, 2368, 2293, 2217, 2142, 2067, 1991, 1916, 1840, 1765, 1690, 1614, 1539, 1464, 1388, 1313, 1237, 1164, 1092, 1023, 956, 891, 828, 768, 710, 655, 601, 550, 501, 455, 410, 368, 328, 291, 256, 223, 192, 164, 137, 114, 92, 73, 56, 41, 28, 18, 10, 5, 1, 0]         # Goal position
dxl_goal_position = [0, 0, 1, 3, 5, 7, 10, 14, 18, 23, 28, 34, 41, 48, 55, 64, 72, 82, 92, 102, 113, 125, 137, 150, 163, 177, 191, 206, 222, 238, 254, 272, 289, 308, 327, 346, 366, 387, 408, 430, 452, 475, 499, 523, 547, 572, 598, 624, 651, 679, 707, 735, 764, 794, 824, 855, 886, 918, 951, 984, 1018, 1052, 1087, 1122, 1158, 1194, 1231, 1269, 1306, 1344, 1382, 1419, 1457, 1494, 1532, 1570, 1607, 1645, 1682, 1720, 1758, 1795, 1833, 1870, 1908, 1945, 1983, 2021, 2058, 2096, 2133, 2171, 2209, 2246, 2284, 2321, 2359, 2397, 2434, 2472, 2509, 2547, 2585, 2622, 2660, 2697, 2735, 2773, 2810, 2848, 2885, 2923, 2961, 2998, 3036, 3073, 3111, 3148, 3186, 3224, 3261, 3299, 3336, 3374, 3412, 3449, 3487, 3524, 3562, 3600, 3637, 3675, 3712, 3750, 3787, 3824, 3860, 3896, 3931, 3965, 3999, 4033, 4065, 4098, 4129, 4160, 4191, 4221, 4250, 4279, 4307, 4335, 4362, 4389, 4415, 4440, 4465, 4489, 4513, 4536, 4559, 4581, 4603, 4623, 4644, 4664, 4683, 4701, 4720, 4737, 4754, 4770, 4786, 4802, 4816, 4830, 4844, 4857, 4869, 4881, 4893, 4903, 4913, 4923, 4932, 4941, 4948, 4956, 4963, 4969, 4974, 4980, 4984, 4988, 4991, 4994, 4997, 4998, 4999, 5000, 5000, 4999, 4998, 4997, 4994, 4991, 4988, 4984, 4980, 4974, 4969, 4963, 4956, 4948, 4941, 4932, 4923, 4913, 4903, 4893, 4881, 4869, 4857, 4844, 4830, 4816, 4802, 4786, 4770, 4754, 4737, 4720, 4701, 4683, 4664, 4644, 4623, 4603, 4581, 4559, 4536, 4513, 4489, 4465, 4440, 4415, 4389, 4362, 4335, 4307, 4279, 4250, 4221, 4191, 4160, 4129, 4098, 4065, 4033, 3999, 3965, 3931, 3896, 3860, 3824, 3787, 3750, 3712, 3675, 3637, 3600, 3562, 3524, 3487, 3449, 3412, 3374, 3336, 3299, 3261, 3224, 3186, 3148, 3111, 3073, 3036, 2998, 2961, 2923, 2885, 2848, 2810, 2773, 2735, 2697, 2660, 2622, 2585, 2547, 2509, 2472, 2434, 2397, 2359, 2321, 2284, 2246, 2209, 2171, 2133, 2096, 2058, 2021, 1983, 1945, 1908, 1870, 1833, 1795, 1758, 1720, 1682, 1645, 1607, 1570, 1532, 1494, 1457, 1419, 1382, 1344, 1306, 1269, 1231, 1194, 1158, 1122, 1087, 1052, 1018, 984, 951, 918, 886, 855, 824, 794, 764, 735, 707, 679, 651, 624, 598, 572, 547, 523, 499, 475, 452, 430, 408, 387, 366, 346, 327, 308, 289, 272, 254, 238, 222, 206, 191, 177, 163, 150, 137, 125, 113, 102, 92, 82, 72, 64, 55, 48, 41, 34, 28, 23, 18, 14, 10, 7, 5, 3, 1, 0, 0]         # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupSyncWrite instance
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# Initialize GroupSyncRead instace for Present Position
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

for i in range(0, len(DXL_ID)):
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[i], ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL_ID[i])

    # Enable trajectory profile
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[i], ADDR_DRIVE_MODE, PROFILE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Write start position point
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID[i], ADDR_GOAL_POSITION, dxl_goal_position[0])
    
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID[i], ADDR_PRESENT_POSITION)
        dxl_present_position = struct.unpack('i', struct.pack('I', dxl_present_position))[0];
        
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[i], dxl_goal_position[0], dxl_present_position))

        if not abs(dxl_goal_position[0] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break    

    # Disable trajectory profile
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[i], ADDR_DRIVE_MODE, PROFILE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))        
    
    # Add parameter storage for Dynamixel present position value
    dxl_addparam_result = groupSyncRead.addParam(DXL_ID[i])
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncRead addparam failed" % DXL_ID[i])
        quit()

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    for index in range(0, len(dxl_goal_position)):
        # Allocate goal position value into byte array
        param_goal_position = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position[index]))]

        for i in range(0, len(DXL_ID)):
            # Add Dynamixel goal position value to the Syncwrite parameter storage
            dxl_addparam_result = groupSyncWrite.addParam(DXL_ID[i], param_goal_position)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % DXL_ID[i])
                quit()

        # Syncwrite goal position
        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Clear syncwrite parameter storage
        groupSyncWrite.clearParam()

        # Wait for movement to goal position
        time.sleep(0.01)

# Clear syncread parameter storage
groupSyncRead.clearParam()

for i in range(0, len(DXL_ID)):
    # Enable trajectory profile
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[i], ADDR_DRIVE_MODE, PROFILE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Write home position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID[i], ADDR_GOAL_POSITION, 0)
    
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID[i], ADDR_PRESENT_POSITION)
        dxl_present_position = struct.unpack('i', struct.pack('I', dxl_present_position))[0];
        
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[i], 0, dxl_present_position))

        if not abs(0 - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break    
        
    # Disable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID[i], ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
