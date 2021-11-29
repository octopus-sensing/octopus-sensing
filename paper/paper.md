---
title: 'Octopus_sensing: A python library for human-computer-interaction studies'
tags:
  - Python
  - Human-Computer-Interaction(HCI)
  - Physiological Signals
  - Multimodal Sensors

authors:
  - name: Nastaran Saffaryazdi
    orcid: 0000-0003-0872-7098
    affiliation: 1
  - name: Aidin Gharibnavaz
    affiliation: 3
  - name: Mark Billinghurst
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
Designing studies and collecting data is critical in exploring and recognizing human behavior automatically.Nonetheless, even when data are collected correctly, synchronizing data from multiple sensors is time and labor intensive and subject to human error. Failure to record and synchronize data can lead to incorrect analysis and result and finally repeating the time-consuming experiments several times. To overcome these challenges, `Octopus Sensing` facilitates synchronous data acquisition from various sources, provides some utilities for designing studies, real-time monitoring and offline data visualization.

# Statement of need
External events affect the human body and mind. Many internal and external changes happen in human body in response to external stimuli. Nowadays, researchers use various sensors to monitor and measure these responses to know more about human [@kreibig2010autonomic; @chen2020physiological; @sun2020multimodal] and employ them in many healthcare application like assisting patients or mental health monitoring [@hassouneh2020development], improve social interactions [@verschuere2006psychopathy; @hossain2019observers], and improve the quality of life by making intelligent devices like Intelligent Tutoring Systems [@dewan2019engagement] or making interactive robots and virtual characters [@val2020affective; @hong2020multimodal].

Recently, many researchers in human-computer interaction research areas try to achieve a deeper understanding of humans by interpreting a combination of physiological and behavioral changes in the human body simultaneously [@shu2018review; @koelstra2011deap]. Acquiring and analyzing data from different sources with various hardware and interface are complex and challenging tasks. Also, recording data with various formats synchronously can be easily affected by human error. These tasks slow down the pace of progress in human research.  There are a limited number of frameworks that support synchronous data acquisition. For example, [iMotions](@https://imotions.com/) has been provided software that integrates and synchronizes a wide range of various sensors and devices that record a considerable range of signals synchronously. Although iMotions offers many facilities, it is too expensive. Also, it is not open-source and cannot easily integrate with all research conditions.

`Octopus Sensing`, is a lightweight open-source and multi-platform library that facilitates synchronous data acquisition from various sources and can be extended to process and analyze data in real-time. It provides a web-based real-time monitoring system that can be used remotely to illustrate and monitor signals in real-time. Also, it provides offline synchronous data visualization to see the changes in various sensors at the same time.can

# Overview

Octopus Sensing is a tool to help in running scientific experiments that involve recording data synchronously from multiple sources in human-computer interaction studies. It can collect data from multiple devices such as [OpenBCI EEG headset](https://openbci.com/), [Shimmer3 sensor]() (GSR and PPG), Video and Audio and so forth simultaneously. Data collection can be started and stopped synchronously across all devices. Collected data will be tagged with the timestamp of the start and stop of the experiment, the ID of the experiment, etc.

The aim is to make the scripting interface so simple that people with minimum or no software development skills can define experiment scenarios with no effort. Also, this tool can be used as the base structure for creating real-time data processing systems like systems with capabilities of recognizing emotions, stress, cognitive load, or analyzing human behaviors.

## Main features

* Manages data recording from multiple sources using a simple unified interface.
* Minimizes human errors from manipulating data in synchronous data collection.
* Providing some utilities for designing studies like showing different stimulus or designing questionnaires.
* Monitoring interface that prepares and visualizes collected data in real-time.
* Offline visualization of data from multiple sources simultaneously 

# References