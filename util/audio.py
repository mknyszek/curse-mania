import pyaudio
import wave
import time
import sys

def play_song(wav_file_name, custom_callback=lambda in_data, frame_count, time_info, status: None):
    wf = wave.open(wav_file_name, 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)

        custom_callback(in_data, frame_count, time_info, status)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    return (wf, p, stream)
