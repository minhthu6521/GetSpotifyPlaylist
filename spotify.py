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
    sameTrackpl = []
    for i in range(len(pl2)):
        if pl2[i] in pl1:
            sameTrackpl.append(pl2[i])
    return sameTrackpl

def allTracks(pl1,pl2):
    allTrackpl = []
    difTrackpl = []
    sameTrackpl = sameTracks(pl1,pl2)
    for i in range(len(pl2)):
        if pl2[i] not in pl1:
            difTrackpl.append(pl2[i])
    for i in range(len(pl1)):
        if pl1[i] not in pl2:
            difTrackpl.append(pl1[i])
    allTrackpl = difTrackpl + sameTrackpl
    return allTrackpl

            
#Get the playlists and return

user = input('Playlist 1: Input user id :')
playlist = input('Playlist 1: Input playlist id:')


playList1 = simplify(getPlayList(user, playlist,token))

user = input('Playlist 2: Input user id:')
playlist = input('Playlist 2: Input playlist id:')
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

