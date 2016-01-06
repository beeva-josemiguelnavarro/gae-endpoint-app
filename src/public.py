import os
import logging

from google.appengine.ext import ndb
from google.appengine.api import users

from models.user import UserModel
import jinja2
import webapp2

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
       
class LogInPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user() is not None:
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

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
    ('/login', LogInPage),
    ('/logout', LogOutPage),
    ('/help', HelpPage),
], debug=True)


