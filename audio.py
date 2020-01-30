import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread

SAMPLING_RATE = 44100  # Sample rate

# The sounddevice library is not working with multiprocessing
class AudioStreaming(Thread):
    def __init__(self, file_name, recording_time):
        super().__init__()
        self._file_path =  "created_files/audio/" + file_name + '.wav'
        self._recording_time = recording_time
        sd._initialize()

    def run(self):
        print("start audio recording")
        myrecording = \
            sd.rec(int(self._recording_time * SAMPLING_RATE),
                   samplerate=SAMPLING_RATE,
                   channels=2)
        sd.wait()  # Wait until recording is finished
        print("stop audio recording")
        write(self._file_path, SAMPLING_RATE, myrecording)
