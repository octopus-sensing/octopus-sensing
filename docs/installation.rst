.. _installation:

************
Installation
************

Octopus Sensing supports multiple device modules. Because everyone might not need all the
modules, they are not installed by default. You can install only the modules you need.

When you install `octopus-sensing` package, only the core package is installed. You need to
install the device modules you need separately.

Pre-requirements
==================

Some devices need additional system dependencies to be installed on your machine.

`stimuli`, `windows`, and `gui` modules (for scenario designing) need the following dependencies:

On Debian-based Gnu/Linux distributions (like Ubuntu), run:

:code:`sudo apt-get install libcairo2-dev libgirepository1.0-dev`

On MacOS, you can use `brew` to install the dependencies:

:code:`brew install cairo pygobject3`

`camera` (for video recording) module needs `gstreamer` package. Use one of the following commands to install it.

:code:`sudo apt-get install gstreamer-1.0`  (for Debian-based Gnu/Linux distributions)

:code:`brew install gstreamer` (for MacOS)


`lsl` (for Lab Streaming Layer support) module needs `liblsl` package. Refer to its official documentation:
`liblsl <https://github.com/sccn/liblsl>`_.


Installation using Pipenv (All Platforms)
=========================================

We recommend using a package manager like `Pipenv <https://pipenv.pypa.io/>`_ or a virtual environment instead of
globally installing Octopus Sensing using `pip` to prevent package conflicts. To do so, follow these commands.
(This is same as what the :ref:`quick_start` script does.)


.. code-block:: bash

    mkdir my-awesome-project
    cd my-awesome-project
    # Or replace it with your python version
    pipenv --python python3.12
    pipenv install octopus-sensing


This installs Octopus Sensing inside the virtual environment created by Pipenv. You need to use
`pipenv` to run your code. For example:

:code:`pipenv run python main.py`

The `octopus-sensing` package is only the core module. To install device modules, use the following command:

.. code-block:: bash

    pipenv install octopus-sensing[<device_module_name>,<another_device_module_name>,...]
    # Example:
    pipenv install octopus-sensing[camera,brainflow]


Refer to `Pipenv website <https://pipenv.pypa.io/>`_ for more info.

Installation using Poetry (All Platforms)
=========================================

You can also use `Poetry <https://python-poetry.org/>`_ to manage your dependencies and virtual environment. To do so, follow these commands:

.. code-block:: bash

    mkdir my-awesome-project
    cd my-awesome-project
    poetry init  # Follow the prompts to create pyproject.toml
    # Or if you want to use a specific python version, run `poetry env use python3.12` before the next command
    poetry add octopus-sensing

This installs Octopus Sensing inside the virtual environment created by Poetry. You can use `poetry run` to run your code. For example:

:code:`poetry run python main.py`

The `octopus-sensing` package is only the core module. To install device modules, use the following command:

.. code-block:: bash

    poetry run pip install "octopus-sensing[<device_module_name>,<another_device_module_name>,...]"
    # Example:
    poetry run pip install ".[camera,brainflow]"

Refer to `Poetry website <https://python-poetry.org/>`_ for more info.

Virtual environment (All Platforms)
===================================

We highly recommend using a virtual environment to keep your global Python environment clean. You can also use a
package manager (see next sections) that creates a virtual environment and handles dependencies for you.

In this section, we use `venv <https://docs.python.org/3/library/venv.html>`_ from Python's standard library to create
a virtual environment. Create a directory for your project and run the following commands:

.. code-block:: bash

    mkdir my-awesome-project
    cd my-awesome-project
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

On Windows, you might need to use `python` and `pip` commands instead of `python3` and `pip3`.

Now you can use `pip` to install `octopus-sensing` and its device modules inside this virtual environment:

.. code-block:: bash

    pip install octopus-sensing

For intalling device modules, use the following command:

.. code-block:: bash

    pip install octopus-sensing[<device_module_name>,<another_device_module_name>,...]
    # Example:
    pip install octopus-sensing[camera,brainflow]

To see a list of available device modules, see :ref:`installation#available-device-modules`.


Installation using pip (All Platforms)
======================================

You can use `pip` to install `octopus-sensing` globally (not recommended) as simple as:

.. code-block:: bash
    pip3 install octopus-sensing

(You might need to replace `pip3` with `pip` depending on your system.)

Then it can be imported like:

:code:`import octopus_sensing`

To install optional device modules, use the following command:

.. code-block:: bash

    pip install octopus-sensing[<device_module_name>,<another_device_module_name>,...]
    # Example:
    pip install octopus-sensing[camera,brainflow]


Installation from source (All Platforms)
========================================

If you want to compile it from source for development purposes or to have the un-released features,
please refer to :ref:`development`.

Troubleshooting
===============

- Pip cannot install PyGObject on Windows. If users want to use `octopus-sensing.stimuli` or `octopus-sensing.windows` packages, they need to install it manually themselves. See `PyGObject documentation <https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started>`_ to know how to install PyGObject on Windows.

- If you saw `Namespace Gst not available` (or similar) while importing `octopus_sensing.stimuli` package, you need to install `gstreamer` package on your machine. On Ubuntu run `sudo apt-get install gstreamer-1.0`.

Available Device Modules
========================

The following devices are installed along with the core package:

- :mod:`openvibe <octopus_sensing.devices.open_vibe_streaming>`: For OpenViBE acquisition server support
- :mod:`socket network device <octopus_sensing.devices.network_devices.socket_device>`: For sending triggers to other softwares via socket connection
- :mod:`http network device <octopus_sensing.devices.network_devices.http_device.HttpNetworkDevice>`: For sending triggers to other softwares via HTTP requests
- :mod:`test device <octopus_sensing.devices.testdevice_streaming>`: A simulated device for testing purposes

The following device modules are available. You can install them using `pip` or `pipenv` as shown above.

- :mod:`shimmer3 <octopus_sensing.devices.shimmer3_streaming>`: For Shimmer3 GSR and PPG sensor support
- :mod:`camera <octopus_sensing.devices.camera_streaming>`: For video recording using your computer's camera
- :mod:`brainflow <octopus_sensing.devices.brainflow_streaming>`: For supporting multiple biosensors supported by BrainFlow library
- :mod:`openbci <octopus_sensing.devices.openbci_streaming>`: (Deprecated. Use BrainFlow instead) For OpenBCI EEG headset support
- :mod:`audio <octopus_sensing.devices.audio_streaming>`: For audio recording from microphone
- :mod:`lsl <octopus_sensing.devices.lsl_streaming>`: For Lab Streaming Layer support
- :mod:`tobiiglasses <octopus_sensing.devices.tobiiglasses_streaming>`: For Tobii Glasses eye-tracker support
- gui: For all GUI components: :ref:`stimuli <stimuli>`, :ref:`windows <windows>`, and :ref:`questionnaire <questionnaire>`
