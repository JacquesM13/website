from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, request, redirect, url_for
from spotify import Spotify

app = Flask(__name__)

bootstrap = Bootstrap4(app)
spotify_agent = Spotify()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/spotify", methods=["GET", "POST"])
def spotify():
    spotify_agent.authorize()
    print(spotify_agent.auth_url)
    return render_template('spotify.html')

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    return render_template('callback.html', auth_code=auth_code)

@app.route("/learn")
def learn():
    return render_template('learn.html')

@app.route("/keygen")
def keygen():
    return render_template('keygen.html')


if __name__ == '__main__':
    app.run(debug=True)