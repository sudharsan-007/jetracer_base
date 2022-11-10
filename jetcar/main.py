# !/usr/bin/env python3.6
# coding: utf-8


import multiprocessing

# Imports
from Racestick import RaceStick
from nvidia_racecar import NvidiaRacecar
from camera import record_img, dir_check

# Initializing the car
car = NvidiaRacecar()
controls = RaceStick()


image_dir_path = "./data/img"

def autonomous_mode():
    pass


def telemetry_mode():
    throttle, steering, steeringoffset = controls.GetThrottleSteering()
    car.RunCar(throttle, steering)


def data_collect_mode():
    record_img()
    

def training_mode():
    pass





      


if __name__=="__main__":
    
    dir_check(image_dir_path)
    
    state, stop = controls.GetDriveState()
    prev_state = None
    
    while not stop:
        
        state, stop = controls.GetDriveState()
        
        
            

        print(state, stop)
        
    print(stop)