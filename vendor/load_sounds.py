import os
import re
import logging
import sys
from collections import namedtuple

import soundfile as sf
from scipy.io import wavfile as wf

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger()

_sounds = namedtuple("Sounds", "data, rate")

def piano():
    data = []
    rate = wf.read(os.path.dirname(__file__)+"/resources/piano_sounds/piano_00001.wav")[0]

    for i in range(64):
        data.append(wf.read(os.path.dirname(__file__)+"/resources/piano_sounds/piano_{:05d}.wav".format(i+1))[1])

    return _sounds(data, rate)


def cello():
    data = {}
    rate = sf.read(os.path.dirname(__file__)+"/resources/cello_sounds/Cello.arco.ff.sulA.A3.stereo.aif")[1]

    for name in os.listdir(os.path.dirname(__file__)+"/resources/cello_sounds"):
        mo = re.search("(A|C|D|G)\.[A-G]b?\d", name)
        sul, pitch = mo.group(0).split('.')
        dat = sf.read(os.path.dirname(__file__)+"/resources/cello_sounds/"+name)[0]
        
        if pitch in data:
            data[pitch][sul] = name
        else:
            data[pitch] = {sul : name}
    #logger.debug(data)
    return _sounds(data, rate)


def xylo():
    data = {}
    rate = sf.read(os.path.dirname(__file__)+"/resources/xylo_sounds/Xylophone.hardrubber.ff.A4.stereo.aif")[1]

    for name in os.listdir(os.path.dirname(__file__)+"/resources/xylo_sounds"):
        key = name.split('.')[3]
        logger.debug(name)
        data[key] = name #sf.read(os.path.dirname(__file__)+"/resources/xylo_sounds/"+name)[0]

    return _sounds(data, rate)


def misc(folder_num):
    data = []
    dirname = os.path.dirname(__file__)+"/resources/misc_sounds/" + str(folder_num)
    for name in os.listdir(dirname):
        if not name.startswith("."): 
            data.append(dirname+'/'+name)

    logger.debug(data)
    return data
    
    
