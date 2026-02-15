.. _development:

***********
Development
***********

Installing from source
======================

you need `poetry`:

>>> pip3 install poetry

(Refer to `Poetry installation guide <https://python-poetry.org/docs/#installation>`_
for alternative ways of installing Poetry.)

Then `cd` to where the source code located and run:

>>> make install
>>> make build

It will create a virtual environment and installs `Octopus Sensing` with all its optional dependencies.

Coding Style
==============

We're following Python PEP 8 for our coding style.

For formatting the code, `autopep8 <https://github.com/hhatto/autopep8>`_ is a good tool.
Many editors support it. You can use it to automate the code formatting.

In-code Comments
~~~~~~~~~~~~~~~~~~~
Add comments to clarify *why* you did things this way. Usually, it's easy to figure out *what* a piece
of code does, but *why* is harder or impossible to figure out.

Also, add a comment for complex algorithms even if they are written very clearly.

Doc Strings
~~~~~~~~~~~~
Every public method or function should have doc string. We also generate our API Reference document
from these doc strings. So ensure they are clear and addresses all the functionality and exceptions
of a method. We are using `NumPy style <https://numpydoc.readthedocs.io/>` for creating doc strings.

Static Type Checking
======================

We use `mypy <http://www.mypy-lang.org/>`_ to type-check our sources. Every variable or parameter
in the source code should have a type, unless MyPy can automatically determine the type.

To run MyPy use our make file:

.. code-block:: bash

   $ make mypy


Tests
======
We're using `pytest <https://docs.pytest.org>`_ to run the tests. You can simply invoke the tests using:

.. code-block:: bash

   $ make test

There are two sets of tests: An integration test that checks the overall health of the library by running
a full scenario, and a lot of small unit tests that are testing functionalities individually.

All tests are located in `octopus-sensing/tests` directory.

Adding Support for a New Device
===============================

To add support for a new device, you need to create a subclass of `octopus-sensing.devices.device.Device`.

The device's code will be run in a separate process. Because Python is not good with threading, and also
because it minimizes the effect of other parts of the application on the data collection.

The Device process and the parent process (the Device Coordinator) talk with each other using Message Queues.

When implementing the `Device` class, you need to override `__init__` and `_run` methods.

In `__init__`, you will receive the required parameters. For example, if the device needs configuration options.
You also need to receive the same parameters as in the `Device` class (your base class) and pass them to your
base class using `super()`.

The `_run` method will be run in the separate process. You need to initialize the device here, and start
recording the data. At the same time, you need to check the messages in `self.message_queue`. So, usually,
you need to do your data recording in a separate thread, and check the messages in the main thread.

The following code can be used as a starting point for adding a device. And also have a look at the devices
currently implemented in Octopus Sensing for some sample codes.

.. code-block:: python

    import threading

    from octopus_sensing.common.message_creators import MessageType
    from octopus_sensing.devices.device import Device

    # We inherit from Device class
    class SampleDevice(Device):

        # 'name' and 'output_path' are from our parent, the Device class
        def __init__(self, config_flag, output_path, name=None):
            # Parent should always be called. It does some initialization of itself.
            # We're passing the parameters we received to it.
            super().__init__(name=name, output_path=output_path)

            # Keeping the config parameter
            self._config_flag = config_flag

            # Note that we don't do anything with the device here.
            # Everything should be done after the process is created,
            # in the _run method.

        # Note that this is '_run' and not 'run'!
        # You should never override 'run'.
        def _run(self):
            # Initialize your device here.
            self._device_handle = ...
            # Then we start a thread for recording the data.
            # We will use this flag to tell the thread to finish recording.
            self._record = True
            threading.Thread(target=self._record_data).start()

            # We're checking messages in the main thread.
            while True:
                # This will block until a message receives from the parent (the deivce coordinator)
                message = self.message_queue.get()
                if message.type == MessageType.TERMINATE:
                    # This will cause the recording thread to exit. (see its code)
                    self._record = False
                    # Exiting the main loop. It will cause the process to finish and terminate.
                    # (since there's nothing after this.)
                    break


        def _record_data(self):
            # This is running in another thread (see _run)
            # Do the actual data recording here.
            while self._record:
                data = self._device_handle.read()
                # Write it to a file for example.

            # Depending on the device, you might want to start recording data
            # when you received the START message in the message_queue, and
            # stop recording when you received the STOP message.

Publising to PyPi
======================

Before publishing to PyPi, it's a good idea to publish to `test.pypi.org` first to ensure
everything is working fine.

You need a separate account for `pypi.org` and `test.pypi.org`. Create an API token, and add it to Poetry:

.. code-block:: bash

   # Add test.pypi repository
   $ poetry config repositories.testpypi https://test.pypi.org/legacy/
   # Add your tokens
   $ poetry config pypi-token.pypi <your-token-here>
   $ poetry config pypi-token.testpypi <your-test-token-here>
   

Then follow these steps to publish a new version:

1. poetry check

2. update version in __init__.py and pyproject.toml

3. poetry build

4. Publish it to test.pypi first:

.. code-block:: bash
    
    $ poetry publish --repository testpypi

5. Install and test it from test.pypi:

.. code-block:: bash

    $ python3.12 -m venv .venv
    $ . .venv/bin/activate
    $ python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple octopus-sensing

6. If everything is fine, tag the version and publish it to PyPi:

.. code-block:: bash

   $ git commit
   $ git tag version
   $ git push --tags
   $ poetry publish

7. Create a new Release in GitHub and add the changes in the release notes.
