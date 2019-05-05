# A script for taking an mp3 file or wav file and
# plotting the song's normalized eq spectrum, along
# with upper and lower bounds. Ultimately the goal
# is to compare two files for the purpose of mixing
# and mastering audio using reference tracks

import wave
import numpy
import scipy
import pydub
import tkinter
from tkinter import filedialog

