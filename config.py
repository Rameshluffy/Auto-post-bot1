from os import environ


class Config:
    API_ID = int(environ.get("API_ID", 25773993))
    API_HASH = environ.get("API_HASH", "9176f5b87d53fc4f668e84c4cb477ac8")
    BOT_TOKEN = environ.get("BOT_TOKEN", "6157402161:AAHjE9S3icWRLh4jwBdHY9AfxrsrYzExnNs")
    BOT_SESSION = environ.get("BOT_SESSION", "fjdfjfd")
    DATABASE_URI = environ.get("DATABASE_URI","mongodb://localhost:27017",)
    DATABASE_NAME = environ.get("DATABASE_NAME", "cluster12")
    BOT_OWNER_ID = [int(id) for id in environ.get("BOT_OWNER_ID", "1832810840").split()]
    START_PIC = environ.get("START_PIC", "https://graph.org/file/c3c11dbbef4523ba84183.jpg")


class temp(object):
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
