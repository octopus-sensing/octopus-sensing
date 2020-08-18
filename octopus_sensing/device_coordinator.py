import multiprocessing


class DeviceCoordinator():
    '''
    Coordinating devices
    '''
    def __init__(self):
        self.devices = []
        self.quesues = []


    def add_device(self, device):
        '''
        Adds new device to the coordinator

        @param Device device: a device object

        @keyword str name: The name of device
        '''
        if device in self.devices:
            raise "This device already has been added"
        self.devices.append(device)
        queue = multiprocessing.Queue()
        device.set_queue(queue)
        self.quesues.append(queue)

    def add_devices(self, devices):
        '''
        Adds new devices to the coordinator

        @param list devices: a list of device object
        @type devices: list(Device)
        '''
        for device in devices:
            self.add_device(device)

    def dispatch(self, message):
        '''
        dispatch new message to all devices

        @param Message message: a message object object
        '''
        for queue in self.quesues:
            queue.put(message)
