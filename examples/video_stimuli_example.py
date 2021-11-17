import time
import os
from octopus_sensing.devices.camera_streaming import CameraStreaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.stimuli.video_stimuli import show_video_stimuli


def video_stimuli_example(stimuli_path):
    # Reading video stimuli and assigning an ID to them based on their alphabetical order
    stimuli_list = os.listdir(stimuli_path)
    stimuli_list.sort()
    stimuli = {}
    i = 0
    for item in stimuli_list:
        stimuli[i] = item
        i += 1
    
    print("initializing")
    # Creating an instance of sensor
    my_camera = CameraStreaming(0, name="camera", output_path="./output", )

    # Creating an instance of device coordinator
    device_coordinator = DeviceCoordinator()

    # Adding sensor to device coordinator
    device_coordinator.add_devices([my_camera])

    experiment_id = "p01"

    # A delay to be sure initialing devices have finished
    time.sleep(3)
 
    input("Press a key to run the scenario")

    for stimuli_id, stmulus_name in stimuli.items():
        # Starts data recording by displaying the image
        device_coordinator.dispatch(start_message(experiment_id, stimuli_id))

        # Displaying image may start with some miliseconds delay after data recording because of GTK initialization in show_image_standalone. If this delay is important to you, use other tools for displaying image stimuli
        show_video_stimuli(os.path.join(stimuli_path, stmulus_name))

        # Stops data recording by closing image
        device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
        input("\nPress a key to continue")

    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()

if __name__ == "__main__":
    video_stimuli_example("/home/nastaran/Videos")