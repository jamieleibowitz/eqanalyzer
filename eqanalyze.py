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
# for each fft call that stft makes, nps determines how many samples it takes in
nps = 8820
# asize is the size of the resulting arrays from calling stft
asize = nps//2+1
# initializing the array where the overall average of each frequency will be stored
song1avg = np.zeros(asize)
# loops through the song, each stft call will get 2 seconds worth of data
for i in range(0, len(song1Data), 2 * f_s):
    # ensuring that we don't go out of bounds by doubling back to exactly 2*f_s+1 samples before the end
    if i + 2 * f_s >= len(song1Data):
        i = len(song1Data) - 2 * f_s - 1
    # avger calculates the weight of the current stft call against the data stored in song1avg
    avger = 2 * f_s/(i + 2 * f_s)
    # temp stores the latest stft call
    freqs, temp = sgnl.stft(song1Data[i:i+2*f_s], fs = f_s, nperseg=nps)[0:3:2]
    # collapse temp into a 1d array
    temp = np.mean(temp, axis=1)
    # add weights temp and song1avg
    temp = [x * avger for x in temp]
    song1avg = [x * (1-avger) for x in song1avg]
    # sum the values by frequency to get the new average signal strength at each frequency
    song1avg = [sum(x) for x in zip(temp, song1avg)]

# plot the result
plt.semilogx(freqs, np.log10(np.abs(song1avg))-8)
plt.show()