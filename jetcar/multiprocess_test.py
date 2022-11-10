# !/usr/bin/env python3.6
# coding: utf-8

# Python imports
import time
import multiprocessing

# Imports
from Racestick import RaceStick
from nvidia_racecar import NvidiaRacecar
from camera import Camera
# from camera import record_img, dir_check


# Initializing the car
car = NvidiaRacecar()
controls = RaceStick()
cam = Camera()

throttle = 0.0
steering = 0.0
steeringOffset = 0.0
mode = "Not Init"


def autonomous_mode():
    pass


def telemetry_mode():
    global throttle, steering, steeringoffset
    throttle, steering, steeringoffset = controls.GetThrottleSteering()
    car.steering_offset = steeringoffset
    car.RunCar(throttle, steering)


def data_collect_mode():
    interval = 1
    prev_time = time.time()
    while True:
        if time.time() - prev_time >= interval:
            prev_time = time.time()
            frame, ret = cam.return_frame()
            print(frame.shape)
            if interval >= 1:
                fname = str(int(time.time()))
                cam.record_data(fname, throttle, steering)
            if interval < 1:
                fname = str(round(time.time())).replace(".","_")
                cam.record_data(fname, throttle, steering)
            cam.save_img_data(frame, fname)
            
            
            print("I am running")
            
            
    

def training_mode():
    pass




if __name__=="__main__":
    
    # dir_check(image_dir_path)

    remoteControl, collectDataState, trainingState, autonomousState, forceStop = controls.GetDriveState()
    prevCollectState = collectDataState
    
    while not forceStop:
        
        # time.sleep(0.2)
        remoteControl, collectDataState, trainingState, autonomous, forceStop = controls.GetDriveState()
        
        if remoteControl == True:
            telemetry_mode()


        if collectDataState == True and collectDataState != prevCollectState:
            print("collecting data now")
            data_collection_process = multiprocessing.Process(target=data_collect_mode)
            data_collection_process.start()
            prevCollectState = collectDataState
            
        if collectDataState == False and collectDataState != prevCollectState:
            print("stopping data collection")
            data_collection_process.terminate()
            prevCollectState = collectDataState
        
        if forceStop == True:
            print("Force Stopping")
            break
            
        
            
        
            
            

        print(remoteControl, collectDataState, trainingState, autonomous, forceStop, throttle, steering)
        
    print("force stopped")
