#!/usr/local/bin/python2.7
import numpy
import pyaudio
import analyse
import time

from threading import Thread
from collections import deque, namedtuple

TimedPitch = namedtuple('TimedPitch', ['time', 'pitch'])

class Listener(Thread):
    def __init__(self, MAX_MEM = 100, TIME_DIFF = 1):
        Thread.__init__(self)
        self.pitches = deque(maxlen = MAX_MEM)
        self.pa = pyaudio.PyAudio()
        self.terminate = False
        self.TIME_DIFF = TIME_DIFF

    def run(self):
        try:
            stream = self.pa.open(44100, 1, pyaudio.paInt16, input=True)
            prev_pitch = None
            prev_time = 0

            while not self.terminate:
                rawsamps = stream.read(1024, exception_on_overflow=False)       
                samps = numpy.fromstring(rawsamps, dtype=numpy.int16)           
                pitch = analyse.musical_detect_pitch(samps)

                if pitch != prev_pitch \
                or time.time() - prev_time > self.TIME_DIFF:
                    now = time.time()
                    self.pitches.append(TimedPitch(now, pitch))
                    prev_pitch = pitch
                    prev_time = now
        finally:
            stream.close()


                    
            
