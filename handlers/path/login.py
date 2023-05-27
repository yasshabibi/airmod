
import json

import PIL
import bcrypt

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager
from helpers import generalHelper
import urllib.parse

@WebRegister("/login") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self):
        return self.send_error(405)
        

    def asyncPost(self):
        
        raw = urllib.parse.unquote(self.request.body.decode("utf-8"))
        # username=aaa&first=aaa&last=aa&mail=aaa@aa.aa&pw=aaa
        data = {}
        split = raw.split("&")
        # ["username=aaa", "first=aaa", "last=aa", "mail=aaa@aa.aa", "pw=aaa"]
        split = [a.split("=") for a in split]
        # [["username", "aaa"], [...]]
        for s in split:
            data[s[0]] = s[1]

        userData = Context.mysql.fetch("SELECT id, password_hash from users where username = %s", data["username"])
        if userData is None or not bcrypt.checkpw(data["pw"].encode("utf-8"), userData["password_hash"].encode("utf-8")):
            self.write({"error": "Wrong username or password"})

        lastID = userData["id"]
        token = generalHelper.randomString(32)
        Context.mysql.execute("INSERT INTO `airmod`.`tokens` (`token`, `uid`) VALUES (%s, %s);", token, lastID)
        self.set_secure_cookie("Authorization", token)
        self.redirect("/storage/{}/index.html".format({"1": "client", "2": "delivery", "3":"seller"}[str(data["type"])]))
        return self.send_error(405)
