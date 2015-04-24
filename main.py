from flask import Flask, session, redirect, request, send_from_directory, render_template, jsonify
import tweepy
from models import Tok
import urllib
from sets import Set
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

    return render_template('twitter.html')

@app.route('/get_twit_graph')
def get_twit_graph():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(session['access_token'], session['access_token_secret'])

    api = tweepy.API(auth)

    authUser = api.me()
    edgeCount = 0
    userSet = Set()
    edgeList = []
    userSet.add(UserInfo(authUser.screen_name, authUser.id))

    # Get friends and followers of authenticated user
    try:
        for user in tweepy.Cursor(api.followers).items(20):
            userSet.add(UserInfo(user.screen_name, user.id))
            edgeList.append({'id':'e'+ str(edgeCount), 'source':str(user.id), 'target':str(authUser.id)})
            edgeCount = edgeCount + 1
    except tweepy.TweepError:
        app.logger.debug("Rate limited init follow. Users so far: " + str(len(userSet)))

    try:
        for user in tweepy.Cursor(api.friends).items(20):
            userSet.add(UserInfo(user.screen_name, user.id))
            edgeList.append({'id':'e'+ str(edgeCount), 'source':str(authUser.id), 'target':str(user.id)})
            edgeCount = edgeCount + 1
    except tweepy.TweepError:
        app.logger.debug("Rate limited in init friends. Users so far: " + str(len(userSet)))

    firstUsers = list(userSet)
    # Get friends and followers of up to 14 more users (due to rate limit)
    for i in range(min(14, len(firstUsers))):
        curUser = firstUsers[i]

        try:
            for user in tweepy.Cursor(api.followers, screen_name=curUser.name).items(20):
                userSet.add(UserInfo(user.screen_name, user.id))
                edgeList.append({'id':'e'+ str(edgeCount), 'source':str(user.id), 'target':str(curUser.userId)})
                edgeCount = edgeCount + 1
        except tweepy.TweepError:
            app.logger.debug("Follow rate limited at user: " + str(i))


        try:
            for user in tweepy.Cursor(api.friends, screen_name=curUser.name).items(20):
                userSet.add(UserInfo(user.screen_name, user.id))
                edgeList.append({'id':'e'+ str(edgeCount), 'source':str(curUser.userId), 'target':str(user.id)})
                edgeCount = edgeCount + 1
        except tweepy.TweepError:
            app.logger.debug("Friends rate limited at user: " + str(i))

    nodesList = []
    for user in userSet:
        nodesList.append({'id':str(user.userId), 'label':str(user.name), 'size':9})


    return jsonify(nodes=nodesList, edges=edgeList)


class UserInfo:

    def __init__(self,name,userId):
        self.name = name
        self.userId = userId

    def __hash__(self):
        return hash((self.name, self.userId))

    def __eq__(self, other):
        return (self.name, self.userId) == (other.name, other.userId)

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
