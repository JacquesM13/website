from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, request, redirect, url_for
from spotify import Spotify

app = Flask(__name__)

bootstrap = Bootstrap4(app)
spotify_agent = Spotify()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/spotify")
def spotify():
    spotify_agent.authorize()
    # print(spotify_agent.auth_url)
    return render_template('spotify.html', top_items= spotify_agent.top_items)

@app.route("/spotify_login")
def spotify_login():
    return redirect(f"{spotify_agent.auth_url}")

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    spotify_agent.get_bearer(auth_code)
    spotify_agent.get_top_items()
    return redirect(url_for('spotify'))


@app.route("/learn")
def learn():
    return render_template('learn.html')

@app.route("/keygen")
def keygen():
    return render_template('keygen.html')


if __name__ == '__main__':
    app.run(debug=True)