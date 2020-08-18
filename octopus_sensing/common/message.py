# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Zahra Saffaryazdi 2020
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

class Message():
    '''
    Message class
    '''
    def __init__(self, message_type, payload,
                 subject_id=None, stimulus_id=None):
        '''
        Initializes the message object

        @param str message_type: The type of message
        @param payload: the message data that can have differnt values

        @keyword str subject_id: subject's ID
        @keyword str stimulus_id: stimulus's ID
        '''
        self.message_type = message_type
        self.payload = payload
        self.subject_id = subject_id
        self.stimulus_id = stimulus_id
