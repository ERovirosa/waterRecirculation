echo before pip > /home/pi/waterRecirculation/pump/pump.log
pip3 install -r /home/pi/waterRecirculation/pump/requirements.txt >> /home/pi/waterRecirculation/pump/pump.log 2>&1
#pip3 list >> /home/pi/waterRecirculation/pump/pump.log 2>&1
python3 /home/pi/waterRecirculation/pump/pump.py >> /home/pi/waterRecirculation/pump/pump.log 2>&1 &
