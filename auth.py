from dotenv import load_dotenv
import requests
import os


def refreshToken():
    load_dotenv()
    if os.environ["AUTH_TOKEN"] == "":
        print("hi")


def getNewToken():
    load_dotenv()
