import os

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user() is not None:
            self.redirect('/dashboard')
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/pages/home.html')
            self.response.write(template.render())
            
class LogInPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user() is not None:
            self.redirect('/dashboard')
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
            self.response.write(template.render({'user':user}))
        else:
            self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LogInPage),
    ('/logout', LogOutPage),
    ('/help', HelpPage),
], debug=True)


