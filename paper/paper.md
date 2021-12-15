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
Designing user studies and collecting data is critical in exploring and automatically recognizing human behavior. Currently, it is possible to use a wide range of sensors to capture heart rate, brain activity, skin conductance, and a variety of different physiological cues [@seneviratne2017survey]. These can be combined together to provide information about a user’s emotional state [@egger2019emotion; @dzedzickis2020human], cognitive load [@vanneste2020towards; @mangaroska2021exploring], or other factors. However, even when data are collected correctly, synchronizing data from multiple sensors is time-consuming and subject to human error. Failure to record and synchronize data can lead to incorrect analysis and results, and finally, the need to repeat the time-consuming experiments several times. 
 
To overcome these challenges, `Octopus Sensing` facilitates synchronous data acquisition from various sources and provides some utilities for designing user studies, real-time monitoring, and offline data visualization.  The major aim of `Octopus Sensing`is to provide a simple scripting interface so that people with little or no software development skills can define sensor-based experiment scenarios with minimum effort.
 
# Statement of need
External events affect the human body and mind, creating many internal and external changes in response to external stimuli. Nowadays, researchers use various sensors to monitor and measure these responses to know more about a person’s state [@kreibig2010autonomic; @chen2020physiological; @sun2020multimodal] and employ sensors in many healthcare applications like assisting patients or mental health monitoring [@hassouneh2020development]. They can also be used to improve social interactions [@verschuere2006psychopathy; @hossain2019observers], and creating better quality of life by making intelligent devices like Intelligent Tutoring Systems [@dewan2019engagement] or making interactive robots and virtual characters [@val2020affective; @hong2020multimodal].
 
Recently, many researchers have tried to achieve a deeper understanding of humans by simultaneously interpreting a combination of physiological and behavioral changes in the human body [@shu2018review; @koelstra2011deap]. Acquiring and analyzing data from different sources with various hardware and software is complex, time-consuming, and challenging. Also, synchronously recording data with multiple formats can be easily affected by human error. These tasks slow down the pace of progress in human-computer interaction and human behavior research.  
 
There are a limited number of frameworks that support synchronous data acquisition. For example, [iMotions](@https://imotions.com/) has developed software that integrates and synchronizes a wide range of various sensors and devices that record a considerable range of signals synchronously. Although iMotions offers many useful features, it is a commercial software and is not open-source.
 
`Octopus Sensing` is a lightweight open-source multi-platform library that facilitates synchronous data acquisition from various sources and can be extended to process and analyze data in real-time. It provides a web-based real-time monitoring system that can be used remotely to illustrate and monitor signals in real-time. It also provides offline data visualization to see the changes in various sensors at the same time.
 
# Overview
 
Octopus Sensing is a tool to help in running scientific experiments that involve recording data synchronously from multiple sources. It can simultaneously collect data from various devices such as EEG [OpenBCI EEG headset](https://openbci.com/), GSR and PPG [Shimmer3 sensor](https://shimmersensing.com), video and audio. Data collection can be started and stopped synchronously across all devices. 
 
The main features of `Octopus Sensing` are listed as follows:

* Manages data recording from multiple sources using a simple unified interface.
* Minimizes human errors from manipulating data in synchronous data collection.
* Provides some utilities for designing studies like showing different stimuli or designing questionnaires.
* Offers a monitoring interface that prepares and visualizes collected data in real-time.
* Provides offline visualization of data from multiple sources simultaneously.
 
# Research perspective
 
We have used `Octopus Sensing` in designing several experiments in human emotion recognition. We designed the experiments and recorded facial video, brain activity, and physiological signals using `Octopus Sensing` in a watching video task to recognize emotion [@Saffaryazdi2021]. This scenario which is common in physiological emotion recognition studies, has been included in the repository as an example and explained in the tutorial. In another research study, we collected multimodal data in a face-to-face conversation task to analyze human emotional responses [@Saffaryazdi2021conv].
 
This tool can be used as the base structure for creating real-time data processing systems with capabilities to recognize emotions, stress, cognitive load, or analyze human behaviors. In the future, we want to extend its features to provide real-time emotion recognition using multimodal data analysis.
 
 
# Acknowledgement
We acknowledge the [Empatic Computing Laboratory](http://empathiccomputing.org/) for financial support and providing feedback.
 
# References

