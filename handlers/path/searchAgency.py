
import json

import PIL

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister(r"/search") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self):
        query = self.request.arguments.get("q", [b""])[0].decode("utf-8") 
        
        query = f"%{query}%"
        data = Context.mysql.fetchAll("SELECT id, name, type FROM airmod.agencies WHERE name LIKE %s OR service LIKE %s OR description LIKE %s OR mail LIKE %s OR type LIKE %s LIMIT 10;", query, query, query, query, query)
        self.set_header("Content-type", "Application/JSON")
        self.write(json.dumps(data, sort_keys=True, indent=4))
        

    def asyncPost(self):
        return self.send_error(405)
