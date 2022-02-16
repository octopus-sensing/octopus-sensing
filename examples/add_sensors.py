import time
from octopus_sensing.devices import CameraStreaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message

def add_sensors():
    # Creating an instance of sensor
    
    my_camera = CameraStreaming(camera_no=0,
                                name="camera",
                                output_path="./output")

    # Creating an instance of device coordinator
    device_coordinator = DeviceCoordinator()

    # Adding sensor to device coordinator
    device_coordinator.add_devices([my_camera])

    experiment_id = "p01"
    stimuli_id = "S00"

    input("Press a button to start data recording")

    # Starts data recording
    device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
    time.sleep(5)

    # Stops deta recording
    device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
    time.sleep(0.5)
    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()

if __name__ == "__main__":
    add_sensors()