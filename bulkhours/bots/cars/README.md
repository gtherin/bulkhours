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

https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_start/install_all_modules.html

## Update os

```bash
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip python3-setuptools python3-smbus
```

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
