import cherrypy
from static_handler import static_handler
from api import api
import os
path = os.path.abspath(os.path.dirname(__file__))

config = {
    "global" : {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80
    },
    "static": {
        "/":{
            "tools.staticdir.root" : path,
            "tools.staticdir.on" : True,
            "tools.staticdir.dir" : "../frontend"
        }
    },
    "api" : {

    }
}

def start_server():
    cherrypy.config.update(config["global"])
    cherrypy.tree.mount(static_handler(path), "/", config["static"])
    cherrypy.tree.mount(api(path), "/api")  
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    start_server()