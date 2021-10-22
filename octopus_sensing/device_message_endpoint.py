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
from octopus_sensing.common.message import Message


class DeviceMessageHTTPEndpoint(EndpointBase):

    def __init__(self, device_coordinator, port=9331):
        super().__init__(endpoint_name="MonitoringEndpoint-Thread",
                         port=port, post_callback=self._post_handler)
        self._device_coordinator = device_coordinator

    def _post_handler(self, request_body: dict):
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
