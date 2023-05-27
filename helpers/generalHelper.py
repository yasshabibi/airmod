
import io
import random
import string
import os
import hashlib
import traceback
import zipfile

from objects import Context
from helpers import console   
import time
from objects import Context

def CheckFolders():
    folderList = [
        ".data",
        ".data/storage",
        ".data/logs"
    ]

    for folder in folderList:
        if not os.path.exists(os.path.join(os.getcwd(), folder)):
            os.makedirs(os.path.join(os.getcwd(), folder))

def stringToBool(string:str)->bool:
    return string.lower() in ("true", "1")

def randomString(length:int=8)->string:
    out = str()
    for _ in range(length):
        out += random.choice(string.ascii_letters + string.digits)
    return out

def registerAllHandlers(path):
    files = os.listdir(os.path.join(os.getcwd(), path))
    baseimport = path.replace("/", ".")
    baseimport.strip(".")
    for file in files:
        if file.endswith(".py"):
            file = file.replace(".py", "")
            console.writeColored("loading Handler {}{}{} ...".format(console.Colors.ENDC,file, console.Colors.BLUE), console.Colors.BLUE, True)
            try:
                __import__(baseimport + "." + file)
                console.writeSuccess()
            except Exception as e:
                console.writeFailure()
                console.error(traceback.format_exc())

def bytesToMd5(Bytes:bytes):
    result = hashlib.md5(Bytes)
    return result.hexdigest()


def SideLoops():
    while True:
        Context.mysql.ping()
        time.sleep(30)

def GetCaptcha():
    captchastring = randomString(5)
    captchatoken = randomString(32)
    found = False
    while not found:
        if captchatoken in [s["token"] for s in Context.Captchas]:
            captchatoken = randomString(32)
        else:
            found = True
    image = ImageCaptcha(width = 280, height = 90)
    data = image.generate(captchastring, "bmp").read()
    return {
        "token": captchatoken,
        "string": captchastring,
    }, data
    
def zipfolder(target, folder):
    if os.path.exists(target):
        os.remove(target)
    zipobj = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(folder) + 1
    for base, dirs, files in os.walk(folder):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])