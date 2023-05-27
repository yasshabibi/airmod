
import json

import PIL

from  objects import Context
import io, qrcode

import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager

@WebRegister("/qrcodeGen") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine

    # /qrcodeGen?content={TonContenu}
    def asyncGet(self):
        data = self.request.arguments.get("content", None)
        if data is None:
            return self.send_error(400)
        img = qrcode.make(data)
        b = io.BytesIO()
        img.save(b, format="png")
        self.set_header("Content-type", "image/PNG")
        self.write(b.getvalue())
        

    def asyncPost(self):
        return self.send_error(405)
