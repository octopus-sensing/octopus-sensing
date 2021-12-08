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
import threading
import http.server
import json

import pytest

from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.network_devices.http_device import HttpNetworkDevice
from octopus_sensing.common.message_creators import start_message, stop_message


class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._expected_messages = [
            {"type": "START", "experiment_id": "exp1", "stimulus_id": "stim1"},
            {"type": "STOP", "experiment_id": "exp1", "stimulus_id": "stim2"},
            {"type": "TERMINATE", "experiment_id": "", "stimulus_id": ""},
        ]

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "-1"))
        serialized_body = self.rfile.read(content_length)
        body = json.loads(serialized_body)

        assert body == self._expected_messages.pop()

        self.send_response(200)
        self.end_headers()


def test_http_network_device_happy_path():
    coordinator = DeviceCoordinator()
    device = HttpNetworkDevice(
        ["http://localhost:5003/"], name="test-http-network-device", timeout=15)
    coordinator.add_device(device)

    server = http.server.ThreadingHTTPServer(("localhost", 5003), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    # To ensure device and server are started
    time.sleep(1)

    coordinator.dispatch(start_message("exp1", "stim1"))
    coordinator.dispatch(stop_message("exp1", "stim2"))
    # Should send TERMINATE message
    coordinator.terminate()


def test_validations():
    # Invalid URLs
    with pytest.raises(RuntimeError):
        HttpNetworkDevice(["localhost:5003"])
    with pytest.raises(RuntimeError):
        HttpNetworkDevice(["127.0.0.1"])
    with pytest.raises(RuntimeError):
        HttpNetworkDevice(["ftp://localhost:5003"])
    with pytest.raises(RuntimeError):
        HttpNetworkDevice(["http:/192.168.1.1/"])
    with pytest.raises(RuntimeError):
        HttpNetworkDevice(["http//192.168.1.1/"])
    # Can't really detect port is not a number. This port will be simply ignored!
    # with pytest.raises(RuntimeError):
    #    HttpNetworkDevice(["http://192.168.1.1:abc/"])

    # Valid URLs
    HttpNetworkDevice(
        ["http://localhost:80",
         "https://localhost/",
         "http://192.168.1.1/",
         "http://192.168.1.1:8080/",
         "http://[::1]/",
         "http://[2345:425:2ca1:0000:0000:567:5673:23b5]/",
         "http://[2345:425:2ca1:0000:0000:567:5673:23b5]:8080/",
         "https://localhost/abc/def",
         "http://localhost:9090/data?q=123",
         ])
