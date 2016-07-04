# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request, session, url_for, flash
import libsonic
from base64 import b64encode

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
))

@app.route('/artwork')
def show_artwork(image=None):
    try:
        conn = build_url()
        json_data = conn.getNowPlaying()
        if 'entry' in json_data['nowPlaying']:
            if type(json_data['nowPlaying']['entry']) is not list:
                for field in json_data['nowPlaying']['entry']:
                    if field == 'username':
                        if json_data['nowPlaying']['entry'][field] == username:
                            image = b64encode(conn.getCoverArt(json_data['nowPlaying']['entry']['coverArt'], size=500).read())
            else:
                for user in json_data['nowPlaying']['entry']:
                    if user['username'] == username:
                        image = b64encode(conn.getCoverArt(user['coverArt'], size=500).read())
            return render_template('layout.html', image=image, playing=True)
        else:
            return render_template('layout.html', playing=False)
    except Exception as e:
        flash(e)
        return render_template('layout.html', error=e)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        global username, password
        username = request.form['username']
        password = request.form['password']
        if username == '':
            error = 'Invalid username'
        elif password == '':
            error = 'Invalid password'
        elif not connection():
            error = 'Invalid username/password'
        else:
            session['logged_in'] = True
            return redirect(url_for('show_artwork'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_artwork'))

def connection():
    try:
        conn = build_url()
        if conn.ping():
            return True
        else:
            return False
    except Exception as e:
        flash(e)
        return False

def build_url():
    try:
        conn = libsonic.Connection('https://subsonic.freestylephenoms.com',
                                   username,
                                   password,
                                   apiVersion='1.12.0',
                                   port=443,
                                   insecure=True
                                   )
        return conn
    except Exception as e:
        flash(e)
        return None

if __name__ == "__main__":
    app.run(debug=True)
