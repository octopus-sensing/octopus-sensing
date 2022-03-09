import os

from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices import AudioStreaming, CameraStreaming
from octopus_sensing.device_message_endpoint import DeviceMessageHTTPEndpoint


def main():
    device_coordinator = DeviceCoordinator()
    subject_id = "00"
    output_path = "output_remote/p{0}".format(subject_id)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=False)

    # Add your devices
    audio = AudioStreaming(0, name="Audio", output_path=output_path)
    # camera = \
    #     CameraStreaming(name="webcam",
    #                     output_path=output_path,
    #                     camera_no=0,
    #                     image_width=640,
    #                     image_height=480)

    device_coordinator = DeviceCoordinator()
    device_coordinator.add_devices([audio])

    # Create and start the endpoint
    message_endpoint = DeviceMessageHTTPEndpoint(device_coordinator)
    print("start listening")
    message_endpoint.start()

    while True:
        key = input("Please enter q to stop")
        if key == "q":
            break

    message_endpoint.stop()

if __name__ == "__main__":
    main()