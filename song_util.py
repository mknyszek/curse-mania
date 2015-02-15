import json

def save(name, audio_file_name, time_points):
    data = {
        'name': name,
        'file_name': audio_file_name,
        'time_points': time_points
    }

    with open(name + '.txt', 'w') as song_file:
        json.dump(data, song_file)

def load(song_file):
	with open(song_file, 'r') as song:
		return json.load(song)
        