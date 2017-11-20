from scipy.io import wavfile as wf

data = []
rate = wf.read("vendor/resources/piano_sounds/39148__jobro__piano-ff-001.wav")[0]

for i in range(64):
    data.append(wf.read("vendor/resources/piano_sounds/{:d}__jobro__piano-ff-0{:02d}.wav".format(
                            39148+i if i < 44 else 39149+i, i+1))[1])
