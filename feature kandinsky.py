import numpy as np
import librosa, librosa.display
import scipy.fftpack as sf
from scipy import signal
import matplotlib.pyplot as plt

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
  
def feature_extractor(signal, frame_length):
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

    return np.array(features), f_min
  
 def create_dict(arr, f_min):
    out = [{#'Background': strumento principale, 
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

 
