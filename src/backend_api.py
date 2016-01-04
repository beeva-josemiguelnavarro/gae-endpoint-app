import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb

import logging

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
    data = messages.MessageField(User, 1, repeated=True)
   
@endpoints.api(name='services', version='v1', description='Backend api services')
class ServicesApi(remote.Service):
    """Services API v1."""
    
    @endpoints.method(message_types.VoidMessage, UserCollection, path='users', http_method='GET',name='listUsers')
    def list_users(self, request):
        usersList = UserModel.query().fetch()
        items = []
        for userItem in usersList:
            items.append(User(user_id=userItem.user_id,
                              email=userItem.email,
                              key=str(userItem.key.id()),
                              strava_id=userItem.strava_id,
                              strava_token=userItem.strava_token))
        return UserCollection(data = items)

    @endpoints.method(message_types.VoidMessage, User,
                      path='user', http_method='POST',
                      name='createUser')
    def insert_user(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            raise endpoints.UnauthorizedException('Authorization required')
        
        logging.info('user '+str(current_user))
        user_id = (current_user.user_id() if current_user is not None and current_user.user_id() is not None
                 else 'Anonymous')
        email = (current_user.email() if current_user is not None
                 else 'Anonymous@gmail.com')
        query = UserModel.query(UserModel.email == email).fetch()
        logging.info('LEN '+str(len(query)))
        userDb = None
        if len(query) > 0:
            userDb = query[0]
            logging.info('DB '+str(userDb))
        else:
            userDb = UserModel(user_id=user_id , email=email)
            userDb.key = ndb.Key('UserModel',email)
            userDb.put()
        
        key = userDb.key.urlsafe()
        #key = userDb.key.id()
        user = User(user_id=userDb.user_id,
                    email=userDb.email,
                    key=str(key))
        
        return user

    KEY_USER = endpoints.ResourceContainer(message_types.VoidMessage,id=messages.StringField(1,variant=messages.Variant.STRING, required=True))
    
    @endpoints.method(KEY_USER, User, path='user/{id}', http_method='GET', name='getUser')  
    def retrieve_user(self, request):
        user_key_id = request.id  
#         logging.info('USE ID '+str(user_key_id))
        user_key = ndb.Key(urlsafe=str(user_key_id))
#         logging.info('KEY '+str(user_key))
        userDb = user_key.get()
#         logging.info('DB '+str(userDb))
        user = None
        if userDb is not None:
            user = User(user_id=userDb.user_id,
                        email=userDb.email,
                        key=str(userDb.key.id()),
                        strava_id=userDb.strava_id,
                        strava_token=userDb.strava_token)
        else:
            message = 'No user with key "%s" exists.' % user_key_id
            raise endpoints.NotFoundException(message)
        return user
    
    USER_UPDATE = endpoints.ResourceContainer(UserForm,
                                              id=messages.StringField(1,variant=messages.Variant.STRING, 
                                                                      required=True))
    
    @endpoints.method(USER_UPDATE, User, path='user/{id}', http_method='PUT', name='updateUser')  
    def update_user(self, request):
        if endpoints.get_current_user() is None:
            raise endpoints.UnauthorizedException('Authorization required')
        
        user_key_id = request.id  
        user_key = ndb.Key(urlsafe=str(user_key_id))
        userDb = user_key.get()
        user = None
        if userDb is not None:
            userDb.user_id = str(request.user_id)
            userDb.strava_id = str(request.strava_id)
            userDb.strava_token = str(request.strava_token)
            userDb.put()
            user = User(user_id=userDb.user_id,
                        email=userDb.email,
                        key=str(userDb.key.id()),
                        strava_id=userDb.strava_id,
                        strava_token = userDb.strava_token)
        else:
            message = 'No user with key "%s" exists.' % str(user_key_id)
            raise endpoints.NotFoundException(message)
        return user
      
app = endpoints.api_server([ServicesApi])