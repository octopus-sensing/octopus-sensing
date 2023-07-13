<h2 align="center">Octopus Sensing</h2>
<p align="center">
  <img src="https://octopus-sensing.nastaran-saffar.me/_static/octopus-sensing-logo-small.png" alt="Octopus Sensing Logo">
</p>
<p align="center">
  <img src="https://img.shields.io/github/workflow/status/octopus-sensing/octopus-sensing/Python%20Check?label=checks" alt="GitHub Workflow Status">
  <img src="https://img.shields.io/codecov/c/gh/octopus-sensing/octopus-sensing" alt="Codecov">
  <img src="https://img.shields.io/pypi/v/octopus-sensing" alt="PyPI">
  <img src="https://img.shields.io/pypi/l/octopus-sensing" alt="PyPI - License">
</p>

Octopus Sensing is a tool to help you run scientific experiments that involve recording data synchronously from
multiple sources in human-computer interaction studies. You write steps of an experiment scenario, for example showing a stimulus and then a questionnaire. The tool takes care of the rest.

It can collect data from multiple devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG),
Video and Audio and so forth simultaneously. Data collection can be started and stopped synchronously across all devices.
Collected data will be tagged with the timestamp of the start and stop of the experiment, the ID of
the experiment, etc.

The aim is to make the scripting interface so simple that people with minimum or no software
development skills can define experiment scenarios with no effort.
Also, this tool can be used as the base structure for creating real-time data processing systems like systems with capabilities of recognizing emotions, stress, cognitive load, or analyzing human behaviors.


**To see the full documentation visit the [Octopus Sensing website](https://octopus-sensing.nastaran-saffar.me/).**

When using the package in your research, please cite:
-----------------------------------------------------

Saffaryazdi, N., Gharibnavaz, A., & Billinghurst, M. (2022). Octopus Sensing: A Python library for human behavior studies. Journal of Open Source Software, 7(71), 4045.

Main features
--------------

* Controls data recording from multiple sources using a simple unified interface
* Tags an event on collected data, such as the start of an experiment, and events during the experiment, etc.
* Can show stimuli (images and videos) and questionnaires
* Monitoring interface that visualizes collected data in real-time
* Offline visualization of data from multiple sources simultanously

Copyright
---------
Copyright © 2020-2023 Nastaran Saffaryazdi, Aidin Gharibnavaz

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

See [License file](https://github.com/nastaran62/octopus-sensing/blob/master/LICENSE) for full terms.
