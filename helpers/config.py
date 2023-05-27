import os
import configparser

class configManager:
    """
    config.ini object

    config -- list with ini data
    default -- if true, we have generated a default config.ini
    """

    config = configparser.ConfigParser()
    extra = {}
    fileName = ""        # config filename
    default = True

    # Check if config.ini exists and load/generate it
    def __init__(self, filename):
        """
        Initialize a config object
        """

        self.fileName = filename
        if os.path.isfile(self.fileName):
            # config.ini found, load it
            self.config.read(self.fileName)
            self.default = False
        else:
            # config.ini not found, generate a default one
            self.CreateConfig()
            self.default = True

    # Check if config.ini has all needed the keys
    def isValid(self):
        """
        Check if this config has the required keys

        return -- True if valid, False if not
        """

        try:
            # Try to get all the required keys
            self.config.get("db", "host")
            self.config.get("db", "username")
            self.config.get("db", "password")
            self.config.get("db", "database")
            self.config.get("db", "workers")

            self.config.get("server", "port")
            self.config.get("server", "debug")
            return True
        except:
            return False


    # Generate a default config.ini
    def CreateConfig(self):
        """Open and set default keys for that config file"""

        # Open config.ini in write mode
        f = open(self.fileName, "w")

        # Set keys to config object
        self.config.add_section("db")
        self.config.set("db", "host", "127.0.0.1")
        self.config.set("db", "username", "root")
        self.config.set("db", "password", "")
        self.config.set("db", "database", "Airmod")
        self.config.set("db", "workers", "16")

        self.config.add_section("server")
        self.config.set("server", "port", "10300")
        self.config.set("server", "debug", "False")

        # Write ini to file and close
        self.config.write(f)
        f.close()
