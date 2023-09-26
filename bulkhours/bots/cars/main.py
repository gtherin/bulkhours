#!/usr/bin/python3


import os
os.environ['PICARX_ROGUE_MODE'] = "True"
os.environ['PICARX_PX_ADDRESS'] = "192.168.1.122"

import Music as music
from vilib import Vilib
import ezblock


import picar
import picappx
px = picappx.px
import cv2
import pygame
from sensor_hat.joystick_module import Joystick_Module

jy = Joystick_Module()

def main():

    if 0:
        pin_D0=ezblock.Pin("D0")
        pin_D1=ezblock.Pin("D1")

        distance = ezblock.Ultrasonic(pin_D0, pin_D1).read()
        print("%s"%distance)
        return

    if 1:
        picappx.start_px_server()

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

main()