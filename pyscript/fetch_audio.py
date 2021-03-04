import os 
from requests import get, post
from urllib.request import urlopen
from shutil import copyfileobj
from shutil import rmtree
from pydub import AudioSegment

#directories
audio_dir = '../processing/HackatonProject1/data/audio'
json_dir = '../processing/HackatonProject1/data'

#request urls
search_url = 'https://api.spotify.com/v1/search'
artist_toptrack_url = 'https://api.spotify.com/v1/artists/id/top-tracks'
audio_features_url = 'https://api.spotify.com/v1/audio-features/id'

#app encoded ids
encoded_ids = 'MzYxYzk3MTU5YTZiNDdkMGI3NDRmYWEwNzg3MGYzNzg6MzYyNmIyNzZiNjQzNDVhODkxM2E4N2RmY2UzNjJkYjk='

def delete_folder(dir_name):
    #delete previous folder for the preview 
    if os.path.exists(dir_name):
        #shutil.rmtree
        rmtree(dir_name)

def make_request(url, parameters, header):
    #request.get
    req = get(url=url, params=parameters, headers=header)
    return req

def error_request(req):
    if not req.status_code == 200:
        print('Error! {}'.format(req.json()['error']['message']))
        delete_folder(audio_dir)
        exit()

def main():
    spotify_features = []

    #delete all the previous folders 
    delete_folder(json_dir)

    #creat audio folder
    os.makedirs(json_dir)
    os.makedirs(audio_dir)

    #make a post request to get the token
    #the app is registered on spotify
    header = {'Authorization': 'Basic {}'.format(encoded_ids)}
    body = {'grant_type':'client_credentials'}
    #request.post
    r = post('https://accounts.spotify.com/api/token', data=body, headers=header)
    token = r.json()['access_token']

    #header field for the request, should contain the token
    header = {'Authorization': 'Bearer %s'%token}

    #ask user for the artist name
    #artist_name ='The Kandinsky Effect'
    artist_name = input('Insert the artist name: ')

    #create the folder for the artist
    #artist_dir = os.path.join(audio_dir, artist_name)
    #os.makedirs(artist_dir)

    #get the id of the artist
    params={'q': artist_name , 'type': 'artist'}
    req = make_request(search_url, params, header)

    #check for error in the response 
    error_request(req)

    artist_id = req.json()['artists']['items'][0]['id']

    #get the top track of the artist
    url = artist_toptrack_url.replace('id', artist_id)
    params = {'country': 'IT'}
    req = make_request(url , params, header)
    #check for error in the response 
    error_request(req)

    songs = req.json()['tracks'] 
    #save url of the preview and song names 
    preview_urls = [song['preview_url'] for song in songs if song['preview_url'] is not None]
    songs_name = [song['name'] for song in songs]
    songs_id = [song['id'] for song in songs]
    #print(preview_urls, len(preview_urls) )

    #for now we simply save the previews
    for index, (url, name) in enumerate(zip(preview_urls, songs_name)):
        #remove illegal chars for windows and spaces, then create filename
        filename = os.path.join(audio_dir, "".join(x for x in name if x.isalnum())+'.mp3')
        print('Dowloading songs from spotify... [{}/{}]'.format(index+1, len(preview_urls)), end='\r')
        with urlopen(url) as in_stream, open(filename ,'wb') as out_file:
            copyfileobj(in_stream, out_file)   
            sound = AudioSegment.from_mp3(filename)
            sound.export(filename.replace('.mp3', '.wav'), format='wav')
        os.remove(filename)

    #for id in songs_id:
    #    song_url = audio_features_url.replace('id', id)
     #   req = make_request(song_url, None, header)
        #check for error in the response 
     #   if req.status_code == 503:
            #spotify_features.append({'energy': np.random.random(), 'valence': np.random.random(), 'tempo':120.0})
    #        print('Error 503 on url: '.format(song_url))
     #       continue
      #  spotify_features.append(req.json())

    return artist_name, spotify_features, songs_name

if __name__ == "__main__":
    main()

