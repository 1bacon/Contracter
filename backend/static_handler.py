import cherrypy
import os

class static_handler:

    def __init__(self, path) -> None:
        self.path = path

    @cherrypy.expose
    def index(self):
        return open(os.path.join(self.path, "../frontend/html/index.html"))