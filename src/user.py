import os
import cgi
import logging

from google.appengine.api import users
#from google.appengine.ext import ndb

from models.user import UserModel

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class RegisterPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if(user):
            self.redirect('/dashboard')
        else:            
            template = JINJA_ENVIRONMENT.get_template('templates/pages/register.html')
            self.response.write(template.render())

    def post(self):
        username = cgi.escape(self.request.get("inputUsername"))
        email = cgi.escape(self.request.get("inputEmail"))
        password = cgi.escape(self.request.get("inputPassword"))
        if(email is not None and password is not None):
            logging.info('Register '+username+" - "+email+" - "+password)
            user = UserModel(user_id=username, email=email, password=password)
            userKey = user.put()
            logging.info(userKey)
            logging.info(userKey.id())
            logging.info(userKey.kind())
            userDb = userKey.get()
            logging.info(userDb)
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/pages/register.html')
            self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/register', RegisterPage),
], debug=True)