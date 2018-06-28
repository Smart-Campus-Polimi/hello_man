#!/usr/bin/python

import threading
import signal
import time
import sys
import subprocess
import Queue
import os
import PingHandler
import pyglet
import logging

from pyglet.gl import *

logging.basicConfig(filename= 'logging.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


queue = Queue.Queue(10)
threads = []
users = {"44:78:3e:a8:57:a0": {'name': "Alessandro", 'status': False},
		 "d4:63:c6:f0:9e:ce": {'name': "Edoardo", 'status': False},
		 "1C:66:AA:CC:9A:18": {'name': "Tucano", 'status': False},
	 	 "54:B1:21:AD:D1:42": {'name': "Armin", 'status': False}
		 }




def signal_handler(signal, frame):
	print "Exit!"

	#close all the thread in thread list
	for thrd in threads:
		thrd.stop()
	try:
		killall_ping = subprocess.check_output(['killall', '-9', 'l2ping'], stderr=subprocess.PIPE)
	except subprocess.CalledProcessError as e:
		pass

		
	sys.exit(0)

def create_label(my_name, user_num):
	label = pyglet.text.Label('Ciao '+my_name+" :)",
                          font_name='Times New Roman',
                          font_size=36,
                          x=(1024//2), y=(768//2)+user_num,
                          anchor_x='center', anchor_y='center')

	return label


def check_active_users(my_users):
	usr_num = 0
	for key, value in my_users.iteritems():
		if value['status']:
			usr_num += 1


	if usr_num==1:
		return [0]
	elif usr_num==2:
		return [-50, +50]
	elif usr_num==3: 
		return [-100,0,+100]

	else:
		pass

def check_labels(my_users):
	my_text = []

	offset = check_active_users(my_users)

	i = 0
	for key, value in my_users.iteritems():
		if value['status']:
			my_text.append(create_label(value['name'], offset[i]))
			i += 1


	return my_text


class MyWindow(pyglet.window.Window):
		def __init__(self, *args, **kwargs):
			super(MyWindow, self).__init__(*args, **kwargs)
			self.set_minimum_size(400,300)
			glClearColor(0, 0, 0, 0)
			pyglet.clock.schedule_interval(self.update, 7.0/24.0)

			
		def on_draw(self):
			self.clear()
			text = check_labels(users)

			for phrase in text:
				phrase.draw()
			
		
		def update(self, dt):
			if not queue.empty():
				logging.info("receive a message")
				name, new_status = queue.get()
				if not users[name]['status']:
					print "hello ", name
					logging.info("turn on")
					users[name]['status'] = True
				

				elif users[name]['status']:
					users[name]['status'] = False
					print "arrivederci ",  name

				#users[hello[0]] = hello[1]




#### MAIN ####
if __name__ == "__main__":

	logging.info("Start")
	signal.signal(signal.SIGINT, signal_handler)
	window = MyWindow(1024, 768, "test hello", resizable=False, visible=True, fullscreen=True)

	for user in users:
		logging.info("create threads")
		thread = PingHandler.PingThread(user, queue)
		threads.append(thread)
		thread.start()

	pyglet.app.run()


 
