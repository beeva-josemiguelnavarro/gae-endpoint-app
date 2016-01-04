import os

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HelpPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/pages/help.html')
        if(user):
            self.response.write(template.render({'user':user}))
        else:
            self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/help', HelpPage),
], debug=True)


