import os
import re
from collections import namedtuple

import soundfile as sf
from scipy.io import wavfile as wf

_sounds = namedtuple("Sounds", "data, rate")

def piano():
    data = []
    rate = wf.read("vendor/resources/piano_sounds/39148__jobro__piano-ff-001.wav")[0]

    for i in range(64):
        data.append(wf.read("vendor/resources/piano_sounds/{:d}__jobro__piano-ff-0{:02d}.wav".format(39148+i if i < 44 else 39149+i, i+1))[1])

    return _sounds(data, rate)


def cello():
    data = {}
    rate = sf.read("vendor/resources/cello_sounds/Cello.arco.ff.sulA.A3.stereo.aif")[1]

    for name in os.listdir("vendor/resources/cello_sounds"):
        mo = re.search("(A|C|D|G)\.[A-G]b?\d", name)
        sul, pitch = mo.group(0).split('.')
        dat = sf.read("vendor/resources/cello_sounds/"+name)[0]

        if pitch in data:
            data[pitch][sul] = dat
        else:
            data[pitch] = {sul : dat}

    return _sounds(data, rate)


def xylo():
    data = {}
    rate = sf.read("vendor/resources/xylo_sounds/Xylophone.hardrubber.ff.A4.stereo.aif")[1]

    for name in os.listdir("vendor/resources/xylo_sounds"):
        key = name.split('.')[3]
        data[key] = sf.read("vendor/resources/xylo_sounds/"+name)[0]

    return _sounds(data, rate)
