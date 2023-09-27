

bash /home/pi/bulkhours/gtherin/bots/cars/run.sh

git clone https://github.com/gtherin/bulkhours

git clone https://github.com/gtherin/ezb-pi ezb-pi.tmp && rm -rf ezb-pi/.git
mv ezb-pi.tmp/.git ezb-pi/ && mv ezb-pi.tmp/.gitignore ezb-pi/ && rm -rf ezb-pi.tmp

git clone https://github.com/gtherin/x-sense-hat sensor_hat.tmp && rm -rf sensor_hat/.git
mv sensor_hat.tmp/.git sensor_hat/ && mv sensor_hat.tmp/.gitignore sensor_hat/ && rm -rf sensor_hat.tmp

git config --global user.email "contact@bulkhours.eu" && git config --global user.name "bulkhours.eu"


picar-x

# Image processings

- **Face recognition**
 - face_reco_knn.py
 - face_reco.py
 - https://github.com/ageitgey/face_recognition


- **Object detection refs**
 - object_detection.py
 - https://www.youtube.com/watch?v=HXDD7-EnGBY
 - https://huggingface.co/docs/transformers/tasks/object_detection
 - https://github.com/murtazahassan/OpenCV-Python-Tutorials-and-Projects

- **Object classifications**
 - https://huggingface.co/models?pipeline_tag=image-classification&sort=downloads
 - https://huggingface.co/nateraw/vit-age-classifier

- **Image 2 image**
 - https://platform.stability.ai/

- **Text 2 speech**
 - Turtoise-tts: https://medium.com/@gpj/making-your-ai-sound-like-you-a-guide-to-creating-custom-text-to-speech-8b595d5cf259  (too slow for raspy)
 - Turtoise-tts: https://www.youtube.com/watch?v=Ci8NaeFCUz4 (too slow for raspy)
 - Use windows audacity to record sound
 - Piper-tts https://www.youtube.com/watch?v=rjq5eZoWWSo (fast)
 - https://colab.research.google.com/drive/1Ymy1FD9Q21N08Dgfclr5WuB8W2DNIb2o#scrollTo=X4zbSjXg2J3N

# Picar-x

Actual calibration values

|Servo|Bias|
---
|Steer |7|
|Pan |-2|
|Tilt |8|


sudo service ezblock stop

tail -f /opt/ezblock/log

http://192.168.1.122:9000/mjpg
http://192.168.1.122:9000/mjpg


https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_start/install_all_modules.html


"""
wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
tar -zxvf Python-3.10.12.tgz Python-3.10.12/
cd Python-3.10.12
./configure --enable-optimizations

pip3 install transformers
"""



## Install robot-hat

```bash
cd /home/pi/
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install
```

## Install vilib

```bash
cd /home/pi/
git clone https://github.com/sunfounder/vilib.git
cd vilib
sudo python3 install.py

pip3 install streamlit==0.62.0
pip3 install matplotlib

http://192.168.0.44:9000/mjpg
```


## Install picar-x

```bash
cd /home/pi/
git clone -b v2.0 https://github.com/sunfounder/picar-x.git
cd picar-x
sudo python3 setup.py install

cd /home/pi/picar-x
sudo bash i2samp.sh
```



## Configure camera

```bash
sudo raspi-config
```
