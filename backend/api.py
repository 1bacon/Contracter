import cherrypy

import database

class api:

    def __init__(self, path) -> None:
        self.path = path
        self.DB = database.DB(path)

    @cherrypy.expose()
    def index(self):
        return "a"

    #@cherrypy.expose()
    def create_db(self):
        return self.DB.create_tables() 
