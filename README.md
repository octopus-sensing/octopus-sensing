# EmotionDataCollection, Octopus-Sensing

This software is for recording data synchronously from different sources including OpenBCI EEG headset, Shimmer sensor (GSR and PPG), Video and Audio. For other modalities that we want to add in the future, we should define a new process similar to others.

For running this software:

1- Create the following folders:

     created_files/

     created_files/videos

     created_files/eeg

     created_files/gsr

     created_files/answers

     created_files/image_index

2- connect the camera to the second monitor

3- setup the eeg cap and check ampedance using OpenBCI GUI

3- start eeg streaming through OpenVibe
   - start openvibe server and connect and play
   - start the scenario for showing and saving eeg data

4- setup shimmer and turn on it.

5- pair bluetooth and serial port
   - hcitool scan //show the macaddress of device. for shimmer it is 00:06:66:F0:95:95
   - vim /etc/bluetooth/rfcomm.conf
        rfcomm0{
           bind no;
           device 00:06:66:F0:95:95;
           channel 1;
           comment "serial port"
        }
    - sudo rfcomm connect rfcomm0 00:06:66:F0:95:95   // This is for reading bluetooth data from a serial port

6- run the following command:

     python3 main.py -s = participant_number
