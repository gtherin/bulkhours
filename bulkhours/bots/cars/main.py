#!/usr/bin/python3


import os
os.environ['PICARX_ROGUE_MODE'] = "True"

from Music import *
from ezblock import TTS
from vilib import Vilib
from ezblock import Remote
from picarx import PiCarX
#import picarx
#px = picarx.PiCarX()
from ezblock import mapping
import cv2
import pygame

#os.environ["SDL_VIDEODRIVER"] = "dummy"


panAngle = None
threadingA = None
Ref1 = None
Ref2 = None
x = None

tts = TTS()
tts.lang('fr-FR')



def main():

    music_set_volume(100)
    tts.say('Bienvenue Sylvia')

    Vilib.camera_start(True)
    #picarx.start_px_server()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
          print("YOYO")
    return

    background_music('come_as_you_are.mp3')
    Vilib.human_detect_switch(True)
    Vilib.detect_color_name('blue')
    Ref1 = 30
    Ref2 = 10
    panAngle = 0

    __RM_OBJECT__ = Remote()

    def play_music():
        global panAngle, threadingA, Ref1, Ref2, x
        music_set_volume(__RM_OBJECT__.get_slider_value("A"))

    def move_joystick():
      global panAngle, threadingA, Ref1, Ref2, x
      px.forward(__RM_OBJECT__.get_joystick_value("B", "Y"))
      px.set_steering_angle((mapping(__RM_OBJECT__.get_joystick_value("B", "X"), (-100), 100, (-45), 45)))

    def camera_with_joystick():
      global panAngle, threadingA, Ref1, Ref2, x
      px.set_camera_pan_angle((mapping(__RM_OBJECT__.get_joystick_value("A", "X"), (-100), 100, (-45), 45)))
      px.set_camera_tilt_angle((mapping(__RM_OBJECT__.get_joystick_value("A", "Y"), (-100), 100, (-45), 45)))

    def camera_with_pad():
      global panAngle, threadingA, Ref1, Ref2, x
      if __RM_OBJECT__.get_dpad_value("A", "U") == x:
        panAngle = (panAngle if isinstance(panAngle, int) else 0) + 1
      px.set_camera_pan_angle(panAngle)

    def forever():
      global panAngle, threadingA, Ref1, Ref2, x
      move_joystick()
      camera_with_joystick()
      play_music()
      if __RM_OBJECT__.get_button_value("A") == 1:
        tts.lang('fr-FR')
        tts.say('On se fait un épisode de')
        tts.lang('en-GB')
        tts.say('the last of us ?')

main()