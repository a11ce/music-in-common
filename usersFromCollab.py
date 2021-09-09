import spotipy
import spotipy.util as util
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
    listLink = input("enter link to collab playlist\n> ")
    batch = sp.user_playlist_tracks("oxa11ce", listLink)
    users = set([item['added_by']['id'] for item in batch['items']])
    while batch['next']:
        batch = sp.next(batch)
        users.update([item['added_by']['id'] for item in batch['items']])

    [print(u) for u in users]


if __name__ == "__main__":
    main()
