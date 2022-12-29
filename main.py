from multiprocessing import context
from multiprocessing.sharedctypes import Value
import os
import sys
from multiprocessing.pool import ThreadPool
import traceback
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
from objects import Context
import pkgutil
import logging
import threading


from handlers.WebRegister import WebStore

from helpers.config import configManager
from helpers import console
from helpers import database
from helpers import generalHelper


def make_app():
    return tornado.web.Application(WebStore.items())

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.printAscii()
        generalHelper.CheckFolders()
        Context.runtimeLog = open(".data/logs/runtime.log", "w")
        Context.errorLog = open(".data/logs/errors.log", "w")
        Context.pool = ThreadPool(24)

        console.writeColored("Hello! this is Airmod API.", console.Colors.GREEN)
        console.write("> Reading config file... ", True)
        Context.configManager = configManager("config.ini")
        if Context.configManager.default:
            console.writeCaution()
            console.writeColored("[!] config.ini not found. A default one has been generated.", console.Colors.YELLOW)
            console.writeColored("[!] Please edit your config.ini and run the server again.", console.Colors.YELLOW)
            raise Exception()
        
        if not Context.configManager.isValid():
            console.writeFailure()
            console.writeColored("[!] Invalid config.ini. Please configure it properly", console.Colors.RED)
            console.writeColored("[!] Delete your config.ini to generate a default one", console.Colors.RED)
            raise Exception()
        else:
            console.writeSuccess()

        console.write("> Checking folders... ", True)
        paths = [".data"]
        for i in paths:
            if not os.path.exists(i):
                os.makedirs(i, 0o770)
        console.writeSuccess()

        try:
            console.write("> Connecting to MySQL database... ", True)
            Context.mysql = database.Db()
            console.writeSuccess()
        except:
            # Exception while connecting to db
            console.writeFailure()
            console.writeColored("[!] Error while connection to database. Please check your config.ini and run the server again", console.Colors.RED)
            raise

        console.writeColored("> Loading Delta Dash Packets ", console.Colors.BLUE)
        generalHelper.registerAllHandlers("handlers/path")



        if generalHelper.stringToBool(Context.configManager.config.get("server", "debug")):
            Context.debug = True
            console.writeColored("[!] Katayo is currently in debug mode", console.Colors.YELLOW)

        serverPort = int(Context.configManager.config.get("server", "port"))
        console.writeColored("> Listening on: 0.0.0.0:{} \n> Ready to accept connections".format(serverPort), console.Colors.GREEN)
        Context.app = make_app()

        logging.getLogger('tornado.access').disabled = True
        threading.Thread(target=lambda:generalHelper.SideLoops()).start() #Run side tasks

        # Set Secure cookies with some encryption
        if (not os.path.isfile(".data/secret.key")):
            with open(".data/secret.key", 'w') as f:
                f.write(generalHelper.randomString(4096))
        with open(".data/secret.key", 'r') as f:
            Context.app.settings["cookie_secret"] = f.read()

            
        Context.app.listen(serverPort)
        tornado.ioloop.IOLoop.instance().start()
        
    finally:
        console.writeColored("> Closing server", console.Colors.RED)
        if Context.mysql is not None:
            Context.mysql.cnx.close()
        console.writeColored("> Seeya !", console.Colors.GREEN)
        Context.runtimeLog.close()
        
