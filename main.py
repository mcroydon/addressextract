from addresses import parse_addresses, tag_addresses
from django.utils import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <head><title>Address Extractor</title></head>
        <body>

          <h3>Address extractor</h3>
          <p>Returns a JSON dictionary whose key is <code>addresses</code> and whose value
          is a list of a tuple of extracted addresses.</p>
          <p>To use this service programmatically, <code>POST</code> your content to
          http://addressextract.appspot.com/extract/ urlencoded with the key <code>content</code>.</p>
          <form action="/extract/" method="post">
            <div><textarea name="content" rows="10" cols="80"></textarea></div>
            <div><input type="submit" value="Go!"></div>
          </form>

          <h3>Address tagger</h3>
          <p>Returns a <code>text/html</code> representation of the posted content with
          addresses wrapped in <code>addr</code> tags.</p>
          <p>To use this service programmatically, <code>POST</code> your content to
          http://addressextract.appspot.com/tag/ urlencoded with the key <code>content</code>.</p>
          <form action="/tag/" method="post">
            <div><textarea name="content" rows="10" cols="80"></textarea></div>
            <div><input type="submit" value="Go!"></div>
          </form>

          <p>Powered by ebdata.nlp.addresses from the <a href="http://www.everyblock.com/code/">Everyblock source</a>.</p>
        </body>
      </html>""")


class Extract(webapp.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(simplejson.dumps({'addresses' : parse_addresses(self.request.get('content'))}))

class Tag(webapp.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(tag_addresses(self.request.get('content')))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/extract/', Extract),
                                      ('/tag/', Tag)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()