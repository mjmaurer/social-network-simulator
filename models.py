from google.appengine.ext import db

class Tok(db.Model):
    oauth_token_secret = db.StringProperty(required = True)
    oauth_token = db.StringProperty(required = True)