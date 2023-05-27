from typing import List
from helpers import database

pool = None
runtimeLog = None
errorLog = None
configManager = None
app = None
mysql:database.Db = None
debug:bool = False