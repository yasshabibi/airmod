
import json
import traceback

import PIL

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager
import urllib.parse
from objects import Context
import bcrypt
from helpers import generalHelper

@WebRegister("/register") # http://4.tcp.eu.ngrok.io:10360/status
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self):
        return self.send_error(405)
        

    def asyncPost(self):
        try:
            # username=aaa&first=aaa&last=aa&mail=aaa%40aa.aa&pw=aaa
            raw = urllib.parse.unquote(self.request.body.decode("utf-8"))
            # username=aaa&first=aaa&last=aa&mail=aaa@aa.aa&pw=aaa
            data = {}
            split = raw.split("&")
            # ["username=aaa", "first=aaa", "last=aa", "mail=aaa@aa.aa", "pw=aaa"]
            split = [a.split("=") for a in split]
            # [["username", "aaa"], [...]]
            for s in split:
                data[s[0]] = s[1]
            # {'username': 'aaa', 'first': 'aaa', 'last': 'aa', 'mail': 'aaa@aa.aa', 'pw': 'aaa'}
            salt = bcrypt.gensalt()
            pw = data["pw"].encode("utf-8")
            hashed = bcrypt.hashpw(pw, salt).decode('utf-8')

            Context.mysql.execute("INSERT INTO `airmod`.`users` (`username`, `password_hash`, `first_name`, `last_name`, `email`, `type`) VALUES (%s, %s, %s, %s, %s, %s);", data["username"], hashed, data["first"], data["last"], data["mail"], data["type"])
            
            lastID = Context.mysql.fetch("SELECT id from users where username = %s", data["username"])["id"]
            token = generalHelper.randomString(32)
            Context.mysql.execute("INSERT INTO `airmod`.`tokens` (`token`, `uid`) VALUES (%s, %s);", token, lastID)
            self.set_secure_cookie("Authorization", token)
            self.redirect("/storage/{}/index.html".format({"1": "client", "2": "delivery", "3":"seller"}[str(data["type"])]))
        except Exception as e:
            console.error(traceback.format_exc())