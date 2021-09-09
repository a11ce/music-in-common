# Music In Common

> Generate spotify playlists from the public playlists of multiple people

## Setup

- Download with `git clone git@github.com:a11ce/music-in-common.git`
- Install dependencies with `pip3 install spotipy tqdm`

## Usage

- Edit `users.txt` to have one spotify profile ID per line. To find the ID of a profile, go to `Share > Copy Link`, and the ID is between `user/` and `?` in the copied link. It might be the same as your display name but not always. 
    - You can run `python3 usersFromCollab.py` and enter the link to a collaborative playlist to get the usernames of everyone who has added a song.
    
- Run `python3 musicInCommon.py`. This can take a while depending on the number of users or the size/number of their public playlists. A new playlist will be created under your (as per L5 of the script) account.


--- 

All contributions are welcome by pull request or issue.

music-in-common is licensed under GNU General Public License v3.0. See [LICENSE](../master/LICENSE) for full text.
