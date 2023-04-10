'''
Can plot EMG data in 2 different ways
change DRAW_LINES to try each.
Press Ctrl + C in the terminal to exit 
'''
import numpy
import pygame
import time
from pygame.locals import *
import multiprocessing
import keyboard
import numpy as np
import scipy.signal as sig
import tensorflow as tf

from pyomyo import Myo, emg_mode



# ------------ Myo Setup ---------------
q = multiprocessing.Queue()

# def signal_filter(emg_signal):
# 	# Step 1: Filter the signal
# 	# High-pass filter to remove baseline noise
# 	fs = 1000  # Sampling frequency in Hz
# 	cutoff_freq = 20  # Cutoff frequency for high-pass filter in Hz
# 	b, a = sig.butter(4, cutoff_freq / (fs / 2), 'highpass')
# 	emg_signal_filtered = sig.filtfilt(b, a, emg_signal)
#
# 	# Low-pass filter to remove high-frequency noise
# 	cutoff_freq = 500  # Cutoff frequency for low-pass filter in Hz
# 	b, a = sig.butter(4, cutoff_freq / (fs / 2), 'lowpass')
# 	emg_signal_filtered = sig.filtfilt(b, a, emg_signal_filtered)
#
# 	# Step 2: Rectify the signal
# 	emg_signal_rectified = np.abs(emg_signal_filtered)
#
# 	# Step 3: Smooth the signal
# 	window_size = 0.1  # Window size for smoothing in seconds
# 	window_length = int(window_size * fs)
# 	emg_signal_smoothed = sig.savgol_filter(emg_signal_rectified, window_length, 2)


def worker(q):
	m = Myo(mode=emg_mode.RAW)
	m.connect()
	
	def add_to_queue(emg, movement):
		q.put(emg)

	m.add_emg_handler(add_to_queue)
	
	def print_battery(bat):
		print("Battery level:", bat)

	m.add_battery_handler(print_battery)

	 # Orange logo and bar LEDs
	m.set_leds([128, 0, 0], [128, 0, 0])
	# Vibrate to know we connected okay
	m.vibrate(1)
	
	"""worker function"""
	while True:
		m.run()
	print("Worker Stopped")

last_vals = None
def plot(scr, vals):
	DRAW_LINES = True
	# font = pygame.font.Font(None, 36)
	global last_vals
	if last_vals is None:
		last_vals = vals
		return

	D = 5
	scr.scroll(-D)
	scr.fill((0, 0, 0), (w - D, 0, w, h))
	for i, (u, v) in enumerate(zip(last_vals, vals)):
		if DRAW_LINES:
			pygame.draw.line(scr, (0, 255, 0),
							 (w - D, int(h/9 * (i+1 - u))),
							 (w, int(h/9 * (i+1 - v))))
			pygame.draw.line(scr, (255, 255, 255),
							 (w - D, int(h/9 * (i+1))),
							 (w, int(h/9 * (i+1))))

			# Get current time
			current_time = time.strftime("%H:%M:%S")

			# # Render time text
			# time_text = font.render(current_time, True, (0, 0, 0))
			# time_rect = time_text.get_rect(center=(screen_width / 2, screen_height / 2))
			#
			# # Draw time text on screen
			# screen.blit(time_text, time_rect)
		else:
			c = int(255 * max(0, min(1, v)))
			scr.fill((c, c, c), (w - D, i * h / 8, D, (i + 1) * h / 8 - i * h / 8))

	pygame.display.flip()
	last_vals = vals

# -------- Main Program Loop -----------
if __name__ == "__main__":
	p = multiprocessing.Process(target=worker, args=(q,))
	p.start()

	w, h = 800, 600
	scr = pygame.display.set_mode((w, h))

	running = time.time()



	try:
		while True:
			# Handle pygame events to keep the window responding
			pygame.event.pump()
			# Get the emg data and plot it
			while not(q.empty()):
				end_time = time.time()
				status = 0
				if(status == 0):
					condition = "False"
				else:
					condition = "True"
				if(running-running>10.0 and running-end_time<20.0):
					print("test")
				# buffer = list(q.get())
				emgnew = list()
				# emg = list(q.get())

				for row in range(8):
					emg = list(q.get())
					plot(scr, [e / 500. for e in emg])
					# A for loop for column entries
					emgnew.append(emg)
				new = tf.convert_to_tensor([emgnew])
				shape = tf.shape(new)
				# print(shape)
				model = tf.keras.models.load_model("/home/pc/Downloads/Opal.h5", compile = True)
				prediction = model.predict(new)
				#
				print(prediction)
				# with open('data/test.txt',"a") as f:
				# 	# for x in range(len(emg)):
				# 		current_time = time.time()-running
				# 		conv = current_time * 1000
				# 		conv_to_int = int(conv)
				# 		int_to_float = float(conv_to_int)
				# 		real_float = int_to_float/1000
				# 		f.writelines("%s\n" % str(emgnew)+str(real_float))

	except KeyboardInterrupt:
		print("Quitting")

		print(end_time -running)
		pygame.quit()
		quit()