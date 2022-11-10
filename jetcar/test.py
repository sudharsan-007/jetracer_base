#!/usr/bin/env python
# coding: utf-8

from Racestick import RaceStick

from nvidia_racecar import NvidiaRacecar
# Initializing the car
car = NvidiaRacecar()
controls = RaceStick()



# Joystick events handled in the background
while True:
    throttle, steering, steeringoffset = controls.GetThrottleSteering()
    car.RunCar(throttle, steering)
    
