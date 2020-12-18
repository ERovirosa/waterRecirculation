#echo log this > /home/pi/waterRecirculation/sensor/readTemp.log
#source /home/pi/water/sensorRecirculation/env/bin/activate
echo before pip > /home/pi/waterRecirculation/sensor/readTemp.log
#pip3 install -r /home/pi/waterRecirculation/sensor/requirements.txt >> /home/pi/waterRecirculation/sensor/readTemp.log 2>&1
#pip3 list >> /home/pi/waterRecirculation/sensor/readTemp.log 2>&1
python3 /home/pi/waterRecirculation/sensor/readTemp.py >> /home/pi/waterRecirculation/sensor/readTemp.log 2>&1 &
