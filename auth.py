from dotenv import load_dotenv
import requests
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove, environ


def refreshToken():
    load_dotenv()
    if environ["AUTH_TOKEN"] == "":
        getNewToken()
        return
    url = "https://osu.ppy.sh/oauth/token"
    payload = {
        "client_id": environ['CLIENT_ID'],
        "client_secret": environ['CLIENT_SECRET'],
        "grant_type": "refresh_token",
        "scope": "public",
        "refresh_token": environ['AUTH_TOKEN']
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, data=payload, headers=headers).json()
    if res.get("refresh_token") != None:
        updateAuthToken(res["refresh_token"])


def getNewToken():
    load_dotenv()
    url = "https://osu.ppy.sh/oauth/token"
    payload = {
        "client_id": environ['CLIENT_ID'],
        "client_secret": environ['CLIENT_SECRET'],
        "grant_type": "client_credentials",
        "scope": "public"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, data=payload, headers=headers).json()
    updateAuthToken(res["access_token"])


def updateAuthToken(token):
    newfd, newPath = mkstemp()
    with fdopen(newfd, 'w') as newFile:
        with open(".env") as curFile:
            for line in curFile:
                if "AUTH_TOKEN" in line:
                    newFile.write(f"AUTH_TOKEN={token}")
                else:
                    newFile.write(line)

    copymode(".env", newPath)
    remove(".env")
    move(newPath, ".env")
