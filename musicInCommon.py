import spotipy
import spotipy.util as util
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials


def initClientCredentials():
    global sp
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    initClientCredentials()

    SPOTIFY_SCOPE = "playlist-modify-private playlist-modify-public"
    global SPOTIFY_USERNAME
    SPOTIFY_USERNAME = input("enter your spotify username\n> ")
    token = util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE)

    users = usersFromFile("users.txt")
    tracks = getPlaylistTracks(users)
    print(tracks)
    global sp
    sp = spotipy.Spotify(token)

    #makePlaylistWithTracks(tracks, "overlap of " + ", ".join(users))
    makePlaylistWithTracks(tracks, "overlap playlist")


def getPlaylistTracks(users):
    allTracks = [tracksFromUserPlaylists(user) for user in tqdm(users)]
    if len(users) == 2:
        return findOverlap(allTracks, 2)

    else:
        overlaps = [
            findOverlap(allTracks, n) for n in tqdm(range((len(users))))
        ]
        for n in range(len(users)):
            print("{}: {}".format(n, len(overlaps[n])))
        chosen = int(input("choose n\n> "))
        return overlaps[chosen]


def makePlaylistWithTracks(tracks, name):
    newPl = sp.user_playlist_create(SPOTIFY_USERNAME, name)['uri']

    for i in tqdm(range(0, len(tracks), 100)):
        sp.user_playlist_add_tracks(SPOTIFY_USERNAME, newPl, tracks[i:i + 100])


def findOverlap(allTracks, cutoff):
    print("n is {}".format(cutoff))
    outPl = []

    freqDict = {}
    for trackSet in tqdm(allTracks):
        for track in tqdm(trackSet):
            if track in freqDict:
                freqDict[track] += 1
            else:
                freqDict[track] = 1

    for k, v in freqDict.items():
        if v >= cutoff:
            outPl.append(k)

    return outPl


def tracksFromUserPlaylists(user):
    tracks = set()
    for pl in tqdm(playlistsFromUser(user)):
        plTracks = tracksInPlaylist(user, pl)
        #print(len(plTracks))
        tracks.update(
            [t['track']['uri'] for t in plTracks if t['track'] is not None])
    return tracks


def playlistsFromUser(user):
    batch = sp.user_playlists(user)
    playlists = [pl['uri'] for pl in batch['items']]
    while batch['next']:
        batch = sp.next(batch)
        playlists.extend([pl['uri'] for pl in batch['items']])
    return playlists


def usersFromFile(filen):
    users = []
    with open(filen) as f:
        for line in f:
            users.append(line.strip())
    return users


def tracksInPlaylist(user, playlist):
    #spotify only gives 100 at a time, thanks ackleyrc
    batch = sp.user_playlist_tracks(user, playlist)
    tracks = batch['items']
    while batch['next']:
        batch = sp.next(batch)
        tracks.extend(batch['items'])
    return tracks


def formatTracklist(tracks):
    formatted = []
    for track in tracks:
        tDat = sp.track(track)
        formatted.append(tDat['name'] + " - " + tDat['artists'][0]['name'])

    formatted = sorted(formatted, key=lambda x: x[::-1])
    return "\n\n<br>".join(formatted)


if __name__ == "__main__":
    main()
