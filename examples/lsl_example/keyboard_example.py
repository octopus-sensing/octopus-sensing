import os
import time
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices import LSLStreaming, CameraStreaming

def main():
    device_coordinator = DeviceCoordinator()

    experiment_id = "px01"
    stimuli_id = "S00"
    subject_id = "00"
    output_path = "output_path/p{0}".format(subject_id)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=False)

    # Add your devices
    # keyboardLSL = LSLStreaming(name="Keyboard_LSL", device_type="name", device="Keyboard")
    mouseLSL = LSLStreaming(name="MouseLSL", device_type="name", device="MousePosition")
    my_camera = CameraStreaming(camera_no=0,
                                name="camera",
                                output_path="./output")

    device_coordinator = DeviceCoordinator()
    device_coordinator.add_devices([my_camera, mouseLSL])

    # A delay to be sure initialing devices have finished
    time.sleep(3)

    # Starts data recording
    device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
    time.sleep(10)

    # Stops deta recording
    device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
    time.sleep(0.5)
    
    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()

if __name__ == "__main__":
    main()