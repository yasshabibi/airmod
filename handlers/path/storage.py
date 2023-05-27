import os
import json
from tornado import iostream

import PIL

from  objects import Context


import tornado.gen
import tornado.web
from helpers import console
from handlers.WebRegister import WebRegister
from helpers.web import requestsManager


chunk_size = 1024 * 1024 * 1 # 1 MiB
@WebRegister(r"/storage/(.*)")
class Handler(requestsManager.asyncRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine


    def asyncGet(self, path = None):
        try:
            # Make sure the screenshot exists
            if path is None or not os.path.isfile("{}/{}".format("storage/", path)):
                raise fileNotFoundException()



            # Output
            filetype = path.split(".")
            filetype = filetype[len(filetype)-1]
            if Context.debug:
                self.set_header("Cache-Control", "no-cache")

            if filetype in ["mp4","webm","avi", "ogg"]:
                self.set_header("Content-type", "video/{}".format(filetype))

            elif filetype in ["jpg", "jpeg", "png", "gif", "bmp", "TIFF"]:
                self.set_header("Content-type", "image/{}".format(filetype))

            elif filetype == "pdf":
                self.set_header("Content-type", "application/pdf")

            elif filetype == "txt":
                self.set_header("Content-type", "text/plain")

            elif filetype == "css":
                self.set_header("Content-type", "text/css")
            
            elif filetype == "html":
                self.set_header("Content-type", "text/html")

            elif filetype == "json":
                self.set_header("Content-type", "application/json")

            else:
                self.set_header("Content-type", "application/octet-stream")

            
            self.set_header("Content-length", os.path.getsize("{}/{}".format("storage/", path)))
            # Read file
            with open("{}/{}".format("storage/", path), "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    try:
                        self.write(chunk) 
                        self.flush() 
                    except iostream.StreamClosedError:
                        break
                    finally:
                        del chunk
            
            
            
        except fileNotFoundException:
            self.set_status(404)

    
class fileNotFoundException(Exception):
    pass
