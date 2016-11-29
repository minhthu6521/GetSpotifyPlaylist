import requests
import json

#Get the authorization token
client_id = '34d126b9cfef4ee89b9e4b74f2af3ad0'
client_secret = '64e95c549ce442a8bcb6cc270bf982f4'

grant_type = 'client_credentials'


body_params = {'grant_type' : grant_type}

url='https://accounts.spotify.com/api/token'

response=requests.post(url, data=body_params, auth = (client_id, client_secret)) 
data = response.json()
token = data['access_token']

#Functions
def getPlayList(user, playist, token):
    "Get the playlist from Spotify and store in array"
    
    url = 'https://api.spotify.com/v1/users/' + user + '/playlists/' + playlist
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8','Authorization': 'Bearer ' + token}
    r = requests.get(url, headers = headers)

    data = r.json()
    arr = data['tracks']['items']
    return arr

class Track:
    def __init__(self,name,artist):
        self.name = name
        self.artist = artist
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    def __hash__(self):
        return hash((self.name,self.artist))

def simplify(playList):
    "Convert the data taken from Spotify to Track object"
    pl = []
    for i in range(len(playList)):
        artists = []
        for j in range(len(playList[i]['track']['artists'])):
            artists.append(playList[i]['track']['artists'][j]['name'])
        str = ', '.join(artists)
        name = playList[i]['track']['name']
        track = Track(name, str)
        pl.append(track)
    return pl


def sameTracks(pl1,pl2):
    sameTrackpl = list(set(pl1).intersection(pl2))
    return sameTrackpl

def allTracks(pl1,pl2):
    allTrackpl = []
    sameTrackpl = sameTracks(pl1,pl2)
    allTrackpl = list(set(pl1) - set(sameTrackpl)) +pl2
    return allTrackpl

            
#Get the playlists and return

user = 'chrischinching'
playlist = '0hHfwU4V0b3SXgMhCFnIqU'


playList1 = simplify(getPlayList(user, playlist,token))

user = 'leecro13'
playlist = '4d2JJUEMf4H5xNOSIhRhEX'
playList2= simplify(getPlayList(user, playlist,token))

print('######################################')
print('The tracks appears on both playlist')
print('######################################')
samePl = sameTracks(playList1,playList2)
for i in range(len(samePl)):
    print(samePl[i].name + ' - ' + samePl[i].artist)
    
print('######################################')
print('All tracks in two playlists')
print('######################################')
allPl = allTracks(playList1,playList2)
for i in range(len(allPl)):
    print(allPl[i].name + ' - ' + allPl[i].artist)

