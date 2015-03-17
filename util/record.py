from curses import wrapper
import sys

from util import audio
from util import play
from util import song_util

def record(stdscr, song_file):
    height, width = stdscr.getmaxyx()
    
    stdscr.clear()

    song_name = song_file[:-4]
    song_file = song_util.DIR_WAV + song_file

    (wave_file, player, stream) = audio.play_song(song_file)
    start_point = stream.get_time()
    time_points = []

    while True:
        stdscr.refresh()
        key = stdscr.getkey()
        time = stream.get_time() - start_point

        if key == 'd':
            stdscr.addstr(0, 0, "d-beat created at: " + str(time))
            time_points.append((0, time))
        elif key == 'f':
            stdscr.addstr(0, 0, "f-beat created at: " + str(time))
            time_points.append((1, time))
        elif key == 'j':
            stdscr.addstr(0, 0, "j-beat created at: " + str(time))
            time_points.append((2, time))
        elif key == 'k':
            stdscr.addstr(0, 0, "k-beat created at: " + str(time))
            time_points.append((3, time))
        else:
            time_points.append((-1, time))
            play.end_playback(wave_file, player, stream)
            song_util.save(song_name, song_file, time_points)
            return
