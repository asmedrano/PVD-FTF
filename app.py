import webapp2
from finder import *
import json

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        #self.response.write(json.dumps(get_trucks()))
        self.response.write("{}")


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
