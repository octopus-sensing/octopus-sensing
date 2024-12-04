import os
import time
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices import CameraStreaming
from octopus_sensing.devices.common import SavingModeEnum
from octopus_sensing.common.message_creators import start_message, stop_message

def main():
    device_coordinator = DeviceCoordinator()

    experiment_id = "px01"
    stimuli_id = "S00"
    subject_id = "00"
    output_path = "output_paths/p{0}".format(subject_id)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=False)

    # Add your devices
    my_audio = CameraStreaming(camera_no=0, saving_mode=SavingModeEnum.SEPARATED_SAVING_MODE)

    device_coordinator = DeviceCoordinator()
    device_coordinator.add_devices([my_audio])

    # A delay to be sure initialing devices have finished
    time.sleep(3)

    # Starts data recording
    device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
    time.sleep(6)

    # Stops deta recording
    device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
    time.sleep(0.5)

    stimuli_id = "S01" # change stimuli

    # Starts data recording
    device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
    time.sleep(5)

    # Stops deta recording
    device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
    time.sleep(5)
    
    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()

if __name__ == "__main__":
    main()
