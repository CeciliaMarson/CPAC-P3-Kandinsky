import fetch_audio
import numpy as np
import os 
import librosa
from color_helper import MplColorHelper

audio_dir = 'audio'
dark_maps = ['gray', 'bone', 'winter', 'copper']
light_maps = ['sping', 'summer', 'autumn', 'hot']

def global_color_map(valence, energy):
    if valence >= 0.2:
        if energy >= 0.5:
            map_name = np.randint(0,2)
        else:
            map_name = np.randint(2,4)
    else:
        if energy >= 0.5:
            map_name = np.randint(0,2)
        else:
            map_name = np.randint(2,4)
    
    return MplColorHelper(map_name, 2, 10)

def feature_extractor(signal, frame_length):
    features = []

    zcr = librosa.feature.zero_crossing_rate(signal, frame_length, frame_length)
    s_flatness = librosa.feature.spectral_flatness(signal, hop_length = frame_length, win_length = frame_length, n_fft=frame_length)
    s_centroid = librosa.feature.spectral_centroid(signal, hop_length = frame_length, win_length = frame_length, n_fft=frame_length)

    features.append(zcr)
    features.append(s_flatness)
    features.append(s_centroid)
    return features

def print_features(signal_features):
    for i, f in enumerate(signals_features):
        print('Mean of zcr: {}'.format(np.mean(f[0])))
        print('Std of zcr: {}'.format(np.std(f[0])))
        print('Mean of flat: {}'.format(np.mean(f[1])))
        print('Std of flat: {}'.format(np.std(f[1])))
        print('Mean of centr: {}'.format(np.mean(f[2])))
        print('Std of centr: {}'.format(np.std(f[2])))
        print('Tempo: {}'.format(spotify_features[i]['tempo']))
        print('#frames: {}'.format(f[0].shape))
        print('Energy: {}'.format(spotify_features[i]['energy']))
        print('Valence: {}'.format(spotify_features[i]['valence']))
        print('\n')
        #print('zcr: {}'.format(f[1]))

def main():
    audio_list = []
    audio_files = []

    if not os.path.exists(audio_dir):
       print('Audio folder not exist!\n') 
       exit()

    tempos = [f['tempo'] for f in spotify_features]

    #name of all the audio files
    for (dirpath, dirnames, filenames) in os.walk(audio_dir):
        audio_list.extend(filenames)

    #load all the audio files
    for audio in audio_list:
        s, sr = librosa.load(os.path.join(audio_dir, audio), sr = None)
        audio_files.append(s)

    #feature extraction
    #1s frame length in sample
    frame_length = sr*np.min(np.array(tempos))
    signals_features = [feature_extractor(audio, int(frame_length/tempo)) for audio, tempo in zip(audio_files, tempos)]
    #print_features(signals_features)

    for sf, f in zip(spotify_features, signals_features):
        #select the color map based on the global features
        COL = global_color_map(sf['valence'], sf['energy']) 
        #TODO select color from the color map at each frame

if __name__ == '__main__':
    #get the artist name from fetch_audio
    artist_name, spotify_features = fetch_audio.main()
    audio_dir = os.path.join(audio_dir, artist_name)
    main()






