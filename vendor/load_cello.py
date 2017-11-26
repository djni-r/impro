import soundfile as sf
import os
import re


def load():
    data = {}
    rate = sf.read("vendor/resources/cello_sounds/Cello.arco.ff.sulA.A3.stereo.aif")[1]

    for name in os.listdir("vendor/resources/cello_sounds"):
        mo = re.search("(A|C|D|G)\.[A-G]b?\d", name)
        string, pitch = mo.group(0).split('.')
        dat = sf.read("resources/cello_sounds/"+name)[0]

        if pitch in data:
            data[pitch][string] = dat
        else:
            data[pitch] = {string : dat}

    return (data, rate)
