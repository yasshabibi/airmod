
import json

import PIL

from  objects import Context

import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister(r"/orders") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
        

    def asyncGet(self):
        data = Context.mysql.fetchAll("SELECT * from orders")
        for d in data:
            d["user"] = Context.mysql.fetch("Select username, first_name, last_name, adress from users where id = %s;", d["userid"])
            del d["userid"]
            d["track"] = Context.mysql.fetchAll("SELECT o.AID agency_id, a.name, a.adresse, g.lat, g.lon FROM airmod.orders_agencies o join agencies a on o.AID = a.id join agency_geo g on a.id = g.agencyID where o.CID = %s;", d["id"])
        self.set_header("Content-type", "Application/JSON")
        self.write(json.dumps(data, indent=4))