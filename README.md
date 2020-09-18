Octopus Sensing
===============

![Travis status](https://img.shields.io/travis/com/nastaran62/octopus-sensing)
![Coveralls status](https://img.shields.io/coveralls/github/nastaran62/octopus-sensing)
![PyPI - Version](https://img.shields.io/pypi/v/octopus-sensing)
![PyPI - License](https://img.shields.io/pypi/l/octopus-sensing)

A tool to help you run scientific experiments that involve recording data synchronously from
multiple sources. You write steps of an experiment scenario, for example showing a stimulus and then
a questionnaire. The tool takes care of the rest.

It can collect data from multiple devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG),
Video and Audio, etc. Data collection can be started and stopped synchronously across all devices.
Collected data will be tagged with the timestamp of the start and stop of the experiment, the ID of
the experiment, etc.

The aim is to make the scripting interface so simple that people with minimum or no software
development skills can define experience scenarios with no effort.

#### Main features

* Controls data recording from multiple sources using a simple unified interface
* Tags an event on collected data, such as the start of an experiment, and events during the experiment, etc.
* Can show stimuli (images and videos) and questionnaires
* Monitoring interface that visualizes collected data in real-time

Getting Started
---------------

#### requirements

You need [Python](https://python.org) installed on your computer (version 3.7 or higher). Refer to
[this guide](https://realpython.com/installing-python/) if you need help.

#### Quickstart Using init script (Linux & Mac)

Octopus Sensing comes with a script that helps you quickly start a project. It uses
[Pipenv](https://pipenv.pypa.io/) to create a [virtual
environment](https://docs.python.org/3/tutorial/venv.html) in order to keep everything clean. It
will also create a sample application.


```
mkdir my-awesome-project
cd my-awesome-project
curl https://raw.githubusercontent.com/nastaran62/octopus-sensing/master/init_script/init.sh
# It's a good idea to read any script before executing it.
sudo bash ./init.sh
rm ./init.sh
```

The created `main.py` file is a sample application. To run it:

```
pipenv run python main.py
```

If you don't want to use the script, you can use the following methods instead.

#### Installation using Pipenv

We recommend using a package manager like [Pipenv](https://pipenv.pypa.io/) instead of globally
installing Octopus Sensing using `pip` to prevent package conflicts. To do so, follow these
commands. (This is same as what the above script does.)

```bash
mkdir my-awesome-project
cd my-awesome-project
# Or replace it with your python version
pipenv --python python3.8
pipenv install octopus-sensing
```

It installs Octopus Sensing inside the virtual environment created by Pipenv. You need to use
`pipenv` to run your code. For example:

```bash
pipenv run python main.py
```

Refer to [Pipenv website](https://pipenv.pypa.io/) for more info.

#### Installation using pip

You can use `pip` to install `octopus-sensing` as simple as:

```bash
pip3 install octopus-sensing
```

(You might need to replace `pip3` with `pip` depending on your system.)

Then it can be imported like:

```python
import octopus_sensing
```

#### Installation from source

If you want to compile it from source for development purposes or to have the un-released features,
please refer to [Development Guide](https://octopus-sensing.nastaran-saffar.me/development).

Tutorial
--------

See [Tutorial](https://octopus-sensing.nastaran-saffar.me/tutorial) to learn how to use Octopus Sensing.

Troubleshooting
---------------
If the installation failed, and this error is in the logs:

```fatal error: portaudio.h: No such file or directory```

You need to install `portaudio` package on your system. On a debian-based linux the package called
`portaudio19-dev`.

Copyright
---------
Copyright © 2020 Nastaran Saffaryazdi

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See [License file](https://github.com/nastaran62/octopus-sensing/blob/master/LICENSE) for full terms.
