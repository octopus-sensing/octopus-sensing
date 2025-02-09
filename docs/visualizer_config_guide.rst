.. _visualizer_config_guide:

*******************************************
How to prepare a config file for Visualizer
*******************************************

A config file includes one section for defining specific configs for each kind of data.

SERVER
------
You can configure the port that server is going to listen on.

Example
"""""""

::
    [SERVER]
    port: 9800


EEG
----
To display EEG data, first of all we should specify the path of recorded EEG file by giving value to the `path` option. 
Also, we should identify the `sampling_rate` of recorded data. 
Octopus-sensing-visualizer has provided several options for displaying raw or processed EEG data.
By giving `True` value to each option, we specify which kind of graphs to be displayed.

Octopus-sensing-visualizer supports the following graphs for displaying the EEG signals:
    - `display_signal`: If True, displays raw signals for all channels
    - `display_power_band_bars`: If True, displays a bar chart of average of each power band signal
    - `display_alpha_signal`: If True, displays alpha band signal extracted from all channels.
    - `display_beta_signal`: If True, displays beta band signal extracted from all channels.
    - `display_gamma_signal`: If True, displays gamma band signal extracted from all channels.
    - `display_delta_signal`: If True, displays delta band signal extracted from all channels.
    - `display_theta_signal`: If True, displays theta band signal extracted from all channels.
    - `window_size`: It specifies the size of window for measuring power bands in seconds
    - `overlap`: Shows the overlap between consequences windows in measuring power bands

Example
"""""""

::
    [EEG]
    path=data/OpenBCI_01_01.csv
    sampling_rate=128
    display_signal=False
    display_power_band_bars=True
    display_alpha_signal=False
    display_beta_signal=False
    display_gamma_signal=False
    display_delta_signal=False
    display_theta_signal=False
    window_size=3
    overlap=2


GSR
----
All options related to GSR signal. 
    - `path`: Path to GSR data (csv file)
    - `sampling_rate`: recording sampling rate
    - `display_signal`: If True, displays GSR raw signal
    - `display_phasic`: If True, extracts phasic component and displays it
    - `display_tonic`: If True, extracts tonic component and displays it

Octopus-sensing-visualizer uses `neurokit library <https://neurokit.readthedocs.io/en/latest/>`_ 
for extracting GSR components.

Example
"""""""

::
    [GSR]
    path=data/gsr-01-01.csv
    sampling_rate=128
    display_signal=True
    display_phasic=True
    display_tonic=True
  

PPG
----
All options related to PPG signal. 

    - `path`: Path to PPG data (csv file)
    - `sampling_rate`: recording sampling rate
    - `display_signal`: If True, displays PPG raw signal
    - `display_hr`: If True, extracts heart rate (hr) and displays it
    - `display_hrv`: If True, extracts heart rate variability (hrv) and displays it
    - `display_breathing_rate`: If True, extracts breathing rate (br) and displays it
    - `window_size`: The window size for extracting hr, hrv and br.
    - `overlap`: Shows the overlap between consequences windows

Octopus-sensing-visualizer uses `heartpy library <https://github.com/paulvangentcom/heartrate_analysis_python>`_ 
for extracting hr, hrv and breathing rate.

Example
"""""""

::
    [PPG]
    path=octopus_sensing_visualizer/test_data/ppg_video-43-00-08.csv
    sampling_rate=128
    display_signal=True
    display_hr=True
    display_hrv=True
    display_breathing_rate=True
    window_size=20
    overlap=19

