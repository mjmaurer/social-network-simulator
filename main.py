from flask import Flask, session, redirect
import tweepy
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    auth = tweepy.OAuthHandler('lVf4ernDov9p75lJ5COIAcUiB', 'XxLd0mZQj6GQtDoaJvbBZlDmEkMqQe1xISCWB1UK9vglMQpHEA')

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'
    
    session['request_token'] = auth.request_token   

    return redirect(redirect_url)


@app.route('/auth')
def twit_auth():  

    return "Here"



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
