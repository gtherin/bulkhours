

pip3 install virtualenv
export PATH=$PATH:/home/pi/.local/bin

virtualenv picarenv
source picarenv/bin/activate

pip3 install transformers

# To avoid noise 
echo "" >> ~/ezb-pi/.gitignore
echo "ezblock/ble_uart/*" >> ~/ezb-pi/.gitignore
echo "*.deb" >> ~/ezb-pi/.gitignore

echo "" >> ~/sensor_hat/.gitignore
echo "build/*" >> ~/sensor_hat/.gitignore
echo "*.egg" >> ~/sensor_hat/.gitignore
echo "*.egg-info" >> ~/sensor_hat/.gitignore
