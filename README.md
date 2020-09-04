Octopus Sensing
===============

A tool to help you run scientific experiments that involves recording data synchronously from
multiple sources. You write steps of an experiment scenario, for example showing a stimuli and then
a questionnaire, and the tool takes care of the rest.

It can collect data from devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG), Video
and Audio, etc. Data collection can be start and stop synchronously across all devices, and
collected data will be tagged with the timestamp of start and stop of the experiment, the ID of the
experiment, etc.

The aim is to make the scripting interface so simple that people with minimum or no software
development skills can define experience scenarios with no effort.


#### Main features

* Controls data recording from multiple sources using a simple unified interface
* Ability to tag an event on all the collected data (such as start of a experiment, and event during
the experiment, etc)
* Can show stimulies (images and videos) and questionnaries
* Monitoring interface that visualizes collected data in real-time

Getting Strated
---------------

#### requirements

You need [Python](https://python.org) installed on your computer (version 3.7 or higher). Refer to
[this guide](https://realpython.com/installing-python/) if you need help.

#### Quick start Using init script (Linux & Mac)

Octopus Sensing comes with a script that helps you quickly start a project. It uses
[Pipenv](https://pipenv.pypa.io/) to create a [virtual
environment](https://docs.python.org/3/tutorial/venv.html) in order to keep everything clean. It
will also create a sample application.


```
mkdir my-awesome-project
cd my-awesome-project
curl... | sudo bash...
```

The created `main.py` file is a sample application. To run it:

```
pipenv run python main.py
```

If you don't want to use the script, you can use following methods instead.

#### Installation using pip

You can use `pip` to install `octopus-sensing` as simple as:

```
pip3 install octopus-sensing
```

(You might need to replace `pip3` with `pip` depending on your system.)

Then it can be imported like:

```python
import octopus_sensing
```

We recommend using a package manager like [Pipenv](https://pipenv.pypa.io/) instead of globally install it using `pip` to prevent package conflicts.

#### Installation from source

If you want to compile it from source for development purposes or to have the un-released features,
please refer to [Development Guide](docs/Development.md).

Tutorial
--------

See [Tutorial](docs/Tutorial.md) to learn how to use Octopus Sensing.

Troubleshooting
---------------
If the installaion failed, and this error is in the logs:

```fatal error: portaudio.h: No such file or directory```

You need to install `portaudio` package on your system. On a debian-based linux the package called `portaudio19-dev`.

Copyright
---------
Copyright © 2020 Nastaran Saffaryazdi

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See [License file](LICENSE) for full terms.
