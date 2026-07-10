from flask_bootstrap import Bootstrap4
from flask import Flask, render_template

app = Flask(__name__)

bootstrap = Bootstrap4(app)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/spotify")
def spotify():
    return render_template('spotify.html')

@app.route("/learn")
def learn():
    return render_template('learn.html')

@app.route("/keygen")
def keygen():
    return render_template('keygen.html')

@app.route("/treedentify")
def treedentify():
    return render_template('treedentify.html')

if __name__ == '__main__':
    app.run(debug=True)