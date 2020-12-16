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

"""
class pump:
	def __init__(self, running):
		self.running = running
	def pumpOn(self):
		bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
		bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
		bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
		bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)
		print("pump turned on")
		self.running = 1
	def pumpOff():
		bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
		bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
		bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
		bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
		print("pump turned off")
		self.running = 0


#pump = pump(0)
"""

def pumpOn():
	bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
	bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
	bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)
	bus.write_byte_data(DEVICE_ADDR, 4, 0xFF)
	print("pump turned on")

def pumpOff():
	bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
	bus.write_byte_data(DEVICE_ADDR, 2, 0x00)
	bus.write_byte_data(DEVICE_ADDR, 3, 0x00)
	bus.write_byte_data(DEVICE_ADDR, 4, 0x00)
	print("pump turned off")

#def sigHandler(signal_received, frame):
def sigHandler():
	print("Pump turned off and exiting program")
	pumpOff()
	sys.exit(0)

shutdown = 0

def warmWater(address, threshold):
	try:
		while (True):
			global shutdown
			pumpOn()
			time.sleep(1)
			temp = float(requests.get(address).content)
			print(temp)
			if (temp > threshold) or (shutdown == 1):
				break
	except:
		print("Error occured when trying to warm Master Bathroom water")
	finally:
		if (shutdown==0):
			print("temperature reached")
			time.sleep(300)
		pumpOff()
		print("Pump Off")
	return

app = Flask(__name__)

@app.route('/Temp')
def getTemp():
	try:
		masterT = float(requests.get("http://192.168.0.152:8080/temp").content)
	except:
		masterT =  "Sensor Unavailable"
	print (masterT)
	try:
		guestT = float(requests.get("http://192.168.0.114:8080/temp").content)
	except:
		guestT = "Sensor Unavailable"
	print (guestT)
	return render_template("water.html", masterT=masterT, guestT=guestT)

@app.route('/warmMaster')
def warmMaster():
	print("Master bath set to warm")
	pump_thread = threading.Thread(target=warmWater, daemon=True, args=("http://192.168.0.152:8080/temp", 85))
	pump_thread.start()
	return redirect('/Temp')

@app.route('/warmGuest')
def warmGuest():
        print("Guest bath set to warm")
        pump_thread = threading.Thread(target=warmWater, daemon=True, args=("http://192.168.0.114:8080/temp", 80))
        pump_thread.start()
        return redirect('/Temp')
@app.route('/shutdown')
def shutdown():
	global shutdown
	shutdown = 1
	time.sleep(3)
	shutdown = 0
	return("Pump shut off")

def main():
	app.run(host = '0.0.0.0', port=constants.port, debug=True)

if __name__ == "__main__":
	#signal(SIGINT, sigHandler)
	atexit.register(sigHandler)
	main()
