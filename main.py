from flask import Flask, session, redirect, request, send_from_directory, render_template
import tweepy
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
consumer_key = 'lVf4ernDov9p75lJ5COIAcUiB'
consumer_secret = 'XxLd0mZQj6GQtDoaJvbBZlDmEkMqQe1xISCWB1UK9vglMQpHEA'

@app.route('/')
def main():
    return render_template('home.html')


@app.route('/twitter')
def twit_start():
    """Return a friendly HTTP greeting."""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    api = tweepy.API(auth)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'
    
    session['request_token'] = auth.request_token   

    return redirect(redirect_url)

@app.route('/auth')
def twit_auth():  

    verifier = request.args.get('oauth_verifier')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.request_token = session['request_token']
    del session['request_token']

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
