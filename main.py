from flask import Flask, session, redirect, request, send_from_directory, render_template
import tweepy
from models import Tok
import urllib
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,asdf?RT'

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app_key = 'avslejf23qwl435kjl4kqnqi3oj5qwq3'
consumer_key = 'lVf4ernDov9p75lJ5COIAcUiB'
consumer_secret = 'XxLd0mZQj6GQtDoaJvbBZlDmEkMqQe1xISCWB1UK9vglMQpHEA'

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def main():
    return render_template('home.html')


@app.route('/facebook')
def facebook_start(): 
    return render_template('facebook.html')


@app.route('/twitter')
def twit_start():

    user = id_generator(size=12)

    getVars = {'id': user}
    url = 'http://social-simulator.appspot.com/auth?'
    callback = url + urllib.urlencode(getVars)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)

    api = tweepy.API(auth)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'

    token = Tok(key_name=user,oauth_token_secret=auth.request_token['oauth_token_secret'],oauth_token=auth.request_token['oauth_token'])
    token.put()

    return redirect(redirect_url)

@app.route('/auth')
def twit_auth():  
    user = request.args.get('id')
    verifier = request.args.get('oauth_verifier')
    token = Tok.get_by_key_name(user)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
    request_token = {}
    request_token['oauth_token_secret'] = token.oauth_token_secret
    request_token['oauth_token'] = token.oauth_token
    auth.request_token = request_token
    token.delete()

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return 'Error! Failed to get access token.'

    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(session['access_token'], session['access_token_secret'])

    api = tweepy.API(auth)
    api.update_status(status='tweepy + oauth!')

    return "DID ITT"


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/templates/<path:path>')
def send_html(path):
    return send_from_directory('templates', path)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
