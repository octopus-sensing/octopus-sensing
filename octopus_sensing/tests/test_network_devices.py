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
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.

import time
import pytest
import sys  # nopep8
import threading
import socket

from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.network_devices.socket_device import SocketNetworkDevice
from octopus_sensing.common.message_creators import start_message, stop_message

PORT = 5002
EVENT = threading.Event()
TIMEOUT = 30

def __server():
    '''
    Starts a server and send several messages and terminates
    '''
    device_coordinator = DeviceCoordinator()
    socket_device = SocketNetworkDevice("localhost", PORT)
    device_coordinator.add_devices([socket_device])

    EVENT.wait(timeout=TIMEOUT)
    message = start_message("test", "00")
    device_coordinator.dispatch(message)

    time.sleep(1)
    message = stop_message("test", "00")
    device_coordinator.dispatch(message)
    time.sleep(1)
    message = start_message("test", "01")
    device_coordinator.dispatch(message)
    time.sleep(1)
    message = stop_message("test", "01")
    device_coordinator.dispatch(message)
    time.sleep(2)

    device_coordinator.terminate()

def test_client_socket():
    threading.Thread(target=__server).start()
    time.sleep(5)
    host = "localhost"
    port = PORT

    # Waiting at most 30 seconds for the SocketNetworkDevice to become ready.
    retries = TIMEOUT
    while True:
      try:
          client_socket = socket.create_connection((host, port))
          break
      except ConnectionError:
          if retries <= 0:
              raise
          retries = retries - 1
          time.sleep(1)
          continue
    # Causes the server to start sending messages.
    EVENT.set()

    data = client_socket.recv(1024).decode()  # receive response
    assert data == "START-test-00\n"
    data = client_socket.recv(1024).decode()  # receive response
    assert data == "STOP-test-00\n"
    data = client_socket.recv(1024).decode()  # receive response
    assert data == "START-test-01\n"
    data = client_socket.recv(1024).decode()  # receive response
    assert data == "STOP-test-01\n"

    data = client_socket.recv(1024).decode()  # receive response
    assert data == "terminate\n"

    client_socket.close()  # close the connection
