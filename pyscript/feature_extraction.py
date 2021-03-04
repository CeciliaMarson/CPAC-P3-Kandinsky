import fetch_audio
import numpy as np
import os 
import random
#disable tf warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
import librosa
import json
from tensorflow.compat.v1.logging import set_verbosity, FATAL
from tensorflow.keras.models import load_model
set_verbosity(FATAL)

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

#used to implement the kandinsky rules
#each instrument correspond to a color
color_dict = {0: (101,101,228), 1: (101,101,228), 2:(101,101,228), 3:(63,288,89), 4:(101,101,228), 5: (223,226,30), 6:(63,288,89), 7: (255,77,77), 8: (255,153,0), 9:(101,101,228), 10:(242,184,48)}


#---------------- color mapping ------------------------

#--------------- feature extraction -------------------

def prevalent_color(A,B,C):
  colors=[]
  for i,a in enumerate(A):
    b=B[i]
    c=C[i]
    if((a<b) & (a<c)):
      color=0
    if(((a>b) & (a<c)) | ((a<b) & (a>c))):
      color=1
    if((a>b) & (a>c)):
      color=2
    colors.append(color)
  return np.array(colors)

def RGB_offset(colors, chroma0, max_0, chroma1, max_1, chroma2, max_2):
  RGB=[]
  R=[]
  G=[]
  B=[]
  for i,c in enumerate(colors):
    if(c==0):
      if(max_1[i]<max_2[i]):
        r=chroma0.T[i]
        g=chroma1.T[i]
        b=chroma2.T[i]
      else:
        r=chroma0.T[i]
        g=chroma2.T[i]
        b=chroma1.T[i]
    if(c==1):
      if(max_1[i]<max_2[i]):
        r=chroma1.T[i]
        g=chroma0.T[i]
        b=chroma2.T[i]
      else:
        r=chroma2.T[i]
        g=chroma0.T[i]
        b=chroma1.T[i]
    if(c==2):
      if(max_1[i]<max_2[i]):
        r=chroma1.T[i]
        g=chroma2.T[i]
        b=chroma0.T[i]
      else:
        r=chroma2.T[i]
        g=chroma1.T[i]
        b=chroma0.T[i]
    R.append(r)
    G.append(g)
    B.append(b)
	
  RGB.append(R)
  RGB.append(G)
  RGB.append(B)
  return np.array(RGB)
  
def major_minor(signal, frame_length):
    max_chroma=[]
    max_arg=[]
    chroma = librosa.feature.chroma_stft(y=signal, hop_length=frame_length, win_length=frame_length, n_fft=frame_length)
    chords=[]
    for c in chroma.T:
        mean=np.mean(c)
        max_a=np.argmax(c)
        third=(max_a+4)%12
        fifth=(max_a+7)%12
        minor=(max_a+3)%12
        if(third>minor):
          if((c[third]>=mean) | (c[fifth]>=mean)):
            key=0
          else: key=2
        else:
          if((c[minor]>=mean) | (c[fifth] >=mean)):
            key=1
          else: key=2
        chords.append(key)
    return np.array(chords)
	

def assign_shape(onset, max_ch, chords, color, f_min):
  shapes=[]
  for i, j in enumerate(onset.T):
    if((f_min==max_ch.T[i]) & (j>5)):
      shape=9  #special condition for grid
    else:
      if(j>5): #lines
        shape=chords[i]
      else:    #fill figure
        if(chords[i]==0):
          if(color[i]==0):
            shape=3;
          if(color[i]==1):
            shape=4
          if(color[i]==2):
            shape=5
        if(chords[i]==1):
          if(color[i]==0):
            shape=6;
          if(color[i]==1):
            shape=7
          if(color[i]==2):
            shape=8
        if(chords[i]==2): 
          shape=int(max_ch.T[i]%6)+3
    shapes.append(shape)   
  return np.array(shapes)

def extract_max_chroma(signal, frame_length, num):
    max_chroma=[]
    max_arg=[]
    chroma = librosa.feature.chroma_stft(y=signal, hop_length=frame_length, win_length=frame_length, n_fft=frame_length)

    for c in chroma.T:
        max_a=np.argsort(c)
        c_frame=np.sort(c)
        max_chroma.append(c_frame[11-num])
        max_arg.append(max_a[11-num])
        
    return np.array(max_chroma),np.array(max_arg)

def detect_pitch(y, frame_length):
    S=librosa.stft(y=y,hop_length=frame_length ,win_length=frame_length, n_fft=frame_length, center='false')
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
    chroma_key0, max_0 = extract_max_chroma(signal,frame_length,0)
    chroma_key1, max_1 = extract_max_chroma(signal,frame_length,1)
    chroma_key2, max_2 = extract_max_chroma(signal,frame_length,2)

    chroma0 = np.expand_dims(chroma_key0, axis=0)
    chroma1 = np.expand_dims(chroma_key1, axis=0)
    chroma2 = np.expand_dims(chroma_key2, axis=0)
    max_ch = np.expand_dims(max_0, axis=0)

    note=np.zeros((12,1))
    for c in max_ch.T:
      note[c]=note[c]+1

    f_min=np.argmin(note)
	
	#indicative if the principal chords is major, minor or not clear
    chords=major_minor(signal, frame_length)

    #assign a primary color based on the position of the higher note in respect to the others
    colors=prevalent_color(max_0,max_1,max_2)

    #the shape is choosen using infomation from the chroma and from the onset detection 
    shap=assign_shape(on_set, max_ch, chords, colors, f_min)
    shapes=np.expand_dims(shap, axis=0)

    #pitch is used for second dimension and position 
    pitch=detect_pitch(signal,frame_length)
    pitch=np.expand_dims(pitch, axis=0)

    #energy is used to computet the transparency of the image
    energy=librosa.feature.rms(y=signal, hop_length=frame_length)
	
    RGB=RGB_offset(colors, chroma0, max_0, chroma1, max_1, chroma2, max_2)
    
    RGB=RGB.reshape(RGB.shape[0],RGB.shape[1])

    #features.append(on_set)
    #features.append(zcr)
    #features.append(s_centroid)
    #features.append(chroma0)
    #features.append(chroma1)
    #features.append(chroma2)
    #features.append(max_ch)
    #features.append(pitch)
    #features.append(energy)
    features.append(shapes)
    features.append(zcr)
    features.append(s_centroid)
    features.append(np.expand_dims(RGB[0], axis=0))
    features.append(np.expand_dims(RGB[1], axis=0))
    features.append(np.expand_dims(RGB[2], axis=0))
    features.append(pitch)
    features.append(energy)

    #print(np.array(features).shape)
    return np.array(features)#, f_min
	

#Shape indices:
#Arc=0,Line=1,Wave=2,Square=3,ArcFill=4,Circle=5,Rect=6,Triangle=7,Ellipse=8,Grid=9
def create_dict(arr):
    out = [{
    'Shape': int(c[0]), #based on note
    'R': int(c[3]*255), #based on value of max note (chord)
    'B': int(c[4]*255), #based on value of second max note (chord)
    'G': int(c[5]*255), #based on value of third max note (chord)
    'Y_dim':int(c[7]*1000), #based on brigthness
    'Stroke':int(c[1]*100), #based on "rougthness"
    'X_dim':int(c[6]), #Based on Pitch
    'Transparency':float(c[2]/100+50), #based on the energy of the track
        } for c in arr.T]
    return out

'''
def create_dict(arr, f_min, background):
    out = [{#'Background': strumento principale, 
    #'Figure fill': int((c[0]<=5)), #choose if less "rythmic"
    #'Figure line': int((c[0]>5)),  #choose if "rythmic"
    'Shape': int(c[0]), #based on note
    'R': background[0] + random.randint(-int(c[3]*255)*2,int(c[3]*255)*2), #based on value of max note (chord)
    'B': background[1] + random.randint(-int(c[4]*255)*2,int(c[4]*255)*2), #based on value of second max note (chord)
    'G': background[2] + random.randint(-int(c[5]*255)*2,int(c[5]*255)*2), #based on value of third max note (chord)
    'Y_dim':int(c[2]), #based on brigthness
    'Stroke':int(c[1]*100), #based on "rougthness"
    'X_dim':int(c[6]), #Based on Pitch
    'Transparency':float(c[7]*100+50), #based on the energy of the track
    #'Grid': int((f_min==c[6])&((c[0]>5))) #less frequent note in figure line mode
        } for c in arr.T]

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
  #predictions = []
  audio = np.empty((1, 128,130,1))

  #use stream to create an iterator
  #already loaded as mono
  audio_it = librosa.stream(audio_path, 1, frame_length, hop_length=hop_length, mono=True, fill_value=0)
  sr = librosa.get_samplerate(audio_path)
  #print('sr: %s' % (sr)) 

  for block in audio_it:
    block_spec = compute_spec(block, sr)

    #add channel dimension
    block_spec = np.expand_dims(block_spec, axis=-1)
    block_spec = np.expand_dims(block_spec, axis=0)
    audio = np.vstack((audio, block_spec))
	
  predictions = model.predict(audio)
  return predictions

def get_instrument(audio_path, frame_length, hop_length, model):
    #compute predictions
    predictions = compute_predictions(audio_path, frame_length, hop_length=hop_length, model=model)

    #compute global mean
    mean_global = np.mean(np.array(predictions), axis=0)

    #compute global predictions
    global_predictions = np.argpartition(mean_global,range(mean_global.shape[0]))[-3:][::-1]
    #print('audio path: {}'.format(audio_path))
    #print('global_predictions: {}'.format([(target_dict[el], mean_global[el]) for el in global_predictions]))

    #compute predictions at each frame
    frame_predictions = np.argmax(predictions, axis=1)
    #print('frame_predictions: {}'.format([target_dict[el] for el in frame_predictions]))

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
    #hop_length = int(frame_length/4) 
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
    for index, audio in enumerate(audio_list):
        audio_path =  os.path.join(audio_dir, audio)
        print('Classifying instruments in the songs and extracting features... [{}/{}]'.format(index+1, len(audio_list)), end='\r')
        #instument extraction
        instrument_list.append(get_instrument(audio_path, frame_length, hop_length, model))
        s, sr = librosa.load(os.path.join(audio_dir, audio), sr = None)
        audio_files.append(s)
	
    
    #------------- feature extraction -------------------

    #1s frame length in sample
    #tempos = [f['tempo'] for f in spotify_features]

    #signals_features = [feature_extractor(audio, int(frame_length/tempo), sr) for audio, tempo in zip(audio_files, tempos)]
    #print_features(signals_features)

    #extraction of the features for each audio file (2048 as frame length)
    signals_features = [feature_extractor(audio, 30000, sr) for audio in audio_files]
    
    #the len of signals_features, song_names and instument_list is always the same (the # of songs)
    #for f, name, instrument in zip(signals_features, song_names, instrument_list):
    #    song_dict = create_dict(f[0][:, 0, :], f[1], color_dict[instrument])
    #    with open(os.path.join(json_dir, "".join(x for x in name if x.isalnum())+'.json'), 'w', encoding='utf-8') as outfile:
    #        json.dump(song_dict, outfile, ensure_ascii=False, indent=4)
	
	#the len of signals_features, song_names and instument_list is always the same (the # of songs)
    for f, name, instrument in zip(signals_features, song_names, instrument_list):
        song_dict = create_dict(f[:, 0, :])
        with open(os.path.join(json_dir, "".join(x for x in name if x.isalnum())+'.json'), 'w', encoding='utf-8') as outfile:
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
    #audio_dir = os.path.join(audio_dir, artist_name)
    main()






