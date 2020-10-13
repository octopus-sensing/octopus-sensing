import os
import random
import csv


class Stimulus():
    def __init__(self, id, path):
        self.id = id
        self.path = path

    def show(self):
        raise NotImplementedError()


class VideoStimulus(Stimulus):
    def __init__(self, id, path):
        super().__init__(id, path)

    def show(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.system("sh {0}/play_video.sh {1}".format(current_dir, self.path))


class ImageStimulus(Stimulus):
    def __init__(self, id, path, show_time):
        super().__init__(id, path)
        self._show_time = show_time

    def show(self):
        pass
