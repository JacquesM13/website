from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
from spotify import Spotify

app = Flask(__name__)

bootstrap = Bootstrap5(app)
spotify_agent = Spotify()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/spotify")
def spotify():
    if spotify_agent.logged_in:
        top_type = request.args.get('top_type')
        if top_type:
            spotify_agent.get_top_items(top_type)
            return render_template('spotify.html', logged_in= spotify_agent.logged_in, top_items= spotify_agent.top_items)
    spotify_agent.get_top_items()
    return render_template('spotify.html', logged_in= spotify_agent.logged_in, top_items= spotify_agent.top_items)

@app.route("/spotify_login")
def spotify_login():
    spotify_agent.authorize()
    return redirect(f"{spotify_agent.auth_url}")

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    spotify_agent.get_bearer(auth_code)
    return redirect(url_for('spotify'))

@app.route("/learn")
def learn():
    return render_template('learn.html')

@app.route("/keygen")
def keygen():
    return render_template('keygen.html')

@app.route("/paletter")
def paletter():
    return render_template('paletter.html')

if __name__ == '__main__':
    app.run(debug=True)