from flask import request
from flask import Flask
from flask import Response

import musicInCommon as MIC

app = Flask(__name__)

MIC.initClientCredentials()


@app.route('/')
def index():
    with open('index.html') as f:
        return f.read()


@app.route("/submitUsernames", methods=['POST'])
def submitUsernames():
    users = [name.strip() for name in request.form['usernames'].split("\n")]

    return MIC.formatTracklist((MIC.getPlaylistTracks(users)))


if __name__ == '__main__':
    app.run()
