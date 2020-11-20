from flask import Flask, render_template, redirect
import constants

import os
import glob
import time
import threading
import sys
from signal import signal, SIGINT
import atexit

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
masterT =  0

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def sync_temp():
	try:
		global masterT
		while True:
			masterT = read_temp()
			time.sleep(1)
	except:
		print("Error occured closing background sync_Temp thread")
		sys.exit(0)

#def sigHandler(signal_received, frame):
def sigHandler():
        print("Closing the master Bedroom sensor")
        sys.exit(0)

app = Flask(__name__)

@app.route('/temp')
def outputTemp():
	print(masterT)
	return str(masterT)

def main():
	pump_thread = threading.Thread(target=sync_temp, daemon=True)
	pump_thread.start()
	app.run(host = '0.0.0.0', port=constants.port, debug=True)

if __name__ == "__main__":
	#signal(SIGINT, sigHandler)
	atexit.register(sigHandler)
	main()
