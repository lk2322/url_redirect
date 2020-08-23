import flask
import os
import db
import sys
import requests
import random
import errors
import string
app = flask.Flask(__name__)

DOMAIN = 'example.com'
HOST_IP = '192.168.1.200'

@app.route('/')
def main():
    return flask.render_template('index.html')

@app.route('/get')
def index():
    data = flask.request.args
    r_url = data['r_url']
    o_url = data['o_url']
    if r_url.startswith('/') or r_url.startswith('\\') or r_url.startswith('?'):
        r_url = r_url[1:]
    if '\\' in r_url or '?' in r_url:
        flask.g.r_url = """Can not use '?' and '\\' in link"""
        return flask.render_template('result.html') 

    # Для рандомных ссылок
    ###########################
    if r_url == '':
        r_url = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
        db.add_url(o_url, r_url, rerol=True)
        flask.g.r_url = DOMAIN + r_url
        return flask.render_template('result.html') 
    ###########################
    try:
        db.add_url(o_url, r_url)
    except errors.LinkAlreadyExistsError as e:
        flask.g.r_url = 'This link already exists: lk2322.asuscomm.com/' + e.r_url
    else:
        flask.g.r_url = DOMAIN + r_url
        return flask.render_template('result.html')    

    return flask.render_template('result.html')
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    res = db.get_url(path)
    if res != 404:
        if res.startswith('http://') or res.startswith('https://'):
            return flask.redirect(res)
        else:
            return flask.redirect('http://' + res)
    return flask.abort(404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 80))
    app.run(host=HOST_IP, port=port)