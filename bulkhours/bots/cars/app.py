import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import time
from pathlib import Path

from picarx import Picarx as PiCarX
from movement import advance_cm
#from ezblock import Remote
#from Music import *
#from ezblock import TTS
#from ezblock import mapping
from vilib import Vilib


panAngle = None
threadingA = None
Ref1 = None
Ref2 = None
x = None
CONFIG_PATH = Path.home() / ".config" / "picar-x" / "picar-x.conf"
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


@st.cache_resource
def get_px(config_path: str) -> PiCarX:
    # Streamlit reruns the script often; keep a single PiCarX instance
    # to avoid GPIO pin double-allocation errors.
    return PiCarX(config=config_path)


px = get_px(str(CONFIG_PATH))
#tts = TTS()
#tts.lang('fr-FR')

# custom packages (see repo)

# headings
month = datetime.now().month
title = "options-2-trees"
if 1 <= month <= 5:
    st.title(title + " 🌳🌳")
elif 5 < month <= 8:
    st.title(title + " 🌴🌴")
elif 8 < month <= 11:
    st.title(title + " 🌲🌲")
else:
    st.title(title + " 🎄🎄")
st.sidebar.title("Parameters")

if st.button('En avant'):
    st.write('Why hello there')
    for count in range(2):
        #tts.say("Je compte: %s" % str(count))
        px.forward(50)
        time.sleep(1)
        px.stop()
    px.stop()

if st.button('Avancer 10 cm'):
    st.write('Avance de 10 cm')
    advance_cm(px, distance_cm=10.0, speed=50, cm_per_sec=20.0)

if st.button('En arriere'):
    st.write('Why hello there')
    for count in range(2):
        #tts.say("Je compte: %s" % str(count))
        px.forward(-50)
        time.sleep(1)
        px.stop()
    px.stop()

if st.checkbox('Start camera'):
    Vilib.camera_start(True)


#import streamlit.components.v1 as components
# embed streamlit docs in a streamlit app
#components.iframe("https://docs.streamlit.io/en/latest")
