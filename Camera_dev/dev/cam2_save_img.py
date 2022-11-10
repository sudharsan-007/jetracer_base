import cv2
import numpy as np
import os
import time
import multiprocessing
import pandas as pd
import random

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,  # 640, 960
    capture_height=720, # 480, 720
    display_width=960,  
    display_height=540,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


image_dir_path = "./data/img"
data_dir_path = "./data"

def dir_check(image_dir_path):
    # checking if  images dir is exist not, if not then create images directory
    CHECK_DIR = os.path.isdir(image_dir_path)
    if not CHECK_DIR:
        os.makedirs(image_dir_path)
        print(f'"{image_dir_path}" Directory is created')
    else:
        print(f'"{image_dir_path}" Directory already Exists.')

def record_img():
    # define a video capture object
    vid = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    # vid = cv2.VideoCapture(0) 
    
    dir_check(image_dir_path)
    
    pd.DataFrame({},columns=["Epoch_time","Throttle","Steering"]).to_csv(f"{data_dir_path}/data.csv")
    
    print('started p1 success')
    prev_time = int(time.time())
    while True:
        ret, frame = vid.read()
        copyFrame = frame.copy()
        cv2.imshow('frame', frame)       
        curr_time = int(time.time())
        if curr_time-prev_time==1:
            cv2.imwrite(f"{image_dir_path}/{int(time.time())}.jpg", copyFrame)
            print("img_saved {}".format(copyFrame.shape))
            
            data = {
                'Epoch_time': [curr_time],
                'Throttle': [random.random()],
                'Steering': [random.random()],
            }
            
            # Make data frame of above data
            df = pd.DataFrame(data)
            
            # append data frame to CSV file
            df.to_csv(f"{data_dir_path}/data.csv", mode='a', index=False, header=False)
            
            prev_time = int(time.time())
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            vid.release()
            cv2.destroyAllWindows()
    
def print_random():
    print("started p2 success")
    while True:
        print(str(time.time()))
        time.sleep(1)
    
  
# while(True):
      
p1 = multiprocessing.Process(target=record_img,args=[])
p2 = multiprocessing.Process(target=print_random,args=[])
    
if __name__=="__main__":
    

        
    p1.start()      
    p2.start()