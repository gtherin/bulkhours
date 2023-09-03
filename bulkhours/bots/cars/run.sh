 #bash /home/pi/bulkhours/bulkhours/bots/cars/run.sh

cp -f /home/pi/bulkhours/bulkhours/bots/cars/main.py /opt/ezblock/main_py.py
cp -f /home/pi/bulkhours/bulkhours/bots/cars/app.py /opt/ezblock/streamlit_app.py

# Copy info to the main directory
#cp -f /home/pi/ezb-pi/workspace/*.py /opt/ezblock/*.py 
cp -f /home/pi/ezb-pi/workspace/vilib.py /opt/ezblock/vilib.py 
cp -f /home/pi/ezb-pi/workspace/picarx.py /opt/ezblock/picarx.py 


cd /opt/ezblock/
sudo python3 /opt/ezblock/main_py.py
#/home/pi/.local/bin/streamlit run streamlit_app.py 
