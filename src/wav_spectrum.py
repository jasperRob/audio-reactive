import wave
import numpy as np
import scipy
import matplotlib.pyplot as plt
import struct

import pyaudio

file = "stereo.wav"

# pyAusio setup
pa = pyaudio.PyAudio()

CHUNK = 88200

# calc fft
def rfft(sig, t):
    f = np.fft.rfftfreq(sig.size, d=t[1]-t[0])
    y = np.fft.rfft(sig)
    return f, np.abs(y)

with wave.open(file, 'rb') as wf:

    rate = wf.getframerate()
    plt.figure()
    plt.ion()

    # open stream based on the wave object which has been input.
    stream = pa.open(format = pa.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)


    # Play samples from the wave file (3)
    while len(data := wf.readframes(rate)):  # Requires Python 3.8+ for :=
        stream.write(data)
         
        # Now we have the chunk of data.
        # Unpack data using struct
        unpack_data = (struct.unpack('h'*CHUNK, data))
        # unpack_data = (np.frombuffer(data))
         
        #convert it into readable array
        pcm = np.array(list(unpack_data), dtype = float)

        l = int(len(pcm)/2)
        print(l)
         
        # Calculate FFT
        fft = np.fft.fft(pcm)
        fftr = 10*np.log10(abs(fft.real))

        fftr = fftr[:l]
        # calculate real part of the FFT, take only the absolute values and convert it into dB scale
        # Rest half of the fft array is a mirror image of the first half.
        # So take only the first half of the array. We don't need that rest half.


        print(fftr)

         
        # Set the Frequency scale
        freq=np.fft.fftfreq(len(pcm), 0.1)
        freq=freq[:l]
        freq=freq*rate/1000
         
        # Plot the periodogram
        # plt.clf()
        # plt.plot(freq,fftr)
        # plt.xlabel("Frequency(KHz)")
        # plt.ylabel("Power(dB)")
        # plt.show()
        # plt.pause(0.001)
