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

def openFile():
    filestring = filedialog.askopenfilename(filetypes = (("mp3 files", "*.mp3"),("wav files", "*.wav")))
    # ensuring that the selected file type is opened correctly, then opening the file 
    # or exiting the program if no file was selected
    if not filestring:
        sys.exit()
    elif filestring.lower().endswith('.mp3'):
        songData = AudioSegment.from_file(filestring, format="mp3")
    elif filestring.lower().endswith('.wav'):
        songData = AudioSegment.from_file(filestring, format="wav")
    else:
        print("Error - File 1: cannot open file of selected file type. Please select an mp3 or wav file")
    return songData

def ftmusic(song):
    # the entire sound file is stored into an array
    f_s = song.frame_rate
    songData = song.get_array_of_samples()
    # for each fft call that stft makes, nps determines how many samples it takes in
    nps = 8820
    # asize is the size of the resulting arrays from calling stft
    asize = nps//2+1
    # initializing the array where the overall average of each frequency will be stored
    songavg = np.zeros(asize)
    # loops through the song, each stft call will get 2 seconds worth of data
    for i in range(0, len(songData), 2 * f_s):
        # ensuring that we don't go out of bounds by doubling back to exactly 2*f_s+1 samples before the end
        if i + 2 * f_s >= len(songData):
            i = len(songData) - 2 * f_s - 1
        # avger calculates the weight of the current stft call against the data stored in songavg
        avger = 2 * f_s/(i + 2 * f_s)
        # temp stores the latest stft call
        freqs, temp = sgnl.stft(songData[i:i+2*f_s], fs = f_s, nperseg=nps)[0:3:2]
        # collapse temp into a 1d array
        temp = np.mean(temp, axis=1)
        # add weights temp and songavg
        temp = [x * avger for x in temp]
        songavg = [x * (1-avger) for x in songavg]
        # sum the values by frequency to get the new average signal strength at each frequency
        songavg = [sum(x) for x in zip(temp, songavg)]
    return freqs, np.log10(np.abs(songavg))

# tkinter used to allow user to navigate their own file structure to find a sound file
root = tk.Tk()
root.withdraw()

song1 = openFile()
song2 = openFile()

freqs1, ftSong1 = ftmusic(song1)
freqs2, ftSong2 = ftmusic(song2)

# plot the result
plt.semilogx(freqs1, ftSong1-np.amax(ftSong1), freqs2, ftSong2-np.amax(ftSong2))
plt.legend(['First song', 'Second song'])
plt.show()

plt.close()