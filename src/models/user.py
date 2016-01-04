from protorpc import messages

from google.appengine.ext import ndb

class UserForm(messages.Message):
    """User field to modify stored data."""
    user_id = messages.StringField(1,required=True)
    strava_id = messages.StringField(2)
    strava_token = messages.StringField(3)
    
class User(messages.Message):
    """User full information."""
    user_id = messages.StringField(1,required=True)
    email = messages.StringField(2,required=True)
    key = messages.StringField(3)
    strava_id = messages.StringField(4)
    strava_token = messages.StringField(5)

class UserModel(ndb.Model):
    """A model of a user registered in the app"""
    user_id = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(required=True)
    strava_id = ndb.StringProperty(indexed=False)
    strava_token = ndb.StringProperty(indexed=False)
    register_date =  ndb.DateTimeProperty(auto_now_add=True)
    update_date =  ndb.DateTimeProperty(auto_now=True)
 
class UserCollection(messages.Message):
    """Collection of users."""
    items = messages.MessageField(User, 1, repeated=True)