import time
import os
import msgpack
import http.client

from octopus_sensing.stimuli import ImageStimulus


def simple_scenario(stimuli_path):
    http_client = http.client.HTTPConnection("127.0.0.1:9331", timeout=3)
    # Reading image stimuli and assigning an ID to them based on their alphabetical order
    stimuli_list = os.listdir(stimuli_path)
    stimuli_list.sort()
    stimuli = {}
    i = 0
    for item in stimuli_list:
        stimuli[i] = item
        i += 1

    experiment_id = "p01"

    # A delay to be sure initialing devices have finished
    time.sleep(3)
 
    input("\nPress a key to run the scenario")

    for stimuli_id, stmulus_name in stimuli.items():
        # Starts data recording by displaying the image
        http_client.request("POST", "/",
                            body=msgpack.packb({'type': 'START',
                                                'experiment_id': experiment_id,
                                                'stimulus_id': stimuli_id}),
                            headers={'Accept': 'application/msgpack'})
        response = http_client.getresponse()
        assert response.status == 200

        # Displaying image may start with some miliseconds delay after data recording
        # because of GTK initialization in show_image_standalone. If this delay is important to you,
        # use other tools for displaying image stimuli
        # Since image is displaying in another thread we have to manually create the same delay in current 
        # thread to record data for 10 seconds

        timeout = 10
        stimulus = ImageStimulus(stimuli_id, os.path.join(stimuli_path, stmulus_name), timeout)
        stimulus.show_standalone()
        time.sleep(timeout)

        # IF the stimuli is a video we are displaying stimuli as follows
        #stimulus = VideoStimulus(stimuli_id, os.path.join(stimuli_path, stmulus_name))
        #stimulus.show()

        # Stops data recording by closing image
        http_client.request("POST", "/",
                    body=msgpack.packb({'type': 'STOP',
                                        'experiment_id': experiment_id,
                                        'stimulus_id': stimuli_id}),
                    headers={'Accept': 'application/msgpack'})
        response = http_client.getresponse()
        assert response.status == 200
        input("\nPress a key to continue")

    # Terminate, This step is necessary to close the connection with added devices
    http_client.request("POST", "/",
                body=msgpack.packb({'type': 'TERMINATE'}),
                headers={'Accept': 'application/msgpack'})
    response = http_client.getresponse()
    assert response.status == 200

if __name__ == "__main__":
    simple_scenario('/home/nastaran/Pictures/wood pattern')#Path_to_the_stimuli_folder')