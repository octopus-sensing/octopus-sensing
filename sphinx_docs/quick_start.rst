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
    curl https://raw.githubusercontent.com/nastaran62/octopus-sensing/master/init_script/init.sh
    # It's a good idea to read any script before executing it.
    sudo bash ./init.sh
    rm ./init.sh


The created `main.py` file is a sample application. To run it:

:code:`pipenv run python main.py`


If you don't want to use the script, you can use the following methods instead.

Installation using Pipenv
=========================

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

Installation using pip
======================

You can use `pip` to install `octopus-sensing` as simple as:

:code:`pip3 install octopus-sensing`

(You might need to replace `pip3` with `pip` depending on your system.)

Then it can be imported like:

:code:`import octopus_sensing`


Installation from source
========================

If you want to compile it from source for development purposes or to have the un-released features,
please refer to `Development Guide <https://octopus-sensing.nastaran-saffar.me/development>`_.

Troubleshooting
===============
If the installation failed, and this error is in the logs:

```fatal error: portaudio.h: No such file or directory```

You need to install `portaudio` package on your system. On a debian-based linux the package called
`portaudio19-dev`.
