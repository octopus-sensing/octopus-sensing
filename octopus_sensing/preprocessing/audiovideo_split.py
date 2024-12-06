# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.
import os
from datetime import datetime
import csv
from pydub import AudioSegment

def audio_split(log_path: str, audio_path: str):
    timestamps = []
    marks = [0]

    with open(log_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        timestamps = [(row[0], row[1]) for row in csv_reader if len(row) > 0]

    for i in range(len(timestamps) - 2):
        elapsed_time = 0
        start_time = datetime.strptime(timestamps[0][0], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(timestamps[i+1][0], "%Y-%m-%d %H:%M:%S.%f")

        diff = end_time - start_time
        elapsed_time = int((diff.seconds * 1000) + (diff.microseconds / 1000))
        marks.append(elapsed_time)
    
    j = 0
    for i in range(int(len(marks)*.5)):
        split_audio = AudioSegment.from_wav('Audio-px01.wav')
        split_audio = split_audio[marks[j]:marks[j+1]]
        split_audio.export(f"audio_stimuli_{timestamps[j][1]}.wav", format="wav")
        j+=2

def video_split(log_path: str, video_path: str):
    return None
