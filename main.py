import sys

import pyaudio

import matplotlib.pyplot as plt
import numpy as np

CHUNK = 1024
RATE = 44100

FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2

AMPLITUDE = 5000
FREQUENCY = 10000

# plot wave
def wave(data):
    x = np.arange(0,2*CHUNK,2)
    plt.subplot(1, 2, 1)
    plt.plot(x, data)
    # set axis range
    ax = plt.gca()
    ax.set_xlim([0, CHUNK])
    ax.set_ylim([-AMPLITUDE, AMPLITUDE])

# plot fft
def fft(data):
    plt.subplot(1, 2, 2)
    ft = np.fft.fft(data)
    freq = np.fft.fftfreq(CHUNK, 0.1)

    # set axis range
    ax = plt.gca()
    ax.set_xlim([0, .5])
    ax.set_ylim([0, 2e10])

    plt.plot(freq, ft.real**2 + ft.imag**2)

# main function
def main():

    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True)

    print('* beginning')

    plt.figure()
    plt.ion()
    plt.ylim(-100, 100)
    plt.xlim(10000)

    stream.start_stream()

    active = True
    while active:
        try:
            # clear
            plt.clf()
            # calculate
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
            wave(data)
            fft(data)
            # display
            plt.show()
            plt.pause(0.001)
        except KeyboardInterrupt:
            active = False

    stream.close()
    pa.terminate()

    print('* done')

# execute main
if __name__ == "__main__":
    main()
