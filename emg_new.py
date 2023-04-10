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

q = multiprocessing.Queue()


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

if __name__ == "__main__":
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    input_list = list()
    for i in range(8):
        emg = list(q.get())
        input_list.append(emg)

    print(input_list)
