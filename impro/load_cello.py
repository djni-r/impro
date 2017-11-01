import soundfile as sf
import os
import re


data = {}
rate = sf.read("resources/cello_sounds/Cello.arco.ff.sulA.A3.stereo.aif")[1]

for name in os.listdir("resources/cello_sounds"):
    mo = re.search("(A|C|D|G)\.[A-G]b?\d", name)
    string, pitch = mo.group(0).split('.')
    dat = sf.read("resources/cello_sounds/"+name)[0]

    if pitch in data:
        data[pitch][string] = dat
    else:
        data[pitch] = {string : dat}
