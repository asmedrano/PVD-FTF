import webapp2
import sys
import cgi
sys.path.insert(1, 'libs')

from finder import *
import json


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        #self.response.write(json.dumps(get_trucks()))
        #self.response.write("{}")
        truck = cgi.escape(self.request.get('truck'))
        if truck:
            self.response.write(json.dumps(get_truck(truck)))
        else:
            # get all of dem.
            self.response.write(json.dumps(get_trucks()))

class TrucksHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(FOOD_TRUCK_HANDLES))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/trucks', TrucksHandler)
], debug=True)
