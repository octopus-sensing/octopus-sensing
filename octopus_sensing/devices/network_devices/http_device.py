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
import re
import threading
import http.client
import pickle
import json
from typing import Optional, Callable, List, Union

import msgpack

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.common.message import Message
from octopus_sensing.devices.device import Device


class SerializationTypes:
    JSON = json.dumps
    MSGPACK = msgpack.packb
    PICKLE = pickle.dumps


class HttpNetworkDevice(Device):
    '''
    This class can be used to send messages (triggers) to the other softwares
    through HTTP protocol.

    The external software need to listen for incoming HTTP connections (a.k.a
    HTTP server or HTTP endpoint). This device will POST message to the specified
    URLs.

    The messages will be in the form of a dictionary, serialized by the specified
    type. For example, if the `serialization_type` is JSON, a `START` message will
    be:

    {"type": "START", "experiment_id": "exp1", "stimulus_id": "s1"}

    Parameters
    ----------
    external_endpoints: List[str]
      A list of URLs to send the message to. It should have the scheme
      (http or https) at the beginning. For example: ["http://localhost:8080"]
      Note that for IPv6, you need to put it between braces, like this:
      `http://[2345:425:2ca1:0000:0000:567:5673:23b5]/`

    serialization_type:
      Should be one of the types defined in SerializationTypes

    name: str, default: None
      Name of this device

    timeout: int, default: 3
      Timeout for both connecting to the external endpoint and POSTing messages.
      In seconds.

    Example
    -------
    In your Octopus Sensing software:

    >>> coordinator = DeviceCoordinator()
    >>> device = HttpNetworkDevice(["http://localhost:8080/", "http://192.168.1.1/trigger"])
    >>> coordinator.add_device(device)

    Every message that is dispatched using `coordinator.dispatch` method will
    be send to `http://localhost:8080/`.
    '''

    def __init__(self,
                 external_endpoints: List[str],
                 serialization_type: Callable[...,
                                              Union[bytes, str]] = SerializationTypes.JSON,
                 name: Optional[str] = None,
                 timeout: int = 3):
        super().__init__(name=name)
        self._endpoints = external_endpoints
        self._timeout = timeout
        self._serialization_func = serialization_type

        # Regex is borrowed from O'Reilly website: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s10.html
        # It validates and extracts host and port parts of the URL
        self._url_regex = re.compile((
            r"""([a-z][a-z0-9+\-.]*://)"""  # scheme
            r"""([a-z0-9\-._~%]+"""  # named host
            r"""|\[[a-f0-9:.]+\]"""  # ipv6 host
            r"""|\[v[a-f0-9][a-z0-9\-._~%!$&'()*+,;=:]+\])"""  # IPvFuture host
            r"""(:[0-9]+)?"""  # port
            r"""(/.*)?"""  # rest
        ))

        # We want to give these kind of errors early
        self._validate_endpoints()

    def _validate_endpoints(self):
        for endpoint in self._endpoints:
            match_object = self._url_regex.match(endpoint)
            if match_object is None:
                raise RuntimeError("HttpNetworkDevice({0}): invalid URL: {1}\nIt should be in the form http://host:port/".format(
                    self.name, endpoint))
            scheme, host, port, rest = match_object.groups()
            if scheme not in ('http://', 'https://'):
                raise RuntimeError("HttpNetworkDevice({0}): invalid URL: {1} It only supports 'http' & 'https' scheme, got: {2}".format(
                    self.name, endpoint, scheme))

    def _run(self):
        while True:
            message = self.message_queue.get()

            if message is None:
                continue

            self._send_message(message)

            if message.type == MessageType.TERMINATE:
                break

    def _send_message(self, message: Message):
        message_dict = {"type": message.type,
                        "experiment_id": message.experiment_id,
                        "stimulus_id": message.stimulus_id}
        serialized_message = self._serialization_func(message_dict)

        for endpoint in self._endpoints:
            threading.Thread(target=self._http_post,
                             args=(endpoint, serialized_message,)).start()

    def _http_post(self, endpoint: str, body: Union[bytes, str]):
        match_object = self._url_regex.match(endpoint)
        assert match_object is not None, 'We already validated all endpoints'
        scheme, host, port_str, rest = match_object.groups()

        port: Optional[int] = None
        if port_str:
            port = int(port_str[1:])

        connect_to = "{0}:{1}".format(scheme, host)
        post_to = rest
        if not rest:
            post_to = "/"

        http_client = http.client.HTTPConnection(
            connect_to, port=port, timeout=self._timeout)

        http_client.request("POST", post_to, body=body)
        response = http_client.getresponse()

        if response.status != 200:
            print("HttpNetworkDevice({0}): Sending message to [{1}] failed: {2} {3}".format(
                  self.name, endpoint, response.status, response.reason),
                  file=sys.stderr)
