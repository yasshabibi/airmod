
import json

import PIL

from  objects import Context
import io, qrcode

import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister(r"/orders/make") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
        

    def asyncPost(self):
        if (not self.isLoggedIn):
            return self.send_error(401)
        id = Context.mysql.fetch("INSERT INTO `airmod`.`orders` (`userid`) VALUES (%s);SELECT last_insert_id() id;", self.userContext)["id"]
        self.write({"id":id})
        
