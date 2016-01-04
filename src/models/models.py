from google.appengine.ext import ndb

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
class UserModel(ndb.Model):
    """A main model of a user registered in the app"""
    user_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty(indexed=False)
#     password = ndb.StringProperty(indexed=False)
#     strava_id = ndb.IntegerProperty()
    register_date =  ndb.DateTimeProperty(auto_now_add=True)
    update_date =  ndb.DateTimeProperty(auto_now=True)