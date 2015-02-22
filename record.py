from curses import wrapper
import sys

import audio
import play
import song_util

def main(stdscr):
    stdscr.clear()

    (wave_file, player, stream) = audio.play_song(sys.argv[2])
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
            play.end_playback(wave_file, player, stream)
            song_util.save(sys.argv[1], sys.argv[2], time_points)
            return

if len(sys.argv) < 3:
        print("Usage: %s song_name filename.wav" % sys.argv[0])
        sys.exit(-1)

wrapper(main)
