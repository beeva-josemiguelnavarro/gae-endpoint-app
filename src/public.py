import os
import logging
import httplib2
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

from models.user import UserModel
from models.user import UserCredentials

import jinja2
import webapp2

from oauth2client import client
from google.appengine.api import memcache

flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/userinfo.email',
    redirect_uri='http://localhost:8080/oauth2callback')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def add_user(user):
    logging.info('user '+str(user))
    user_id = (user.user_id() if user is not None and user.user_id() is not None
             else 'Anonymous')
    email = (user.email() if user is not None
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
    return userDb

class HomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is not None:
            user_app = add_user(user)
            template = JINJA_ENVIRONMENT.get_template('templates/pages/dashboard.html')
            self.response.write(template.render(user=user_app,))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/pages/home.html')
            self.response.write(template.render())
        
class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        pass
           
class Oauth2CallbackHandler(webapp2.RequestHandler):
    def get(self):
        auth_code = self.request.get('code')
        if auth_code is not None:
            logging.critical(auth_code)
            credentials = flow.step2_exchange(auth_code)
            token_response = credentials.token_response
            token = token_response.get('token_type')+' '+token_response.get('access_token')
            token_expire_in = credentials.token_expiry
            user = users.get_current_user().email()
            key = "token_"+user
            memcache_client = memcache.Client()
            memcache_client.add(key=key, value=token, time=token_expire_in)
            self.response.set_cookie('Authorization',token,expires=token_expire_in,path='/',domain='appspot.com')
            self.redirect('/')
        else:
            error = self.request.get('error')
            logging.critical(error)
    
class LogInPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user() is not None:
            auth_uri = flow.step1_get_authorize_url()
            logging.critical(str(auth_uri))
            self.redirect(str(auth_uri))
        else:
            self.redirect(users.create_login_url('/login'))        

class LogOutPage(webapp2.RequestHandler):    
    def get(self):
        if users.get_current_user() is not None:
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect('/')

class HelpPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/pages/help.html')
        if(user):
            self.response.write(template.render(user=user,))
        else:
            self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/oauth2callback',Oauth2CallbackHandler),
    ('/login', LogInPage),
    ('/logout', LogOutPage),
    ('/help', HelpPage),
], debug=True)


