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

from octopus_sensing.common.endpoint_base import EndpointBase, EndpointClientError
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message import Message


class DeviceMessageHTTPEndpoint(EndpointBase):
    '''
    Stars and endpoint that listens for incoming Message requests. It passes the message to
    the Device Coordinator to dispatch them to the devices.
    It accepts HTTP POST requests. The Body can be serialized in one of 'json', 'msgpack'
    or 'pickle'. See the Usage section for how to call the endpoint.

    Attributes
    ----------

    Parameters
    ----------
    device_coordinator
        An instance of DeviceCoordinator class.
    port
        Port to listen on. Default is: 9331

    Examples
    --------
    To start the endpoint:

    >>> from octopus_sensing.device_coordinator import DeviceCoordinator
    >>> from octopus_sensing.device_message_endpoint import DeviceMessageHTTPEndpoint
    >>> device_coordinator = DeviceCoordinator()
    >>> # Add you devices
    >>> message_endpoint = DeviceMessageHTTPEndpoint(device_coordinator)
    >>> message_endpoint.start()
    >>> # You need to stop it after your program finished.
    >>> message_endpoint.stop()

    The client can call the endpoint like this (Note that it's a separate process):

    >>> import http.client
    >>> import msgpack
    >>> http_client = http.client.HTTPConnection("127.0.0.1:9331", timeout=3)
    >>> http_client.request(
    ...     "POST", "/",
    ...    body=msgpack.packb({'type': 'START',
    ...                        'experiment_id': '123',
    ...                        'stimulus_id': 's8'}),
    ...                        headers={'Accept': 'application/msgpack'})
    >>> response = http_client.getresponse()
    >>> assert response.status == 200

    Note that you must pass 'Accept' in the headers, so the endpoint knows what
    type of serialization you used.
    Also, the request needs 'Content-Length' in headers. However, it's part of
    the HTTP standard and your http client should do it automatically.

    '''

    def __init__(self, device_coordinator: DeviceCoordinator, port: int = 9331):
        super().__init__(endpoint_name="DeviceMessageHttpEndpoint-Thread",
                         port=port, post_callback=self._post_handler)
        self._device_coordinator = device_coordinator

    def _post_handler(self, request_body: dict):
        if not isinstance(request_body, dict):
            raise EndpointClientError(
                "The request body must contain a dictionary. Got [{}]".format(type(request_body)))

        if 'type' not in request_body:
            raise EndpointClientError(
                "'type' field is mandatory in request body")

        message_type = request_body['type']
        experiment_id = request_body.get('experiment_id', None)
        stimulus_id = request_body.get('stimulus_id', None)

        if not isinstance(message_type, str):
            raise EndpointClientError(
                "'type' must be of type 'str', got '{0}'".format(type(message_type)))
        if experiment_id is not None and not isinstance(experiment_id, str):
            raise EndpointClientError(
                "'experiment_id' must be of type 'str', got '{0}'".format(type(experiment_id)))
        if message_type is not None and not isinstance(message_type, str):
            raise EndpointClientError(
                "'stimulus_id' must be of type 'str', got '{0}'".format(type(stimulus_id)))

        message = Message(message_type,
                          request_body.get('payload', None),
                          experiment_id,
                          stimulus_id)

        self._device_coordinator.dispatch(message)

        return "message dispatched"
