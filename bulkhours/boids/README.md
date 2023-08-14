
# Launch boids program

```bash
bulkhours-boids
```

# Pica-x

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
