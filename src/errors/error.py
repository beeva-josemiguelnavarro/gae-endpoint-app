import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('IP: '+self.request.remote_addr+'\n')
        self.response.out.write('URL: '+self.request.url+'\n')
        self.response.out.write('ERROR: 404 Page Not Found\n')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)