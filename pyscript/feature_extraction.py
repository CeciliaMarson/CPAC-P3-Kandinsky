import fetch_audio
import numpy as np
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import librosa
import json
from tensorflow.keras.models import load_model
from color_helper import MplColorHelper

audio_dir = '../processing/HackatonProject1/data/audio'
json_dir = '../processing/HackatonProject1/data'
models_dir = 'models'
dark_maps = ['gray', 'bone', 'winter', 'copper']
light_maps = ['spring', 'autumn', 'summer' , 'hot']

#change based on the model!!!!!
#this is for model3
target_dict = {0: 'cla', 1: 'cel', 2: 'flu', 3: 'vio', 4: 'pia', 5: 'gel', 6: 'gac', 7: 'sax', 8: 'voi', 9: 'org', 10: 'tru'} 

'''
red -> violin
orange -> baritone or viola
yellow -> trumpet 
green -> violin
blue -> flaute, cello, organ
violet -> horn
white -> pause
black -> silence
'''
color_dict = {0: (0, 0, 255), 1: (0, 0, 255), 2:(0, 0, 255), 3:(0, 255, 0), 5: (0, 0, 255), 7: (255, 255, 0), 8: (255, 0, 0)}

'''
#---------------- color mapping ------------------------
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
'''

#--------------- feature extraction -------------------

def extract_max_chroma(signal, frame_length, num):
    max_chroma=[]
    max_arg=[]
    chroma = librosa.feature.chroma_stft(y=signal, hop_length=frame_length, win_length=frame_length)

    for c in chroma.T:
        max_a=np.argmax(c)
        c_frame=np.sort(c)
        max_chroma.append(c_frame[num])
        max_arg.append(max_a)
    if(num==0):
      return np.array(max_chroma),np.array(max_arg)
  
    return np.array(max_chroma)

def detect_pitch(y, frame_length):
    S=librosa.stft(y=y,hop_length=2048,win_length=2048, center='false')
    Xmag=librosa.amplitude_to_db(np.abs(S))
    pitches, magnitudes = librosa.piptrack(S=Xmag, fmin=80, fmax=1000)
    pitch=[]

    for i,mag in enumerate(magnitudes.T):
        index = mag.argmax()  
        pitch.append(pitches[index][i])

    return np.array(pitch)

def feature_extractor(signal, frame_length, sr):
    features = []

    #on set detection is used to choose if a shape is a line or a figure
    oenv = librosa.onset.onset_strength(y=signal, sr=sr, hop_length=frame_length)
    on_set=np.expand_dims(oenv,axis=0)

    #Needed for stroke
    zcr = librosa.feature.zero_crossing_rate(signal, frame_length, frame_length)
    #Needed for the first dimesion
    s_centroid = librosa.feature.spectral_centroid(signal, hop_length = frame_length, win_length = frame_length, n_fft=frame_length)

    #The higher value note in the chromogram is needed for choosing the shape 
    #The second and the third one complete the chord... the three together choose the color
    chroma_key0, max_c=extract_max_chroma(signal,frame_length,0)
    chroma_key1=extract_max_chroma(signal,frame_length,1)
    chroma_key2=extract_max_chroma(signal,frame_length,2)

    #entropy_s=entropy.spectral_entropy(signal,method='fft',nperseg=frame_length)
    chroma0=np.expand_dims(chroma_key0, axis=0)
    chroma1=np.expand_dims(chroma_key1, axis=0)
    chroma2=np.expand_dims(chroma_key2, axis=0)
    max_ch=np.expand_dims(max_c, axis=0)

    note=np.zeros((12,1))
    for c in max_ch.T:
      note[c]=note[c]+1

    f_min=np.argmin(note)

    #pitch is used for second dimension and position 
    pitch=detect_pitch(signal,frame_length)
    pitch=np.expand_dims(pitch, axis=0)

    #energy is used to computet the transparency of the image
    energy=librosa.feature.rms(y=signal, hop_length=frame_length)

    features.append(on_set)
    features.append(zcr)
    features.append(s_centroid)
    features.append(chroma0)
    features.append(chroma1)
    features.append(chroma2)
    features.append(max_ch)
    features.append(pitch)
    features.append(energy)

    #print(np.array(features).shape)
    return np.array(features), f_min

def create_dict(arr, f_min, background):
    out = [{#'Background': strumento principale, 
    'Back_R': background[0],
    'Back_G': background[1],
    'Back_B': background[2],
    'Figure fill': int((c[0]<=5)), #choose if less "rythmic"
    'Figure line': int((c[0]>5)),  #choose if "rythmic"
    'Shape': int(c[6]), #based on note
    'R': int(c[3]*255), #based on value of max note (chord)
    'B': int(c[4]*255), #based on value of second max note (chord)
    'G': int(c[5]*255), #based on value of third max note (chord)
    'Y_dim':int(c[2]), #based on brigthness
    'Stroke':int(c[1]*100), #based on "rougthness"
    'X_dim':int(c[7]), #Based on Pitch
    'Transparency':float(c[8]*10), #based on the energy of the track
    'Grid': int((f_min==c[6])&((c[0]>5))) #less frequent note in figure line mode
        } for c in arr.T]

    return out

'''
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
'''
#--------------- instrument classification --------------------

def compute_spec(audio, sr):
    #downsamle
    audio = librosa.resample(audio, sr, int(sr/2))
    #normalization
    audio = librosa.util.normalize(audio)
    #mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=int(sr/2), n_fft=2048, hop_length=512, win_length=1024)
    #log of mel spectrogram magnitude
    db_spec = librosa.power_to_db(mel_spec, ref=np.max)
    
    return db_spec

def compute_predictions(audio_path, frame_length, hop_length, model):
  predictions = []

  #use stream to create an iterator
  #already loaded as mono
  audio_it = librosa.stream(audio_path, 1, frame_length, hop_length=hop_length, mono=True)
  sr = librosa.get_samplerate(audio_path)
  print('sr: %s' % (sr)) 

  for block in audio_it:
    block_spec = compute_spec(block, sr)

    #add batch dimension and channel dimension
    block_spec = np.expand_dims(block_spec, axis=-1)
    block_spec = np.expand_dims(block_spec, axis=0)
    predictions.append(model.predict(block_spec)[0])

  return predictions

def get_instrument(audio_path, frame_length, hop_length, model):
    #compute predictions
    predictions = compute_predictions(audio_path, frame_length, hop_length=hop_length, model=model)

    #compute global mean
    mean_global = np.mean(np.array(predictions), axis=0)

    #compute global predictions
    global_predictions = np.argpartition(mean_global,range(mean_global.shape[0]))[-3:][::-1]
    print('audio path: {}'.format(audio_path))
    print('global_predictions: {}'.format([(target_dict[el], mean_global[el]) for el in global_predictions]))

    #compute predictions at each frame
    frame_predictions = np.argmax(predictions, axis=1)
    print('frame_predictions: {}'.format([target_dict[el] for el in frame_predictions]))

    #return the most probable instrument
    return global_predictions[0]

def load_model_from_path(model_path):
    model = load_model(model_path)
    return model

# ------------------------ main -----------------------------------

def main():
    audio_list = []
    audio_files = []
    instrument_list = []
    #songs_rgb_list = []

    #parameters for instrument classification
    frame_length = 44100*3
    hop_length = int(frame_length/4) 

    #check if all the audio have been downloaded
    if not os.path.exists(audio_dir):
       print('Audio folder not exist!\n') 
       exit()

    if not os.path.exists(json_dir):
       print('Json folder not exist!\n') 
       exit()

    #name of all the audio files
    for (dirpath, dirnames, filenames) in os.walk(audio_dir):
        audio_list.extend(filenames)
    
    #-------------- instument classification -------------

    #load the model for instrument classification
    #model is trained in the instrument_classifier.ipynb
    #here is only used to make predictions
    model_path = os.path.join(models_dir, 'model3.h5')
    model = load_model_from_path(model_path)

    #load all the audio files
    for audio in audio_list:
        audio_path =  os.path.join(audio_dir, audio)
        #instument extraction
        instrument_list.append(get_instrument(audio_path, frame_length, hop_length, model))
        s, sr = librosa.load(os.path.join(audio_dir, audio), sr = None)
        audio_files.append(s)

    #------------- feature extraction -------------------

    #1s frame length in sample
    tempos = [f['tempo'] for f in spotify_features]
    frame_length = sr*np.min(np.array(tempos))

    #signals_features = [feature_extractor(audio, int(frame_length/tempo), sr) for audio, tempo in zip(audio_files, tempos)]
    #print_features(signals_features)

    #extraction of the features for each audio file (2048 as frame length)
    signals_features = [feature_extractor(audio, 2048, sr) for audio, tempo in zip(audio_files, tempos)]
    
    #the len of signals_features, song_names and instument_list is always the same (the # of songs)
    for f, name, instrument in zip(signals_features, song_names, instrument_list):
        song_dict = create_dict(f[0][:, 0, :], f[1], color_dict[instrument])
        with open(os.path.join(json_dir, name+'.json'), 'w', encoding='utf-8') as outfile:
            json.dump(song_dict, outfile, ensure_ascii=False, indent=4)

    '''
    #for each song choose a colormap based on the global features
    #and then use the local features to select a color for each frame
    for sf, f, name in zip(spotify_features, signals_features, song_names):
        #select the color map based on the global features
        COL = global_color_map(sf['valence'], sf['energy']) 
        rgb_arr = local_features(COL, f)
        rgb_dict = create_dict(rgb_arr)
        with open(os.path.join(json_dir, name+'.json'),'w', encoding='utf-8') as outfile:
            json.dump(rgb_dict, outfile, ensure_ascii=False, indent=4)
   '''

if __name__ == '__main__':
    #get the artist name from fetch_audio
    artist_name, spotify_features, song_names = fetch_audio.main()
    audio_dir = os.path.join(audio_dir, artist_name)
    main()






