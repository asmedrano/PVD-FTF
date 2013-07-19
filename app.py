import webapp2
import sys
import cgi
sys.path.insert(1, 'libs')
import logging
from finder import *
import json

from google.appengine.ext import db

class DBCachedResponse(db.Model):
    query_type = db.StringProperty() # single or all
    query_meta = db.StringProperty() # any related info
    time = db.DateTimeProperty(auto_now_add=True)
    response = db.TextProperty()

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        truck = cgi.escape(self.request.get('truck'))
        if truck:
            try:
                result = json.dumps(get_truck(truck))
                put_result(result, truck)
            except TwitterHTTPError:
                result = get_from_cache(truck)

            if result != None:
                self.response.write(result)
            else:
                self.response.write("{'error':'Service Unavailable'}")

        else:
            # get all of dem.
            try:
                result = json.dumps(get_trucks())
                put_result(result, truck)
            except TwitterHTTPError:
                result = get_from_cache(truck)
            if result != None:
                self.response.write(result)
            else:
                self.response.write("{'error':'Service Unavailable'}")


class TrucksHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(FOOD_TRUCK_HANDLES))


def put_result(result, truck=''):

    result = DBCachedResponse(response=result)
    if truck != '':
        # store result for "all request"
        result.query_type = "single"
        result.query_meta = truck
    else:
        # store a result for a single truck
        result.query_type = "all"

    result.put()


def get_from_cache(truck=''):
    if truck is '':
        logging.info("Serving all request from cache")
        # get the last result for a "all request"
        q = DBCachedResponse.all()
        q.filter("query_type =", "all")
        q.order("-time")
        result = q.get()
        if result:
            return result.response
        else:
            return None
    else:
        # get the last known result for this truck
        logging.info("Serving single request from cache: %s" % truck)
        q = DBCachedResponse.all()
        q.filter("query_meta =", truck)
        q.order("-time")
        result = q.get()
        if result:
            return result.response
        else:
            return None


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/trucks', TrucksHandler)
], debug=True)

def main():
    # Set the logging level in the main function
    # See the section on Requests and App Caching for information on how
    # App Engine reuses your request handlers when you specify a main function
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
