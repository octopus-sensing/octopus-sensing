---
title: 'Octopus-sensing: A python library for human behavior studies'
tags:
 - Python
 - Javascript
 - Human-Computer-Interaction(HCI)
 - Human behavior research
 - Physiological Signals
 - Electroencephalography
 - Multimodal Sensors
 - Synchronous data acquisition
 - Data visuaization
 - Affective Computing
 - Experimental design
 
authors:
 - name: Nastaran Saffaryazdi
   orcid: 0000-0002-6082-9772
   affiliation: 1
 - name: Aidin Gharibnavaz
   orcid: 0000-0001-6482-3944
   affiliation: 3
 - name: Mark Billinghurst
   orcid: 0000-0003-4172-6759
   affiliation: 1, 2
affiliations:
- name: Empathic Computing Laboratory, Auckland Bioengineering Institute, University of Auckland
  index: 1
- name: Empathic Computing Laboratory, University of South Australia
  index: 2
- name: Independent Researcher
  index: 3
date: 1 December 2021
bibliography: paper.bib
 
---
 
# Summary
Designing user studies and collecting data is critical to exploring and automatically recognizing human behavior. It is currently possible to use a range of sensors to capture heart rate, brain activity, skin conductance, and a variety of different physiological cues [@seneviratne2017survey]. These data can be combined to provide information about a user's emotional state [@egger2019emotion; @dzedzickis2020human], cognitive load [@vanneste2020towards; @mangaroska2021exploring], or other factors. However, even when data are collected correctly, synchronizing data from multiple sensors is time-consuming and prone to errors. Failure to record and synchronize data is likely to result in errors in analysis and results, as well as the need to repeat the time-consuming experiments several times.
To overcome these challenges, `Octopus Sensing` facilitates synchronous data acquisition from various sources and provides some utilities for designing user studies, real-time monitoring, and offline data visualization. The primary aim of `Octopus Sensing` is to provide a simple scripting interface so that people with basic or no software development skills can define sensor-based experiment scenarios with less effort.
 
# Statement of need
Several changes occur in the body and mind due to various internal and external stimuli. Nowadays, researchers use various sensors to measure and monitor these responses to determine an individual's state [@kreibig2010autonomic; @chen2020physiological; @sun2020multimodal] and to assist patients [@hassouneh2020development] or monitor mental health [@africa2020psychiatry]. Monitoring and analyzing human responses can be used to improve social interactions [@verschuere2006psychopathy; @hossain2019observers] and improve quality of life by creating intelligent devices such as Intelligent Tutoring Systems [@dewan2019engagement], creating adaptive systems [@aranha2019adapting], or creating interactive robots and virtual characters [@val2020affective; @hong2020multimodal].
 
Researchers have recently attempted to gain a deeper understanding of humans by simultaneously studying physiological and behavioral changes in the human body [@shu2018review; @koelstra2011deap]. Acquiring and analyzing data from different sources with various hardware and software is complex, time-consuming, and challenging. Additionally, synchronously recording data in multiple formats can be easily affected by human error. These tasks slow down the pace of progress in human-computer interaction and human behavior research.  
 
There are only a few frameworks that support synchronous data acquisition and design. [iMotions](https://imotions.com/) has developed software for integrating and synchronizing data recording through a wide range of various sensors and devices. Despite having many great features, iMotions is commercial software and not open-source. In contrast, there are a few open-source programs for conducting human studies. [Psychopy](https://www.psychopy.org/) is a powerful open-source, cross-platform software that is mainly used for building experiments' pipelines in behavioral science with visual and auditory stimuli. It can also record data and send the triggers to a few devices software that record human responses. Another effort in this area is [LabStreamingLayer (LSL) LabRecorder](http://labstreaminglayer.org/). Although, LSL LabRecorder provides synchronized, multimodal streaming through a wide range of devices, an extra application still needs to be run for acquiring data from each sensor separately.

`Octopus Sensing` is a lightweight open-source multi-platform library that facilitates synchronous data acquisition from various sources through a unified software and could be easily extended to process and analyze data in real-time. We designed the 'Octopus Sensing` library to minimize the effect of network failure in synchronous data streaming and reduce the number of applications that we should run for data streaming through different devices. Rather than creating a standalone software or framework, we created a library that could be easily integrated with other applications. Octopus Sensing provides a real-time monitoring system for illustrating and monitoring signals remotely using a web-based platform. The system also provides offline data visualization to see various human responses at the same time.
 
# Overview
 
Octopus Sensing is a tool to help in running scientific experiments that involve recording data synchronously from multiple sources. It can simultaneously collect data from various devices such as [OpenBCI EEG headset](https://openbci.com/), [Shimmer3 sensor](https://shimmersensing.com), camera, and audio-recorder without running another software for data recording. Data recording can be started, stopped, and triggered synchronously across all devices through a unified software. 

The main features of `Octopus Sensing` are listed as follows:

* Manages data recording from multiple sources using a simple unified interface.
* Minimizes human errors from manipulating data in synchronous data collection.
* Provides some utilities for designing studies like showing different stimuli or designing questionnaires.
* Offers a monitoring interface that prepares and visualizes collected data in real-time.
* Provides offline visualization of data from multiple sources simultaneously.

# Methodology
Octopus Sensing synchronizes data recording by using `multiprocessing` in Python. It creates a message queue and a process with three threads for every device by creating the device's instance. The main thread handles the message queue. One thread is responsible for data streaming and reacording, and the other thread listens on a queue and when received a request, returns the last three second of data from a buffer. This data can be used in real-time monitoring, or real-time processing and creating real-time feedbacks.  The `Device Coordinator` sends different triggers such as the start of recording or end of recording to different devices by putting the message in all devices' queue. The `Device Coordinator` also sends the trigger over the network for devices that are not embedded in the Octopus Sensing. 
<p align="center">
  <img src="https://github.com/octopus-sensing/octopus-sensing/blob/paper-review/docs/_static/OCS-diagram.png" alt="Ovrall view of Octopus Sensing">
</p>
 
# Research perspective
 
We have used `Octopus Sensing` to design several human emotion recognition experiments. We designed the experiments and recorded facial video, brain activity, and physiological signals using `Octopus Sensing` in a watching video task to recognize emotion [@Saffaryazdi2021]. This scenario which is common in physiological emotion recognition studies has been included in the repository as an example and explained in the tutorial. In another research study, we collected multimodal data in a face-to-face conversation task to analyze human emotional responses [@Saffaryazdi2021conv].
 
This tool can be used to build real-time data processing systems to recognize emotions, stress, cognitive load, or analyze human behavior. Our final goal is to extend its capabilities to provide real-time emotion recognition using multimodal data. Furthermore, we plan to integrate it with `Psychopy` in the future and combine multimodal data collection and monitoring with `Psychopy` features when designing scenarios. Additionally, we plan to support LSL in the future. By supporting LSL, other applications that already support LSL could work with Octopus Sensing.
 
 
# Acknowledgement
We acknowledge the [Empatic Computing Laboratory (ECL)](http://empathiccomputing.org/) for their financial support and for providing feedback, and Professor Suranga Nanayakkara for giving us feedback.
 
# References

