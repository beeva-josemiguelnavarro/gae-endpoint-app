import os

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/pages/home.html')
        if(user):
            self.redirect('/dashboard')
        else:
            self.response.write(template.render())
            
class LogInPage(webapp2.RequestHandler):

    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            self.redirect('/dashboard')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class LogOutPage(webapp2.RequestHandler):
    
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()
        
        if user:
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect('/')
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write('testGAE form Eclipse')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LogInPage),
    ('/logout', LogOutPage),
], debug=True)


