import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Read the file (rate and data):
rate, data = wavfile.read('file.wav') # See source

# Compute PSD:
f, P = signal.periodogram(data, rate) # Frequencies and PSD

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

x = f
y = P

fig = plt.figure()

plt.scatter(x, y)
plt.plot(x, y)

plt.show()
