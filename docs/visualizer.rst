.. _octopus_sensing_visualizer:

***************************
Octopus Sensing Visualizer
***************************

Octopus Sensing Visualizer is a web-based real-time visualizer for `Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>`_. 
It can be used for offline data visualization. You can visualize the recorded multimodal data as the raw data. Also, it can extract
some essential features or components of data and display them in a single window. Using this tool, you can observe the effect of an event on recorded data simultaneously.

`Octopus Sensing Visualizer <https://github.com/octopus-sensing/octopus-sensing-visualizer>`_ is 
a separated project and can be installed if we need to visualize data. 
It can be used for displaying recorded data with
the same format as we recorded through Octopus Sensing.

**Note**

If we want to display data that is recorded by Octopus Sensing, 
we should apply :ref: `preprocessing` module to prepare data for the visualizer while we record data or later.



Installation
------------
It requires Python 3.7 or later.

You can use `pip` to install it:

>>> pip install octopus-sensing-visualizer

You can also use one of the Python package managers like `pipenv <https://pipenv.pypa.io/en/latest/>`_ or 
`poetry <https://python-poetry.org/>`_ to prevent package conflict.

>>> pipenv install octopus-sensing-visualizer

How to use it
--------------
At first, you should create an `octopus_sensing_visualizer_config.conf` in the current directory. 
This config file includes the path to the data and the type of graphs that we want to visualize.
See :ref:`visualizer_config_guide` to know how to prepare this file.

Then simply run the server by invoking `octopus-sensing-visualizer` from the command line.
For example, if you use `pipenv <https://pipenv.pypa.io/en/latest/>`_ as the package manager, run it as follows:

>>> pipenv run octopus-sensing-visualizer


The visualizer will listen on `8080` port. Open a web page and point to the machine's IP. For
example, in the same machine, open http://localhost:8080 . Or replace `localhost` with the machine's
IP and open it from any other machine.


Security notice
---------------
Note that the webserver accepts requests from any machine, and it uses `http` protocol, which
is not encrypted. Don't run it on a network that you don't trust.


How to prepare a config file
----------------------------
.. toctree::
   :maxdepth: 1
   
   visualizer_config_guide

Which data can be visualized
-----------------------------
It can be used for displaying recorded data using any software if the data is prepared with
the same format as we recorded through Octopus Sensing.

**EEG** : 
A CSV file with 16 columns for 16 channels. The number of rows shows the number of samples.

**GSR**: 
A CSV file with one column. The number of rows shows the number of samples.

**PPG**: 
A CSV file with one column. The number of rows shows the number of samples.


User interface
--------------
The user interface includes graphs with True value in the config file. 
Also, it has a slide bar that allows us to go forward and backward in data samples.
There is a text box for setting window size. This window size shows the length of the horizontal axis in time.
Setting the bigger values leads to displaying a wider window of data in each moment and so fewer details. 
The sliding bar is moving each second, and all graphs will be updated in each second. 

Copyright
---------

Copyright © 2021 [Nastaran Saffaryazdi]

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See `License file <https://github.com/nastaran62/octopus-sensing/blob/master/LICENSE>`_  for full terms.