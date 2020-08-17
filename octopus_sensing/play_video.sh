#!/bin/sh

vlc --fullscreen --play-and-exit $1
# It should run in two different terminal
wmctrl -ir $(wmctrl -l |grep VLC |cut -d ' ' -f 1) -e 0,1200,0,-1,-1
