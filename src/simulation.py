import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pygame
import math
import wave
import struct

# Audio
CHUNK = 1024
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
AMPLITUDE = 5000
FREQUENCY = 10000
SCALE = 1e+307
THRESHOLD = 45

# UI
BACKGROUND = "white"
NUM_PIXELS = 40
PIXEL_SIZE = 40

# args
style = sys.argv[1]
file = sys.argv[2]

# open the file for reading.
wf = wave.open(file, 'rb')

# pyAusio setup
pa = pyaudio.PyAudio()

# open stream based on the wave object which has been input.
stream = pa.open(format = pa.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 40))
clock = pygame.time.Clock()

class Pixel:
  red = 0;
  green = 0;
  blue = 0;

# calc fft
def fft(signal, time):
    f = np.fft.fftfreq(len(signal), d=time[1]-time[0])
    y = np.fft.fft(signal)
    return f, y

def spectrum(signal, freq):
    res = math.floor(len(signal) / NUM_PIXELS)
    avgs = []
    pixels = []
    fftr = 10*np.log10(abs(signal.real))
    # fftr[np.isnan(fftr)] = 0;
    for i in range(NUM_PIXELS):
        lower = res*i
        upper = res*(i+1)


        avg = sum(fftr[lower:upper]) / len(fftr[lower:upper])

        if (np.isinf(avg)):
            avgs.append(0)
        else:
            avgs.append(int(avg))


        p = Pixel()
        p.red = 0 if avg > THRESHOLD else 255
        p.green = 0 if avg > THRESHOLD else 255
        p.blue = 0 if avg > THRESHOLD else 255
        pixels.append(p)

    print(avgs)
    return avgs, pixels

def draw(pixels):
    for i in range(NUM_PIXELS):
        p = pixels[i]
        pygame.draw.rect(screen, (p.red, p.green, p.blue), (i*PIXEL_SIZE,0,PIXEL_SIZE,PIXEL_SIZE), 0)

# main function
def main():

    print('* beginning')

    with wave.open(file, 'rb') as wf:

        # Play samples from the wave file (3)
        while len(signal := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(signal)
            # dummy process events
            for _ in pygame.event.get():
                pass
            # clear screen
            screen.fill(BACKGROUND)
            # ampl, freq = fft()
            time = np.arange(0, CHUNK, 1)
            unpack_data = (struct.unpack('h'*2048, signal))
            freq, spec = fft(unpack_data, time)


            pixels = None
            avgs = None
            if style == 'spectrum':
                avgs, pixels = spectrum(spec, freq)
            else:
                print("Unknown style " + style)
                raise Exception()

            draw(pixels)

            pygame.display.update()
            clock.tick(60)


    pygame.quit()
    stream.close()
    pa.terminate()

    print('* done')

# execute main
if __name__ == "__main__":
    main()
