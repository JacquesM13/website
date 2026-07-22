from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
from spotify import Spotify

app = Flask(__name__)

bootstrap = Bootstrap5(app)
spotify_agent = Spotify()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/spotify", defaults={'top_type': 'artists'})
@app.route("/spotify/<top_type>")
def spotify(top_type):
    if spotify_agent.logged_in:
        # top_type = request.args.get('top_type')
        period = request.args.get('period')
        spotify_agent.get_top_items(top_type= top_type, period= period)

        if top_type == 'tracks':
            return render_template('spotify.html', logged_in=spotify_agent.logged_in,
                                   top_type= top_type, top_items= spotify_agent.top_tracks, period= period)
        else:
            return render_template('spotify.html', logged_in= spotify_agent.logged_in,
                                   top_type= top_type, top_items= spotify_agent.top_artists, period= period)
    return render_template('spotify.html', logged_in= spotify_agent.logged_in)

@app.route("/spotify_login")
def spotify_login():
    spotify_agent.authorize()
    return redirect(f"{spotify_agent.auth_url}")

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    spotify_agent.get_bearer(auth_code)
    return redirect(url_for('spotify'))

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/keygen")
def keygen():
    return render_template('keygen.html')

@app.route("/paletter")
def paletter():
    return render_template('paletter.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)