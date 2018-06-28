#!/usr/bin/python

import logging
import threading
import bluetoothHandler
import subprocess
import Queue


class PingThread(threading.Thread):
	def __init__(self, mac_address, queue):
		threading.Thread.__init__(self)
		self.mac_address = mac_address
		self.queue = queue
		self.arrived = False
		
	def run(self):
		self.bt = bluetoothHandler.bluetoothHandler()
		self.bt.start(self.mac_address)

		self.is_running = True

		while self.is_running:
			self.rssi, self.ping = self.bt.rssi()

			if self.rssi is not None:
				if self.rssi == "OOR":
					if self.arrived:
						self.arrived = False
						self.queue.put([self.mac_address, self.arrived])
				else:	
					if not self.arrived:
						print "CIAO ", self.mac_address
						self.arrived = True
						self.queue.put([self.mac_address, self.arrived])
				

	def stop(self):
		self.is_running = False

	
