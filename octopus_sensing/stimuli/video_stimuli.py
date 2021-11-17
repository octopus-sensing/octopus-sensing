# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.

import threading
import vlc


def get_end_callback(mediaplayer):
    def end_callback(event):
        print("End of playing reached")
        mediaplayer.stop()
        mediaplayer.get_media().release()
        mediaplayer.release()
        mediaplayer.get_instance().release()
    return

def show_video_stimuli(video_path):
    '''
    Displays video in the specified path

    Parameters
    ----------

    video_path: str
        The path of video
    
    '''

    def play():
        vlc_instance = vlc.Instance(["--no-xlib", "--play-and-exit"])
        media_player = vlc.MediaPlayer(vlc_instance, video_path)
        
        media_player.play()

        event_manager = media_player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, get_end_callback(media_player))
        
        # wait so the video can be played for 5 seconds
        # irrespective for length of video
        
        # stopping the media
        #media_player

    threading.Thread(target=play).start()
