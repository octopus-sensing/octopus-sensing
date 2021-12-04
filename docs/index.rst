.. image:: _static/octopus-sensing-logo-small.png
   :alt: Octopus Sensing Logo

Octopus Sensing
====================================================================================

**Welcome to Octopus Sensing's documentation!**

Octopus Sensing is a tool to help you run scientific experiments that involve recording data synchronously from
multiple sources in human-computer interaction studies. You write steps of an experiment scenario, for example showing a stimulus and then
a questionnaire. The tool takes care of the rest.

It can collect data from multiple devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG),
Video and Audio and so forth simultaneously. Data collection can be started and stopped synchronously across all devices.
Collected data will be tagged with the timestamp of the start and stop of the experiment, the ID of
the experiment, etc.

The aim is to make the scripting interface so simple that people with minimum or no software
development skills can define experiment scenarios with no effort. 
Also, this tool can be used as the base structure for creating real-time data processing systems like systems with capabilities of recognizing emotions, stress, cognitive load, or analyzing human behaviors.

Main features
~~~~~~~~~~~~~

* Controls data recording from multiple sources using a simple unified interface
* Tags an event on collected data, such as the start of an experiment, and events during the experiment, etc.
* Can show stimuli (images and videos) and questionnaires
* Monitoring interface that visualizes collected data in real-time
* Offline visualization of data from multiple sources simultaneously 

Quick Start
=========== 
See :ref:`quick_start` to learn how to install Octopus Sensing.

Tutorial
========
See :ref:`tutorial` to learn how to use Octopus Sensing.

API Reference
=============
See :ref:`api_reference` for the complete documentation of all the public classes and methods available in Octopus Sensing.

Copyright
=========
Copyright © 2020 Nastaran Saffaryazdi, Aidin Gharibnavaz

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See `License file <https://github.com/nastaran62/octopus-sensing/blob/master/LICENSE>`_ for full terms.



Content
========

.. toctree::
   :maxdepth: 3
   :caption: .

   quick_start
   tutorial
   api_reference
   development
   visualizer
   monitoring