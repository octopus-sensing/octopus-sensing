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
import threading
import socket
from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.common.message import Message
from octopus_sensing.devices.device import Device

class SocketNetworkDevice(Device):
    '''
    This class is being used for sending triggers to other softwares using TCP-IP socket.
    It works as a server socket, which sends triggers (when an event happen) to the connected clients.

    For example if we have a device that record data through matlab, through this server socket, we can 
    send the trigger to the matlab application to mark the recorded data.

    Attributes
    ----------

    Parameters
    ----------
    host: str
        host IP address

    port: str
        port number

    Example
    -------
    Creating a SocketNetworkDevice in the local machine and adding it to the device_coordinator.
    By adding it to the DeviceCoordinator, it starts listening

    >>> device_coordinator = DeviceCoordinator()
    >>> socket_device = SocketNetworkDevice("0.0.0.0", 5002)
    >>> device_coordinator.add_devices([socket_device])

    Note
    -----
    Look at Examples/send_trigger_to_remote_device.py (server code), 
    Examples/matlabRecorder.m or examples/client.py (client codes)

    '''
    def __init__(self,
                 host: str,
                 port: str,
                 **kwargs):
        super().__init__(**kwargs)

        self._server_socket = socket.socket()  # get instance
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(0.5)
        self.__connections = []

        self._server_socket.bind((host, port))  # bind host address and port together
        self._stop_listening = False


        self._trigger = None
        self._experiment_id = None


    def _accept_connections(self):
        print("Listening")
        self._server_socket.listen(5)
        while True:
            if self._stop_listening is True:
                print("End of listening")
                break
            try:
                conn, address = self._server_socket.accept()  # accept new connection
            except socket.timeout:
                continue
            if conn is not None:
                self.__connections.append(conn)
                print("Connection from: " + str(address))

        print("close socket")
        self._server_socket.shutdown(socket.SHUT_RDWR)
        self._server_socket.close()

    def _run(self):
        threading.Thread(target=self._accept_connections).start()
        while True:
            message = self.message_queue.get()
            print(message)
            if message is None:
                continue
            if message.type == MessageType.START:
                print("start")
                self._experiment_id = message.experiment_id
                self.__set_trigger(message)
                for connection in self.__connections:
                    threading.Thread(target=self.__send_message, args=(connection,)).start()

            elif message.type == MessageType.STOP:
                self._experiment_id = message.experiment_id
                self.__set_trigger(message)
                for connection in self.__connections:
                    threading.Thread(target=self.__send_message, args=(connection,)).start()

            elif message.type == MessageType.TERMINATE:
                print("terminate")
                self._trigger = "terminate"
                print("done")
                self._stop_listening = True
                for connection in self.__connections:
                    threading.Thread(target=self.__send_message, args=(connection,)).start()
                break


    def __send_message(self, connection: socket.socket):
        '''
        Gets a connection and sends the trigger to it

        Parameters
        ----------
        connection: socket.socket
            a socket connection
        '''
        print("send message", self._trigger)
        self._trigger += "\n"
        connection.send(self._trigger.encode())

    def __set_trigger(self, message: Message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        ----------
        message: Message
            a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))
