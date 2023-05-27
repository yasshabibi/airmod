
import json

import PIL

from  objects import Context
import io, qrcode

import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager
import urllib.parse

@WebRegister(r"/settings") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
        

    def asyncPost(self, orderID, agencyID):
            raw = urllib.parse.unquote(self.request.body.decode("utf-8"))
            data = {}
            split = raw.split("&")
            split = [a.split("=") for a in split]
            for s in split:
                data[s[0]] = s[1]
            
            if self.isLoggedIn:
                id= self.userContext["id"]
                pw = data["pw"].encode("utf-8")
                data = Context.mysql.fetch("INSERT INTO user VALUE (%s,%s,%s,%s,%s,%s) WHERE id='id'",data["username"],pw,data["frist_name"],data["last_name"],data["email"],data["adress"])
                