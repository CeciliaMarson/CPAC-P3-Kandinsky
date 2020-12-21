import fetch_audio
import numpy as np
import os 
import librosa

audio_dir = 'audio'

def feature_extractor(signal, frame_length):
    features = []

    zcr = librosa.feature.zero_crossing_rate(signal, frame_length, frame_length)
    s_flatness = librosa.feature.spectral_flatness(signal, hop_length = frame_length, win_length = frame_length, n_fft=frame_length)
    s_centroid = librosa.feature.spectral_centroid(signal, hop_length = frame_length, win_length = frame_length, n_fft=frame_length)

    features.append(zcr)
    features.append(s_flatness)
    features.append(s_centroid)
    return features


def main():
    audio_list = []
    audio_files = []

    if not os.path.exists(audio_dir):
       print('Audio folder not exist!\n') 
       exit()

    #name of all the audio files
    for (dirpath, dirnames, filenames) in os.walk(audio_dir):
        audio_list.extend(filenames)

    #load all the audio files
    for audio in audio_list:
        s, sr = librosa.load(os.path.join(audio_dir, audio), sr = None)
        audio_files.append(s)

    #feature extraction
    #1s frame length in sample
    frame_length = int(sr/4)
    f = feature_extractor(audio_files[0], frame_length) 
    print(len(f))
    print(f[0].shape)
    print(f[1].shape)
    print(f[2].shape)

if __name__ == '__main__':
    #get the artist name from fetch_audio
    artist_name = fetch_audio.main()
    audio_dir = os.path.join(audio_dir, artist_name)
    main()






