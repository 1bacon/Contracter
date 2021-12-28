import cherrypy
import database

class api:

    def __init__(self, path) -> None:
        self.path = path
        self.DB = database.DB(path)

    @cherrypy.expose
    def index(self):
        return "a"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def user(self, name=""):
        users = self.DB.get_user(name)
        return users

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def user_add(self):
        body = cherrypy.request.json

        if not ("name" in body and "password" in body and "pretty_name" in body) or not (type(body["name"]) == str and type(body["password"]) == str and type(body["pretty_name"]) == str):
            cherrypy.response.status = 400
            return "bad request. What u doing? name password(pls already hashed) pretty_name is required"

        r =  self.DB.add_user(body["name"], body["password"], body["pretty_name"])
        cherrypy.response.status = r[0]
        return r[1]
        
    #@cherrypy.expose()
    def create_db(self):
        return self.DB.create_tables() 
