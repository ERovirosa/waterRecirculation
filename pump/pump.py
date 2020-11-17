import time
import smbus
import sys
import RPi.GPIO as GPIO
from signal import signal, SIGINT
from flask import Flask, request, render_template, redirect
import requests
import threading
import atexit

import constants

DEVICE_ADDR = 0x10
bus = smbus.SMBus(1)

def pumpOn(relay):
	bus.write_byte_data(DEVICE_ADDR, relay, 0xFF)
	print("pump turned on")

def pumpOff(relay):
	bus.write_byte_data(DEVICE_ADDR, relay, 0x00)
	print("pump turned off")

#def sigHandler(signal_received, frame):
def sigHandler():
	print("Pump turned off and exiting program")
	pumpOff(1)
	sys.exit(0)

def warmWater(address):
	try:
		while (True):
			pumpOn(1)
			time.sleep(1)
			masterT = float(requests.get(address).content)
			print(masterT)
			if (masterT > 75):
				break
	except:
		print("Error occured when trying to warm Master Bathroom water")
	finally:
		pumpOff(1)
	return 

app = Flask(__name__)

@app.route('/Temp')
def getTemp():
	masterT = float(requests.get("http://192.168.0.114:8080/temp").content)
	print (masterT)
	#guestT = requests.get("http://123/temp")
	return render_template("water.html", masterT=masterT)

@app.route('/warmMaster')
def warmMaster():
	print("Master bath set to warm")
	pump_thread = threading.Thread(target=warmWater, daemon=True, args=("http://192.168.0.114:8080/temp",))
	pump_thread.start()
	return redirect('/Temp')

def main():
	app.run(host = '0.0.0.0', port=constants.port, debug=True)

if __name__ == "__main__":
	#signal(SIGINT, sigHandler)
	atexit.register(sigHandler)
	main()
