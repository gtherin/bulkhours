import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time

"""
sudo ufw allow 8678
cd /home/ubuntu/bulkhours && streamlit run evaluate.py --server.address appv26.bulkhours.fr --server.port 8678
cd /home/ubuntu/bulkhours && streamlit run evaluate.py --server.address 0.0.0.0 --server.port 8678
"""

st.set_page_config(page_title="Multi-Capture for ChatGPT", layout="centered")
st.title("📸 Take Multiple Photos for ChatGPT")

st.markdown("""
Use your webcam to capture several images. Once you're done, you can send them to ChatGPT for analysis.
""")

# Session state to store photos
if 'photos' not in st.session_state:
    st.session_state['photos'] = []

# Camera input
img_file = st.camera_input("Take a photo")

if img_file is not None:
    image = Image.open(img_file)
    st.session_state['photos'].append(image)
    st.success(f"Photo #{len(st.session_state['photos'])} saved!")

# Display saved images
if st.session_state['photos']:
    st.subheader("📷 Captured Photos")
    for i, img in enumerate(st.session_state['photos']):
        st.image(img, caption=f"Photo #{i+1}", use_column_width=True)

    # Button to clear
    if st.button("🗑️ Clear all photos"):
        st.session_state['photos'] = []
        st.experimental_rerun()

    # Button to prepare for ChatGPT
    if st.button("✅ Prepare for ChatGPT"):
        st.subheader("Ready to upload to ChatGPT!")
        for i, img in enumerate(st.session_state['photos']):
            st.download_button(
                label=f"Download Photo #{i+1}",
                data=img,
                file_name=f"photo_{i+1}.png",
                mime="image/png"
            )
        st.markdown("➡️ Now you can upload these images to ChatGPT for further analysis.")
else:
    st.info("Take at least one photo to get started.")
