


cp -f /home/pi/bulkhours/bulkhours/bots/cars/main.py /opt/ezblock/main_py.py
cp -f /home/pi/bulkhours/bulkhours/bots/cars/app.py /opt/ezblock/streamlit_app.py

# Copy info to the main directory
# cp -f /home/pi/ezb-pi/workspace/*.py /opt/ezblock/*.py 

cd /opt/ezblock/
sudo python3 /opt/ezblock/main_py.py
#/home/pi/.local/bin/streamlit run streamlit_app.py 
