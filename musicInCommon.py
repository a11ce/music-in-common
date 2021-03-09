import spotipy
import spotipy.util as util
from tqdm import tqdm

SPOTIFY_USERNAME = "EDIT THIS"

if (SPOTIFY_USERNAME == "EDIT THIS"):
    print(
        "you need to change EDIT THIS in musicInCommon.py line 5 to your own spotify username"
    )
    exit()

SPOTIFY_SCOPE = "playlist-modify-private playlist-modify-public"

token = util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE)
sp = spotipy.Spotify(token)


def main():
    users = usersFromFile("users.txt")
    allTracks = [tracksFromUserPlaylists(user) for user in tqdm(users)]
    overlap = findOverlap(allTracks,
                          (2 if len(users) == 2 else len(users) / 2))

    newPl = sp.user_playlist_create(SPOTIFY_USERNAME,
                                    "overlap of " + ", ".join(users))['uri']

    print(overlap)

    for i in tqdm(range(0, len(overlap), 100)):
        sp.user_playlist_add_tracks(SPOTIFY_USERNAME, newPl,
                                    overlap[i:i + 100])


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


if __name__ == "__main__":
    main()
