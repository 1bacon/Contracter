import cherrypy

class api:
    @cherrypy.expose()
    def index(self):
        return "a"
