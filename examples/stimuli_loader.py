import os
import csv
import mimetypes
import random
from octopus_sensing.stimuli import ImageStimulus, VideoStimulus


def load_stimuli(stimuli_path, csv_file="stimuli_ids.csv", show_time=None):
    stimuli_csv_file_path = os.path.join(stimuli_path, csv_file)
    stimuli_list = []
    if os.path.exists(stimuli_csv_file_path) is False:
        # If there is not csv file, it will be created here to use it next time
        stimuli_file_list = os.listdir(stimuli_path)
        stimuli_file_list.sort()
        with open(stimuli_csv_file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for i, item in enumerate(stimuli_file_list):
                type = mimetypes.guess_type(item)
                if 'image' in type[0]:
                    stimulus = ImageStimulus(i,
                                             os.path.join(stimuli_path, item),
                                             show_time=show_time)
                elif 'video' in type[0]:
                    stimulus = \
                        VideoStimulus(i, os.path.join(stimuli_path, item))
                stimuli_list.append(stimulus)
                writer.writerow([i, item])
    else:
        print(os.path.join(stimuli_path, csv_file))
        reader = csv.reader(open(os.path.join(stimuli_path, csv_file)),
                            delimiter=',')
        i = 0
        for row in reader:
            i = row[0]
            item = row[1]
            type = mimetypes.guess_type(item)
            if 'image' in type[0]:
                stimulus = ImageStimulus(i,
                                         os.path.join(stimuli_path, item),
                                         show_time=show_time)
            elif 'video' in type[0]:
                stimulus = \
                    VideoStimulus(i, os.path.join(stimuli_path, item))
            stimuli_list.append(stimulus)
    random.shuffle(stimuli_list)
    return stimuli_list
