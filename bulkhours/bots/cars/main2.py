#!/usr/bin/python3


import os
import cv2
import pygame

os.environ['PICARX_ROGUE_MODE'] = "True"
os.environ['PICARX_PX_ADDRESS'] = "192.168.1.122"

import Music as music
from vilib import Vilib
import ezblock
import picar
import picappx
px = picappx.px
from sensor_hat.joystick_module import Joystick_Module

jy = Joystick_Module()


def bullfight():
    x_axis = None
    width = None
    pan_angle = None

    if 0:
        px.stop()
        return

    Vilib.detect_color_name('blue')
    Vilib.color_detect_switch(True)
    Vilib.camera_start(True)
    px.set_servo_angle("STEER", 0)
    px.set_servo_angle("TILT", 0)
    px.set_servo_angle("PAN", 0)

    pan_angle = 0

    while True:
        x_axis = Vilib.color_detect_object('x')
        width = Vilib.color_detect_object('width')
        ezblock.delay(5)
        if x_axis == -1:
            pan_angle = pan_angle - 1
            pan_angle = ezblock.constrain(pan_angle, -90, 90)
            px.set_camera_servo1_angle(pan_angle)
            pan_angle = ezblock.constrain(pan_angle, -45, 45)
            px.set_steering_angle(pan_angle)
        elif x_axis == 1:
            pan_angle = pan_angle + 1
            pan_angle = ezblock.constrain(pan_angle, -90, 90)
            px.set_camera_servo1_angle(pan_angle)
            pan_angle = constrain(pan_angle, -45, 45)
            px.set_steering_angle(pan_angle)
        if width > 50:
            px.forward(50)
        else:
            px.stop()


def avoid_obstacles():
    Ref1 = 30
    Ref2 = 10
    while True:
        distance = px.get_distance()
        if distance >= Ref1:
            px.set_steering_angle(0)
            px.forward(50)
        elif distance >= Ref2:
            px.set_steering_angle(40)
            px.forward(50)
            ezblock.delay(500)
        else:
            px.set_steering_angle((-40))
            px.backward(50)
            ezblock.delay(500)




def main():

    px.stop()
    print(Vilib.detect_obj_parameter)

    if 1:
        picappx.start_px_server()

    if 0:
        return

    if 0:
        gs = Grayscale_Module("A0", "A1", "A2")
        while True:
            print(gs.get_grayscale_data())
            ezblock.delay(500)

        #avoid_obstacles()
        #bullfight()
        return

    if 0:
        pin_D0=ezblock.Pin("D0")
        pin_D1=ezblock.Pin("D1")

        distance = ezblock.Ultrasonic(pin_D0, pin_D1).read()
        print("%s"%distance)
        return


    if 1:
        Vilib.camera_start(True)
        Vilib.human_detect_switch(True)
        #Vilib.detect_color_name('red')

    __RM_OBJECT__ = ezblock.Remote()


    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
          print("YOYO")
    print("AAAAAAAAAAAAA")
    return

    Ref1 = 30
    Ref2 = 10
    panAngle = 0

    def move_joystick():
        px.forward(__RM_OBJECT__.get_joystick_value("B", "Y"))
        px.set_steering_angle((ezblock.mapping(__RM_OBJECT__.get_joystick_value("B", "X"), (-100), 100, (-45), 45)))


    def camera_with_joystick():
        px.set_camera_pan_angle((ezblock.mapping(__RM_OBJECT__.get_joystick_value("A", "X"), (-100), 100, (-45), 45)))
        px.set_camera_tilt_angle((ezblock.mapping(__RM_OBJECT__.get_joystick_value("A", "Y"), (-100), 100, (-45), 45)))

    def camera_with_pad():
        if __RM_OBJECT__.get_dpad_value("A", "U") == x:
            panAngle = (panAngle if isinstance(panAngle, int) else 0) + 1
        px.set_camera_pan_angle(panAngle)

        if __RM_OBJECT__.get_button_value("A") == 1:
            tts.lang('en-GB')
            tts.say('Is it cool')