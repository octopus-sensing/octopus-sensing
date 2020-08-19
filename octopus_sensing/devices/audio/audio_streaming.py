import threading
import sounddevice as sd
from scipy.io.wavfile import write

from octopus_sensing.devices.device import Device

SAMPLING_RATE = 44100  # Sample rate

# The sounddevice library is not working with multiprocessing
class AudioStreaming(Device):
    def __init__(self):
        super().__init__()
        self._recording_time = 0
        self._stream_data = []
        self._record = False
        sd._initialize()

    def run(self):
        threading.Thread(target=self._stream_loop).start()
        while True:
            message = self.message_queue.get()
            if message is not None:
                self.subject_id = message.subject_id
                self.stimulus_id = message.stimulus_id
            if message.type == "terminate":
                break
            elif message.type == "stop_record":
                self._record = False
                self._save_to_file()
            elif message.type == "start_record":
                # The duration of audio recording
                self._recording_time = message.payload["audio_recording_time"]
                self._stream_data = []
                self._record = True

        def _streem_loop(self):
            if self._record is True:
                print("start audio recording")
                self._stream_data = \
                    sd.rec(int(self._recording_time * SAMPLING_RATE),
                           samplerate=SAMPLING_RATE,
                           channels=2)
                sd.wait()  # Wait until recording is finished
                print("stop audio recording")

        def _save_to_file(self):
            file_name = \
                "{0}/audio/{1}-{2}-{3}.wav".format(self.output_path,
                                                   self.device_name,
                                                   self.subject_id,
                                                   self.stimulus_id)
            write(file_name, SAMPLING_RATE, self._stream)
