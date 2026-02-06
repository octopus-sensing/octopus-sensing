.. _octopus_sensing_monitoring:

***************************
Octopus Sensing Monitoring
***************************

A web-based real-time monitoring for `Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>`_. You can
monitor your data from any machine in the same network.

`Octopus Sensing monitoring <https://github.com/octopus-sensing/octopus-sensing-monitoring>`_ is
a separated project and can be installed for Octopus Sensing if we need monitoring features.


Installation
------------

It required Python 3.7 or later. And it needs to be installed on the same machine where `Octopus
Sensing` is running.

You can use `pip` to install it:

.. code-block:: bash

   $ pip install octopus-sensing-monitoring


Then simply run it by invoking `octopus-sensing-monitoring` from the command line.

You can also use one of the Python package managers like `pipenv <https://pipenv.pypa.io/en/latest/>`_
or `poetry <https://python-poetry.org/>`_ to prevent package conflict.

.. code-block:: bash

   $ pipenv install octopus-sensing-monitoring
   $ pipenv run octopus-sensing-monitoring


The monitoring will listen on `8080` port. Open a web page and point to the machine's IP. For
example, in the same machine, open http://localhost:8080 . Or replace `localhost` with the machine's
IP and open it from any other machine.

Starting endpoint in your code
------------------------------

In the code that running Octopus Sensing, you need to start the monitoring endpoint as well. To do so, add this to your code:

>>> from octopus_sensing.device_coordinator import DeviceCoordinator
>>> from octopus_sensing.monitoring_endpoint import MonitoringEndpoint
>>> # Create coordinator instance
>>> coordinator = DeviceCoordinator()
>>> # Add your devices
>>> ...
>>> # Creating the endpoint instance and start it.
>>> monitoring_endpoint = MonitoringEndpoint(coordinator)
>>> monitoring_endpoint.start()
>>> ...
>>> # It's a good idea to stop it after your software terminated.
>>> monitoring_endpoint.stop()


Testing with fake data
----------------------

For testing purposes, you can ask the server to generate fake data instead of fetching data from
`Octopus Sensing`. To do so, add `--fake` flag when running the script:

.. code-block:: bash

   $ octopus-sensing-monitoring --fake

Naming your devices
-------------------

In `Octopus Sensing`, when you're creating an instance of devices, you need to provide a `name`. At the
moment, device names are hard coded in this monitoring app. So you need to use these names for your
devices in order for them to appear on the web page.

* For OpenBCIStreaming or BrainFlowOpenBCIStreaming use `eeg` (i.e. `OpenBCIStreaming(name="eeg", ...)` )
* For Shimmer3Streaming use `shimmer`
* For the camera, you need to create instance of `CameraStreaming` and name it `webcam`

Security notice
---------------

Note that the webserver accepts requests from any machine, and it uses `http` protocol, which
is not encrypted. Don't run it on a network that you don't trust.

**Copyright**

Copyright © 2020,2026 `Aidin Gharibnavaz <https://aidinhut.com>`

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See `License file <LICENSE>` for full terms.
