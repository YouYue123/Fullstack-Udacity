import webapp2
import os #added
from google.appengine.ext.webapp import template #also added
path = os.path.join(os.path.dirname(__file__), 'index.html') 
## Welcome Page Handler
class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(path, {}))


app = webapp2.WSGIApplication([
                               ('/',Welcome)
                               ],
                              debug=True)