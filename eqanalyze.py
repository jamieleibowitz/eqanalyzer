# A script for taking an mp3 file or wav file and
# plotting the song's normalized eq spectrum, along
# with upper and lower bounds. Ultimately the goal
# is to compare two files for the purpose of mixing
# and mastering audio using reference tracks

import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftp
import scipy.signal as sgnl
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import sys

# tkinter used to allow user to navigate their own file structure to find a sound file
root = tk.Tk()
root.withdraw()

file1 = filedialog.askopenfilename(filetypes = (("mp3 files", "*.mp3"),("wav files", "*.wav")))

# ensuring that the selected file type is opened correctly, then opening the file 
# or exiting the program if no file was selected
if not file1:
    sys.exit()
elif file1.lower().endswith('.mp3'):
    song1 = AudioSegment.from_file(file1, format="mp3")
elif file1.lower().endswith('.wav'):
    song1 = AudioSegment.from_file(file1, format="wav")
else:
    print("Error: cannot open file of selected file type. Please select an mp3 or wav file")

# the entire sound file is stored into an array
f_s = song1.frame_rate
song1Data = song1.get_array_of_samples()
freqs = fftp.fftfreq(len(song1Data)) * f_s
song1ft = fftp.fft(song1Data)

plt.semilogx(freqs, np.log10(np.abs(song1ft))-6)
plt.show()