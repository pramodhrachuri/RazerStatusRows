#!/usr/bin/python3
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import math
import numpy as np
import time
from colour import Color
import psutil

DEBUG = True

if DEBUG:
    import matplotlib.pyplot as plt

device_manager = DeviceManager()

print("Found {} Razer devices".format(len(device_manager.devices)))

devices = device_manager.devices
for device in list(devices):
    if not device.fx.advanced:
        print("Skipping device " + device.name + " (" + device.serial + ")")
        devices.remove(device)

device_manager.sync_effects = False

device = devices [0]

rows = device.fx.advanced.rows
cols = device.fx.advanced.cols

row_size = [15, 14, 14, 14, 14, 14]

color_gradiant = list(Color("orange").range_to(Color("red"),row_size[1]+1))
color_gradiant = list([list(np.array(x.get_rgb())*255) for x in color_gradiant])

batter_level = 0
temperature  = 0

charging_animation_status = 0

while 1:
    batter_level = psutil.sensors_battery().percent/100
    temperature = np.max([x[0].current for x in np.array(list(psutil.sensors_temperatures().values())).reshape(-1)])/100
    with open("/sys/class/power_supply/AC0/online") as f:
        charging_status = int(f.read())

    row_limit = [0]*len(row_size)
    row_limit[0]  = np.clip(math.ceil(batter_level*row_size[0]),1,None)
    row_limit[1]  = np.clip(math.ceil(temperature*row_size[1]) ,1,None)

    # everything black
    rgbs_matrix = np.array([[(0 ,0 ,0 ) for i in range(cols)] for i in range(rows)])

    # white as default
    rgbs_matrix[0,:] = [255,255,255]
    rgbs_matrix[1,:] = [255,255,255]
    rgbs_matrix[2,:] = [255,255,255]
    rgbs_matrix[3,:] = [255,255,255]
    rgbs_matrix[4,:] = [255,255,255]
    rgbs_matrix[5,:] = [255,255,255]

    # green/red as data
    rgbs_matrix[0,1:row_limit[0]+1] = ([0,255,0] if batter_level>=0.69 else ([255,0,0] if batter_level<=0.30 else [0,0,255]))

    if charging_status:
        rgbs_matrix[0][charging_animation_status] = ([0,0,255] if batter_level>=0.69 else [0,255,0])

        charging_animation_status += 1
        if charging_animation_status >= cols:
            charging_animation_status = 0

    # gradiant as data
    rgbs_matrix[1,:row_limit[1]+1] = color_gradiant[:row_limit[1]+1]


    device.fx.advanced.matrix.reset()  
    for i in range(rows):
        for j in range(cols):
            device.fx.advanced.matrix[i, j] = list(rgbs_matrix[i,j])

    device.fx.advanced.draw()

    time.sleep(0.5)