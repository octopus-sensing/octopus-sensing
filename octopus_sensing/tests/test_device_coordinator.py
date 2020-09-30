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

from octopus_sensing.device_coordinator import MonitoringCache

def test_monitoring_cache():
    cache = MonitoringCache()

    data = [1, 2, 3]

    cache.cache(data)

    time.sleep(0.06)
    assert cache.get_cache() == data

    time.sleep(0.05)
    assert cache.get_cache() is None
