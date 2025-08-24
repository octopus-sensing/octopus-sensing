.. _quick_start:

***********
Quick start
***********

requirements
============

You need `Python <https://python.org>`_ installed on your computer (version 3.7 or higher). Refer to
`this guide <https://realpython.com/installing-python/>`_ if you need help.

Quickstart Using init script (Linux & Mac)
==========================================

Octopus Sensing comes with a script that helps you quickly start a project. It uses
`Pipenv <https://pipenv.pypa.io/>`_ to create a `virtual
environment <https://docs.python.org/3/tutorial/venv.html>`_ in order to keep everything clean. It
will also create a sample application.


.. code-block:: bash

    mkdir my-awesome-project
    cd my-awesome-project
    curl --output init.sh https://raw.githubusercontent.com/nastaran62/octopus-sensing/master/init_script/init.sh
    # It's a good idea to read any script before executing it.
    bash ./init.sh
    rm ./init.sh


The created `main.py` file is an example application. To run it:

:code:`pipenv run python main.py`


If you don't want to use the script, you can use the following methods instead.

Pre-requirements
==================

If you're using Gnu/Linux, you need to install a few packages on your machine. On an Ubuntu distro, run:

:code:`sudo apt-get install libcairo2-dev libgirepository1.0-dev gstreamer-1.0`

You also need to install [liblsl](https://github.com/sccn/liblsl).

For Mac OS, you can use `brew` to install the dependencies:

:code:`brew install cairo pygobject3 labstreaminglayer/tap/lsl`


Installation using Pipenv (All Platforms)
=========================================

We recommend using a package manager like `Pipenv <https://pipenv.pypa.io/>`_ instead of globally
installing Octopus Sensing using `pip` to prevent package conflicts. To do so, follow these
commands. (This is same as what the above script does.)


.. code-block:: bash

    mkdir my-awesome-project
    cd my-awesome-project
    # Or replace it with your python version
    pipenv --python python3.8
    pipenv install octopus-sensing



It installs Octopus Sensing inside the virtual environment created by Pipenv. You need to use
`pipenv` to run your code. For example:

:code:`pipenv run python main.py`


Refer to `Pipenv website <https://pipenv.pypa.io/>`_ for more info.

Installation using pip (All Platforms)
======================================

You can use `pip` to install `octopus-sensing` as simple as:

:code:`pip3 install octopus-sensing`

(You might need to replace `pip3` with `pip` depending on your system.)

Then it can be imported like:

:code:`import octopus_sensing`


Installation from source (All Platforms)
========================================

If you want to compile it from source for development purposes or to have the un-released features,
please refer to :ref:`development`.

Troubleshooting
===============

- Pip cannot install PyGObject on Windows. If users want to use `octopus-sensing.stimuli` or `octopus-sensing.windows` packages, they need to install it manually themselves. See `PyGObject documentation <https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started>`_ to know how to install PyGObject on Windows.

- If you saw `Namespace Gst not available` (or similar) while importing `octopus_sensing.stimuli` package, you need to install `gstreamer` package on your machine. On Ubuntu run `sudo apt-get install gstreamer-1.0`.
