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

Note that the script only installs Camera module. See :ref:`installation` to learn how to install other device
modules.

If you don't want or can't use the script, see :ref:`installation`. It includes a troubleshooting section.
