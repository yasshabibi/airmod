
import json

import PIL

from  objects import Context
import io, qrcode

import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister(r"/orders/(\d*)/add/([a-z\d]{40})") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
        

    def asyncPost(self, orderID, agencyID):
        if not self.isLoggedIn:
            return self.send_error(401)
        try:
            Context.mysql.execute("INSERT INTO `airmod`.`orders_agencies` (`CID`, `AID`) VALUES (%s, %s);", orderID,agencyID)
        except:
            self.send_error(403)
            return