from ast import arg
import mysql.connector
from mysql.connector.connection import MySQLConnection
import mysql.connector.pooling
from objects import Context
from helpers import console
from time import  sleep

class Db:
    def __init__(self) -> None:
        dbConfig = {
            "host" : Context.configManager.config.get("db", "host"),
            "username" : Context.configManager.config.get("db", "username"),
            "password" : Context.configManager.config.get("db", "password"),
            "database" : Context.configManager.config.get("db", "database"),
            "pool_size" : int(Context.configManager.config.get("db", "workers")),
            "pool_name" : "KatayoPool",
            "pool_reset_session" : True
        }
        self.cnx:MySQLConnection = mysql.connector.pooling.MySQLConnectionPool(**dbConfig)
        

    def fetch(self, request, *args):


        console.debug(f"sql fetch : {request}" % args)
        con = self.cnx.get_connection()
        cur =con.cursor(dictionary=True, buffered=True)
        cur.execute(request, args)
        c = cur.fetchone()
        console.debug(f"sql response : {c}")
        con.close()
        return c

    def fetchAll(self, request, *args):

        console.debug(f"sql fetchAll : {request}" % args)
        con = self.cnx.get_connection()
        cur = con.cursor(dictionary=True, buffered=True)
        cur.execute(request, args)
        c = cur.fetchall()
        console.debug(f"sql response : {c}")
        con.close()
        return c

    def execute(self, request, *args):
        print('aaa')
        console.debug(f"sql Execute : {request}" % args)
        con = self.cnx.get_connection()
        cur = con.cursor(dictionary=True, buffered=True)
        cur.execute(request, args)
        con.commit()
        con.close()

    def ping(self):
        self.fetch("SELECT 1+1")