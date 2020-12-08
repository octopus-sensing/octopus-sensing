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

import sys
import traceback
import threading
import pickle
import json
import http.server

import msgpack


def make_handler(device_coordinator):
    class Handler(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            data = device_coordinator.get_monitoring_data()

            encoding_type = self.headers.get("Accept")
            if encoding_type is None or "pickle" in encoding_type:
                serialized_data = pickle.dumps(data)
            elif "json" in encoding_type:
                serialized_data = json.dumps(data)
            elif "msgpack" in encoding_type:
                serialized_data = msgpack.packb(data)
            else:
                self.send_error(
                    400,
                    message="Unknown content type. Should be one of 'json', 'msgpack', or 'pickle'")
                self.end_headers()
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(serialized_data)

    return Handler


class MonitoringEndpoint(threading.Thread):

    def __init__(self, device_coordinator):
        super().__init__(daemon=True, name="MonitoringEndpoint-Thread")
        self._device_coordinator = device_coordinator
        self._server = None

    def run(self):
        try:
            self._server = http.server.ThreadingHTTPServer(
                ('0.0.0.0', 9330), make_handler(self._device_coordinator))
            self._server.serve_forever()
        except Exception as ex:
            print("Error in MonitoringEndpoint", file=sys.stderr)
            traceback.print_exc()

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server = None
