
import json

import PIL

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister("/status") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self):
        data = {
            "Version" : "Alpha 0.1",
        }
        
        self.set_header("Content-type", "Application/JSON")
        self.write(json.dumps(data))
        

    def asyncPost(self):
        return self.send_error(405)
