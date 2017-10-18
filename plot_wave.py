#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Fabien Marteau <mail@fabienm.eu>
""" plot_wave
"""
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import wave
import sys
import audioop

fname = "foobar.wav"
#fname = 'maison_raspberry_plaques_cuissons.wav'
#fname = 'Mesure_grille_pain_700W.wav'
#fname = 'Mesure_bouilloire_1100W.wav'

print("Open wave file : {}".format(fname))
spf = wave.open(fname,'r')

FECH = spf.getframerate()
print("Framerate : {}".format(FECH))
print("Frame num : {}".format(spf.getnframes()))

print("Extract Raw Audio from Wav File")
signal = spf.readframes(-1)
print("Convert string to int16")
signal = np.fromstring(signal, 'Int8')
print("extract channels")
if spf.getnchannels() > 1:
    monoright = np.array(
            [signal[i] for i in range(len(signal)) if i%2 == 0],
            dtype='Int16')
else:
    monoright = signal
print("RMS : {}".format(audioop.rms(signal, 2)))
print("RMS : {}".format(audioop.rms(monoright, 2)))
for i in range(10):
    print("RMS {} à {} seconds : {}"
            .format(i, i+1,
                audioop.rms(monoright[i*FECH:((i+1)*FECH)], 2)))


print("longueur du signal {} soit {} secondes"
        .format(len(monoright), len(monoright)/FECH))

#If Stereo
#if spf.getnchannels() == 2:
#    print('Just mono files')
#    sys.exit(0)

print("Plotting")
plt.figure(1)
plt.title('monoright')
plt.plot(monoright)
plt.show()
