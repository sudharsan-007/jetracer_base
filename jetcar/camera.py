import cv2
import os
import time
import pandas as pd

import multiprocessing

import matplotlib.pyplot as plt
# from Racestick import RaceStick

# controls = RaceStick()

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,  
    capture_height=720, 
    display_width=640,  
    display_height=480,
    framerate=30,
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

def dir_check(image_dir_path = "./data/img"):
    # checking if  images dir is exist not, if not then create images directory
    CHECK_DIR = os.path.isdir(image_dir_path)
    if not CHECK_DIR:
        os.makedirs(image_dir_path)
        print(f'"{image_dir_path}" Directory is created')
    else:
        print(f'"{image_dir_path}" Directory already Exists.')

def record_img(throttle, steering):
    # define a video capture object
    vid = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    # vid = cv2.VideoCapture(0) 
    
    dir_check()
    
    pd.DataFrame({},columns=["Epoch_time","Throttle","Steering"]).to_csv(f"{data_dir_path}/data.csv")
    
    print('started p1 success')
    prev_time = int(time.time())
    while True:
        ret, frame = vid.read()
        copyFrame = frame.copy()
        # cv2.imshow('frame', frame)       
        curr_time = int(time.time())
        if curr_time-prev_time==1:
            
            # throttle, steering, steeringoffset = controls.GetThrottleSteering()

            data = {
                'Epoch_time': [curr_time],
                'Throttle': [throttle],
                'Steering': [steering],
            }
            
            cv2.imwrite(f"{image_dir_path}/{int(time.time())}.jpg", copyFrame)
            print("img_saved {}".format(copyFrame.shape))
            
            # Make data frame of above data
            df = pd.DataFrame(data)
            
            # append data frame to CSV file
            df.to_csv(f"{data_dir_path}/data.csv", mode='a', index=False, header=False)
            
            prev_time = int(time.time())
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            vid.release()
            cv2.destroyAllWindows()
            
class Camera():
    
    def __init__(self):
        self.vid = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        
        self.image_dir_path = "./data/img"
        self.data_dir_path = "./data"
        
        self.check_dir()
        
        if not os.path.isfile(os.path.join(self.data_dir_path,"data.csv")):
            pd.DataFrame({},columns=["Epoch_time","Throttle","Steering"]).to_csv(f"{self.data_dir_path}/data.csv")
            print("No previous data found, creating new file")
        
        print("Camera initialised ")
        
    def return_frame(self):
        ret, frame = self.vid.read()
        copy_frame = frame.copy()
        return copy_frame, ret
    
    def check_dir(self):
        # checking if  images dir is exist not, if not then create images directory
        CHECK_DIR = os.path.isdir(self.image_dir_path)
        if not CHECK_DIR:
            os.makedirs(self.image_dir_path)
            print(f'"{self.image_dir_path}" Directory is created')
        else:
            print(f'"{self.image_dir_path}" Directory already Exists.')
            
    def record_data(self, curr_time, throttle, steering):
        data = {
                'Epoch_time': [str(curr_time)],
                'Throttle': [str(throttle)],
                'Steering': [str(steering)],
            }
        df = pd.DataFrame(data)
        df.to_csv(f"{self.data_dir_path}/data.csv", mode='a', index=False, header=False)
        
    def save_img_data(self, frame, fname):
        # fname = str(round(time.time())).replace(".","_")
        cv2.imwrite(f"{self.image_dir_path}/{fname}.png", frame)
        
    

def data_collect_mode():
    cam = Camera()
    interval = 1.0
    prev_time = time.time()
    while True:
        if time.time() - prev_time >= interval:
            prev_time = time.time()
            frame, ret = cam.return_frame()
            if interval >= 1:
                cam.record_data(str(int(time.time())), "throttle", "steering")
            else:
                cam.record_data(str(round(time.time())).replace(".","_"), "throttle", "steering")
            cam.save_img_data(frame)
            
            
            print("I am running")
        
        


    
if __name__=="__main__":
    # p1 = multiprocessing.Process(target = data_collect_mode)
    # p1.start()
    # time.sleep(2)
    # print("I slept for 2 seconds while camera was on")
    # time.sleep(2)
    # print("slept again")
    # p1.terminate()
    # print("stopped camera")
    
    
    # cam = Camera()
    # frame, ret = cam.return_frame()
    # print(frame.shape)
    # time.sleep(1)
    # frame2, _ = cam.return_frame()
    # print(frame2)

    record_img("asf", "daf")
    
    