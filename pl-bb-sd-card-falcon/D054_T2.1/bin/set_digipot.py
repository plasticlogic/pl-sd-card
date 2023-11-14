#!/usr/bin/env python
# python script to read/write a float value to an i2c nvm

import sys
import os.path
import argparse
import subprocess
import smbus
import time
import struct

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Python script set digipot value.")
	parser.add_argument("-d", help="Digipot Device: pos, neg.")
	parser.add_argument("-va", help="Value in Hex.")
	parser.add_argument("-v", action='store_true', help="Verbose: Prints additional messages.")
	parser.add_argument("-w", default=1, type=float, help="Wait time in ms.")

	args = parser.parse_args()
	device = args.d
	targetValue = int(args.va)
	v = args.v
	wait = args.w
	
	try:	
		if(v):
			print (sys.version)
			print ('Start ...')
			print (targetValue)
			
		#bus = smbus.SMBus(1)		
		
		if (device == "pos"):
		
			f = open('/tmp/digipot_pos_value.txt', 'a+');
			f.seek(0);
			strCurrentValue = f.read()
			
			if(strCurrentValue == ""):
				strCurrentValue = "0"
			
			currentValue = int(strCurrentValue, 0)
			
			while (currentValue <> targetValue):
			
				if (currentValue < targetValue):
					currentValue = currentValue + 1
					
				if (currentValue > targetValue):
					currentValue = currentValue - 1
					
				#bus.write_byte_data(0x3d, 0x00, currentValue)
				subprocess.check_call(["epdc-app", "-write_i2c", "0x3d", "0x00", str(currentValue)])
				
				if(v):
					print(currentValue)
					
				time.sleep(wait/1000)						
			
			open('/tmp/digipot_pos_value.txt', 'w').write(str(currentValue))
			
		elif (device == "neg"):
		
			f = open('/tmp/digipot_neg_value.txt', 'a+');
			f.seek(0);
			strCurrentValue = f.read()
			
			if(strCurrentValue == ""):
				strCurrentValue = "0"
			
			currentValue = int(strCurrentValue, 0)
			
			while (currentValue <> targetValue):
			
				if (currentValue < targetValue):
					currentValue = currentValue + 1
					
				if (currentValue > targetValue):
					currentValue = currentValue - 1
					
				#bus.write_byte_data(0x3c, 0x00, currentValue)
				subprocess.check_call(["epdc-app", "-write_i2c", "0x3c", "0x00", str(currentValue)])
				
				if(v):
					print(currentValue)
					
				time.sleep(wait/1000)						
			
			open('/tmp/digipot_neg_value.txt', 'w').write(str(currentValue))
		
		else:				
			print("No or wrong digipot specified!")
			
		if(v):
			print("...finished")
		
	except Exception as e:
		print("Exception: {}".format(e))
		sys.exit(1)
			
	sys.exit(0)