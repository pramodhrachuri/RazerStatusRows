#!/usr/bin/python3
from openrazer.client import DeviceManager, constants as razer_constants
import math
import numpy as np
import time
from colour import Color
import psutil

# Constants and Configurations
DEBUG = True
BATTERY_HIGH_THRESHOLD = 0.69
BATTERY_LOW_THRESHOLD = 1-BATTERY_HIGH_THRESHOLD
SLEEP_INTERVAL = 0.5

# Initialize Device Manager
device_manager = DeviceManager()
devices = device_manager.devices

if DEBUG:
    import matplotlib.pyplot as plt

def find_advanced_devices(device_list):
    advanced_devices = []
    for device in device_list.copy():
        if not device.fx.advanced:
            print(f"Skipping device {device.name} ({device.serial})")
            device_list.remove(device)
        else:
            advanced_devices.append(device)
    return advanced_devices

def create_gradient_colors(start_color, end_color, num_steps):
    gradient = list(Color(start_color).range_to(Color(end_color), num_steps + 1))
    return [list(np.array(x.get_rgb()) * 255) for x in gradient]

def main():
    advanced_devices = find_advanced_devices(devices)
    
    if not advanced_devices:
        print("No advanced devices found.")
        return
    
    device = advanced_devices[0]
    rows = device.fx.advanced.rows
    cols = device.fx.advanced.cols
    row_sizes = [15, 14, 14, 14, 14, 14]
    
    color_gradient = create_gradient_colors("orange", "red", row_sizes[1] + 1)
    
    charging_animation_status = 0
    
    while True:
        battery_level = psutil.sensors_battery().percent / 100
        temperature = np.max([x[0].current for x in np.array(list(psutil.sensors_temperatures().values())).reshape(-1)]) / 100
        
        with open("/sys/class/power_supply/AC0/online") as f:
            charging_status = int(f.read())
        
        row_limits = [0] * len(row_sizes)
        row_limits[0] = np.clip(math.ceil(battery_level * row_sizes[0]), 1, None)
        row_limits[1] = np.clip(math.ceil(temperature * row_sizes[1]), 1, None)
        
        # Create an empty RGB matrix
        rgbs_matrix = np.zeros((rows, cols, 3), dtype=int)
        
        # Set default white colors
        rgbs_matrix[0, :] = [255, 255, 255]
        rgbs_matrix[1, :] = [255, 255, 255]
        rgbs_matrix[2, :] = [255, 255, 255]
        rgbs_matrix[3, :] = [255, 255, 255]
        rgbs_matrix[4, :] = [255, 255, 255]
        rgbs_matrix[5, :] = [255, 255, 255]
        
        # Set green/red for battery level
        rgbs_matrix[0, 1:row_limits[0] + 1] = ([0,255,0] if battery_level>=BATTERY_HIGH_THRESHOLD else ([255,0,0] if battery_level<=BATTERY_LOW_THRESHOLD else [0,0,255]))


        if charging_status:
            rgbs_matrix[0, charging_animation_status] = [0, 0, 255] if battery_level >= BATTERY_HIGH_THRESHOLD else [0, 255, 0]
            charging_animation_status = (charging_animation_status + 1) % cols
        
        
        # Set gradient for temperature
        rgbs_matrix[1, :row_limits[1] + 1] = color_gradient[:row_limits[1] + 1]
        
        device.fx.advanced.matrix.reset()
        for i in range(rows):
            for j in range(cols):
                device.fx.advanced.matrix[i, j] = list(rgbs_matrix[i, j])
        
        device.fx.advanced.draw()
        
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    print(f"Found {len(devices)} Razer devices")
    main()
