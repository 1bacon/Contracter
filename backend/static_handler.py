import cherrypy
import os
path = os.path.abspath(os.path.dirname(__file__))

class static_handler:
    @cherrypy.expose
    def index(self):
        return open(f"{path}/../frontend/index.html", "r")