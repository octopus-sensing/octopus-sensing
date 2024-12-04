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
import io
import http.server
import pickle
import json
import urllib.parse

from typing import Callable, Optional, Any, Dict, List

import msgpack
import numpy


class EndpointClientError(Exception):
    pass

class _NumpyJSONEncoder(json.JSONEncoder):
    """Helper class for encoding Numpy types to JSON"""
    def default(self, obj):
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
                            numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
                            numpy.uint16, numpy.uint32, numpy.uint64)):
            return int(obj)
        elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32,
                              numpy.float64)):
            return float(obj)
        elif isinstance(obj, (numpy.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def _numpy_msgpack_encoder(obj):
    """Helper function for encoding Numpy types to msgpack"""
    if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
                        numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
                        numpy.uint16, numpy.uint32, numpy.uint64)):
        return int(obj)
    elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32,
                          numpy.float64)):
        return float(obj)
    elif isinstance(obj, (numpy.ndarray,)):
        return obj.tolist()
    return obj


def make_handler(get_callback: Optional[Callable[[io.BufferedIOBase], Any]], post_callback: Optional[Callable[[Any], Any]]):
    class Handler(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            if get_callback is None:
                self.send_error(
                    400,
                    message="This endpoint does not support GET requests")
                self.end_headers()
                return

            query_string = urllib.parse.urlparse(self.path).query
            if query_string:
                query_params = urllib.parse.parse_qs(query_string)
            else:
                query_params = {}

            try:
                response = get_callback(self.rfile, query_params)
            except EndpointClientError as client_error:
                self.send_error(
                    400,
                    message=client_error.message)
                self.end_headers()
                return

            encoding_type = self.headers.get("Accept")
            if encoding_type is None or "pickle" in encoding_type:
                serialized_response = pickle.dumps(response)
            elif "json" in encoding_type:
                serialized_response = json.dumps(response, cls=_NumpyJSONEncoder).encode('UTF-8')
            elif "msgpack" in encoding_type:
                serialized_response = msgpack.packb(response, default=_numpy_msgpack_encoder)
            else:
                self.send_error(
                    400,
                    message="Unknown content type. Should be one of 'json', 'msgpack', or 'pickle'")
                self.end_headers()
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(serialized_response)

        def do_POST(self):
            if post_callback is None:
                self.send_error(
                    400,
                    message="This endpoint does not support POST requests")
                self.end_headers()
                return

            content_length = int(self.headers.get("Content-Length", "-1"))
            serialized_body = self.rfile.read(content_length)

            encoding_type = self.headers.get("Accept")
            if encoding_type is None or "pickle" in encoding_type:
                body = pickle.loads(serialized_body)
            elif "json" in encoding_type:
                body = json.loads(serialized_body)
            elif "msgpack" in encoding_type:
                body = msgpack.unpackb(serialized_body)
            else:
                self.send_error(
                    400,
                    message="Unknown content type. Should be one of 'json', 'msgpack', or 'pickle'")
                self.end_headers()
                return

            try:
                response = post_callback(body)
            except EndpointClientError as client_error:
                self.send_error(
                    400,
                    message=str(client_error))
                self.end_headers()
                return

            # We already check that encoding_type is one of these values
            if encoding_type is None or "pickle" in encoding_type:
                serialized_response = pickle.dumps(response)
            elif "json" in encoding_type:
                serialized_response = json.dumps(response).encode('UTF-8')
            elif "msgpack" in encoding_type:
                serialized_response = msgpack.packb(response)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(serialized_response)

    return Handler


class EndpointBase(threading.Thread):

    def __init__(self, endpoint_name: str, port: int, get_callback: Optional[Callable[[io.BufferedIOBase, Dict[str, List[Any]]], Any]] = None, post_callback: Optional[Callable[[Any], Any]] = None):
        '''
        This class shouldn't be used directly. Use one of the implementations instead.

        Parameters
        ----------
        get_callback : Function
                       This will be called when a GET request received by the endpoint.
                       It should accept one parameter, which is a io.BufferedIOBase
                       containing the request's body.
        post_callback : Function
                        This will be called when a POST request received by the endpoint.
                        It should accept one parameter, which is the deserialized version
                        of the request's body.

        Notes
        -----
        If callbacks raise EndpointClientError, it will be send back to the client as a
        BadRequest status.
        '''
        super().__init__(daemon=True, name=endpoint_name)
        self._server = None
        self._port = port
        self._get_callback = get_callback
        self._post_callback = post_callback

    def run(self):
        try:
            self._server = http.server.ThreadingHTTPServer(
                ('0.0.0.0', self._port), make_handler(self._get_callback, self._post_callback))
            self._server.serve_forever()
        except Exception as ex:
            print("Error in {}".format(self.name), file=sys.stderr)
            traceback.print_exc()

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server = None
