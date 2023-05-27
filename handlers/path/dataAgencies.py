
import json

import PIL

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister(r"/agency/(.*)") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self, agencyID):
        data = Context.mysql.fetch("SELECT name, type, description, adresse, phone, service, mail FROM agencies WHERE id = %s", agencyID)
        if data is None: data = {}
        data["banner"] = "https://t3.ftcdn.net/jpg/03/02/04/06/360_F_302040655_IEH9RyDlu7LL8YCLjgL1IskhrpOlmlSv.jpg"

        data["schedules"] = Context.mysql.fetchAll("SELECT * FROM agency_schedules WHERE AgencyID = %s", agencyID)
        data["pos"] = Context.mysql.fetch("SELECT * FROM airmod.agency_geo WHERE agencyID = %s;", agencyID)
        self.set_header("Content-type", "Application/JSON")
        self.write(json.dumps(data, sort_keys=True, indent=4))
        

    def asyncPost(self):
        return self.send_error(405)
