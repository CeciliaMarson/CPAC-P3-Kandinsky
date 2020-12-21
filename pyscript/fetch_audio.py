import requests 
import os 
import urllib.request
import json
import numpy as np
from urllib.request import urlopen
from shutil import copyfileobj
import shutil
from pydub import AudioSegment

#token
token = "BQDsvtF62_ZhbeVGX09X-XIq_zj4in8nPnq317rP9ef9KJuBNL0VUsNmi2A1DM4gTkuL1B2DyuKBTwgPEPM54iCy9GZ2zBgfinFWlRCklnJO7Wij4-KWtmhYijM64E2gX3Ia479JzOdquvMh9HfYagZWo49RaCDfZge9B948bBIv88sHBfc-9t1xhV9F79PMbd528q8Bucx2mZw6Oy48kv8wNhPD16Lh6l-niGpCqA90pCfFcupahTq0LcsCRNPYVQlkUTMTz6ESIn1YuNk" 

#header field for the request, should contain the token
header = {'Authorization': 'Bearer %s'%token}

#directories
audio_dir = 'audio'

#request urls
search_url = 'https://api.spotify.com/v1/search'
artist_toptrack_url = 'https://api.spotify.com/v1/artists/id/top-tracks'
audio_features_url = 'https://api.spotify.com/v1/audio-features/id'

def delete_folder(dir_name):
    #delete previous folder for the preview 
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

def make_request(url, parameters):
    req = requests.get(url=url, params=parameters, headers=header)
    return req

def main():
    spotify_features = []

    #delete all the previous folders 
    delete_folder(audio_dir)

    #creat audio folder
    os.makedirs(audio_dir)

    #ask user for the artist name
    #artist_name ='The Kandinsky Effect'
    artist_name = input('Insert the artist name: ')

    #create the folder for the artist
    artist_dir = os.path.join(audio_dir, artist_name)
    os.makedirs(artist_dir)

    #get the id of the artist
    params={'q': artist_name , 'type': 'artist'}
    req = make_request(search_url, params)

    if not req.status_code == 200:
        print('Error! {}'.format(req.json()['error']['message']))
        delete_folder(audio_dir)
        exit()

    artist_id = req.json()['artists']['items'][0]['id']

    #get the top track of the artist
    url = artist_toptrack_url.replace('id', artist_id)
    params = {'country': 'IT'}
    req = make_request(url , params)

    if not req.status_code == 200:
        print('Error! {}'.format(req.json()['error']['message']))
        delete_folder(audio_dir)
        exit()

    songs = req.json()['tracks'] 
    #save url of the preview and song names 
    preview_urls = [song['preview_url'] for song in songs]
    songs_name = [song['name'] for song in songs]
    songs_id = [song['id'] for song in songs]

    #for now we simply save the previews
    for url, name in zip(preview_urls, songs_name):
        filename = os.path.join(artist_dir, name+'.mp3')
        with urlopen(url) as in_stream, open(filename ,'wb') as out_file:
            copyfileobj(in_stream, out_file)   
            sound = AudioSegment.from_mp3(filename)
            sound.export(filename.replace('.mp3', '.wav'), format='wav')
            os.remove(filename)

    for id in songs_id:
        song_url = audio_features_url.replace('id', id)
        req = make_request(song_url, None)
        spotify_features.append(req.json())

    return artist_name, spotify_features

if __name__ == "__main__":
    main()

