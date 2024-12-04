import time
#from octopus_sensing.devices import Shimmer3Streaming
from octopus_sensing.devices import CameraStreaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.realtime_data_endpoint import RealtimeDataEndpoint



def simple_scenario():
    print("initializing")
    # Creating an instance of simmer3
    #my_shimmer = Shimmer3Streaming(name="shimmer", output_path="./output")

    # Creating an instance of camera. by uncommenting this line and adding it to the dive_coordinator
    # you can record video data as well
    my_camera = CameraStreaming(0, name="camera", output_path="./output")

    # Creating an instance of device coordinator
    device_coordinator = DeviceCoordinator()

    # Adding sensor to device coordinator
    device_coordinator.add_devices([my_camera])

    experiment_id = "p01"
    stimuli_id = "s01"

    # A delay to be sure initialing devices have finished
    time.sleep(3)
 
    input("\nPress a key to run the scenario")
    print("***********************")
    device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
    realtime_data_endpoint = RealtimeDataEndpoint(device_coordinator)
    realtime_data_endpoint.start()
    while True:
        key = input("Please enter q to stop")
        if key == "q":
            break

    device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))

    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()
    realtime_data_endpoint.stop()

if __name__ == "__main__":
    simple_scenario()