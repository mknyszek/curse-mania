from curses import wrapper
import sys

import audio
import song_util

THRESHOLD = 0.04
OFFSET = 0.00

def start_song(song_file_name, note_callback=lambda note, time_window: None):
    global start_point

    song = song_util.load(song_file_name)
    time_points = song['time_points']
    start_point = None

    def audio_callback(in_data, frame_count, time_info, status):
        global start_point

        if start_point is None:
            start_point = stream.get_time()

        if len(time_points) > 0:
            time = stream.get_time() - start_point
            note = time_points[0][0]
            time_point = time_points[0][1]

            if time >= time_point - THRESHOLD:
                if time <= time_point + THRESHOLD:
                    note_callback(note, THRESHOLD * 2)
                del time_points[0]

    (wave_file, player, stream) = audio.play_song(song['file_name'], audio_callback)

def end_playback(wf, p, stream):
    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()

def debug_callback(note, time_window):
    print(note)
