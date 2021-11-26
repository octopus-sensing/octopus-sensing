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
import http.client
import pickle
import json

import pytest
import msgpack

from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.device import Device
from octopus_sensing.device_message_endpoint import DeviceMessageHTTPEndpoint
from octopus_sensing.common.message import Message


def fake_run(self):
    pass


@pytest.fixture()
def fixture():
    test_device = Device()
    test_device._run = fake_run
    coordinator = DeviceCoordinator()
    coordinator.add_device(test_device)

    endpoint = DeviceMessageHTTPEndpoint(coordinator)
    endpoint.start()

    time.sleep(0.5)

    http_client = http.client.HTTPConnection("127.0.0.1:9331", timeout=2)

    yield (endpoint, coordinator, test_device, http_client)

    endpoint.stop()


def test_should_accept_a_message(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    http_client.request(
        "POST", "/",
        body=msgpack.packb({'type': 'msg_type', 'experiment_id': '123'}),
        headers={'Accept': 'application/msgpack'})
    response = http_client.getresponse()
    assert response.status == 200

    message = test_device.message_queue.get(timeout=2)
    assert message.type == 'msg_type'
    assert message.experiment_id == '123'
    assert message.stimulus_id is None
    assert message.payload is None


def test_type_is_mandatory(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    http_client.request(
        "POST", "/",
        body=msgpack.packb({'experiment_id': '123'}),
        headers={'Accept': 'application/msgpack'})
    response = http_client.getresponse()
    assert response.status == 400


def test_json(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    http_client.request(
        "POST", "/",
        body=json.dumps({'type': 'msg_type', 'experiment_id': '123',
                         'stimulus_id': 's8', 'payload': {'data': 100}}),
        headers={'Accept': 'application/json'})
    response = http_client.getresponse()
    assert response.status == 200

    message = test_device.message_queue.get(timeout=2)
    assert message.type == 'msg_type'
    assert message.experiment_id == '123'
    assert message.stimulus_id == 's8'
    assert message.payload == {'data': 100}


def test_pickle(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    http_client.request(
        "POST", "/",
        body=pickle.dumps({'type': 'msg_type', 'experiment_id': '123',
                           'stimulus_id': 's8', 'payload': {'data': 100}}),
        headers={'Accept': 'application/pickle'})
    response = http_client.getresponse()
    assert response.status == 200

    message = test_device.message_queue.get(timeout=2)
    assert message.type == 'msg_type'
    assert message.experiment_id == '123'
    assert message.stimulus_id == 's8'
    assert message.payload == {'data': 100}


def test_bad_content_type(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    http_client.request(
        "POST", "/",
        body=pickle.dumps({'type': 'msg_type', 'experiment_id': '123',
                           'stimulus_id': 's8', 'payload': {'data': 100}}),
        headers={'Accept': 'text'})
    response = http_client.getresponse()
    assert response.status == 400


def test_multiple_endpoints(fixture):
    endpoint, coordinator, test_device, http_client, = fixture

    endpoint2 = DeviceMessageHTTPEndpoint(coordinator, port=9334)
    endpoint2.start()

    http_client.request(
        "POST", "/",
        body=msgpack.packb({'type': 'msg_type', 'experiment_id': '123'}),
        headers={'Accept': 'application/msgpack'})
    response = http_client.getresponse()
    assert response.status == 200

    message = test_device.message_queue.get(timeout=2)
    assert message.type == 'msg_type'
    assert message.experiment_id == '123'
    assert message.stimulus_id is None
    assert message.payload is None

    http_client2 = http.client.HTTPConnection("127.0.0.1:9334", timeout=2)

    http_client2.request(
        "POST", "/",
        body=msgpack.packb({'type': 'msg_type2', 'experiment_id': 'ex2'}),
        headers={'Accept': 'application/msgpack'})
    response2 = http_client2.getresponse()
    assert response2.status == 200

    message = test_device.message_queue.get(timeout=2)
    assert message.type == 'msg_type2'
    assert message.experiment_id == 'ex2'
    assert message.stimulus_id is None
    assert message.payload is None
