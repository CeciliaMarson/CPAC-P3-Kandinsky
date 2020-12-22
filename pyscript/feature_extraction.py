import fetch_audio
import numpy as np
import os 
import librosa
import json
from color_helper import MplColorHelper

audio_dir = '../processing/HackatonProject1/data/audio'
json_dir = '../processing/HackatonProject1/data'
dark_maps = ['gray', 'bone', 'winter', 'copper']
light_maps = ['spring', 'autumn', 'summer' , 'hot']

#select color map based on global features
def global_color_map(valence, energy):
    if valence >= 0.2:
        if energy >= 0.5:
            map_name = light_maps[np.random.randint(0,2)]
        else:
            map_name = light_maps[np.random.randint(2,4)]
    else:
        if energy >= 0.5:
            map_name = dark_maps[np.random.randint(0,2)]
        else:
            map_name = dark_maps[np.random.randint(2,4)]
            
    return MplColorHelper(map_name, 1, 100)

def evaluate_feature(feature_arr):
    mean = np.mean(feature_arr)
    val = np.copy(feature_arr[0])
    
    for i, f in enumerate(val):
        if f >=mean:
            val[i] = np.random.randint(1,51)
        else:
            val[i] = np.random.randint(50, 100)

    val = val.astype(int)
    return val.tolist() 

#select color for each frame based on local features
def local_features(color_map, features):
    zcr = features[0]
    flat = features[1]
    centroid = features[2]

    val = [evaluate_feature(f) for f in features]
    mean = np.mean(np.array(val), axis=0)
    return [color_map.get_rgb(int(v)) for v in mean]

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

def create_dict(arr):
    out = [{'R': int(c[0]*255), 'G': int(c[1]*255), 'B': int(c[2]*255), 'Shape': np.random.randint(0,6)} for c in arr]
    return out

def main():
    audio_list = []
    audio_files = []
    songs_rgb_list = []

    if not os.path.exists(audio_dir):
       print('Audio folder not exist!\n') 
       exit()

    if not os.path.exists(json_dir):
       print('Json folder not exist!\n') 
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
    
    #for each song choose a colormap based on the global features
    #and then use the local features to select a color for each frame
    for sf, f, name in zip(spotify_features, signals_features, song_names):
        #select the color map based on the global features
        COL = global_color_map(sf['valence'], sf['energy']) 
        rgb_arr = local_features(COL, f)
        rgb_dict = create_dict(rgb_arr)
        with open(os.path.join(json_dir, name+'.json'),'w', encoding='utf-8') as outfile:
            json.dump(rgb_dict, outfile, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    #get the artist name from fetch_audio
    artist_name, spotify_features, song_names = fetch_audio.main()
    audio_dir = os.path.join(audio_dir, artist_name)
    main()






