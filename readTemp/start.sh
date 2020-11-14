#echo log this > /home/pi/water/readTemp/readTemp.log
#source /home/pi/water/readTemp/env/bin/activate
echo before pip > /home/pi/waterRecirculation/readTemp/readTemp.log
#pip3 install -r /home/pi/water/readTemp/requirements.txt >> /home/pi/water/readTemp/readTemp.log 2>&1
#pip3 list >> /home/pi/water/readTemp/readTemp.log 2>&1
python3 /home/pi/waterRecirculation/readTemp/readTemp.py >> /home/pi/waterRecirculation/readTemp/readTemp.log 2>&1 &
