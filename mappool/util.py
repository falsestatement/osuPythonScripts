import requests
from dotenv import load_dotenv
from os import environ
import json


def getBeatmapInfo(beatmapId, mods=[]):
    load_dotenv("../.env")
    info = dict()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + environ["AUTH_TOKEN"]
    }
    payload = {
        "mods": mods,
        "ruleset": "osu"
    }
    infoRes = requests.get(
        environ["BASE_URL"] + f"/beatmaps/{beatmapId}", headers=headers).json()
    attributeRes = requests.post(
        environ["BASE_URL"] + f"/beatmaps/{beatmapId}/attributes", headers=headers, json=payload).json()["attributes"]

    hpMod = 1
    csMod = 1
    bpmMod = 1
    if "HR" in mods:
        hpMod *= 1.4
        csMod *= 1.3
    if "EZ" in mods:
        hpMod *= 0.5
        csMod *= 0.5
    if "DT" in mods:
        bpmMod *= 1.5
    if "HT" in mods:
        bpmMod *= 0.5

    info["id"] = infoRes["id"]
    info["mapset_id"] = infoRes["beatmapset"]["id"]
    info["cover_url"] = infoRes["beatmapset"]["covers"]["cover"]
    info["artist"] = infoRes["beatmapset"]["artist"]
    info["title"] = infoRes["beatmapset"]["title"]
    info["diff_name"] = infoRes["version"]
    info["star_rating"] = attributeRes["star_rating"]
    info["ar"] = attributeRes["approach_rate"]
    info["od"] = round(attributeRes["overall_difficulty"], 1)
    info["hp"] = round(min(infoRes["drain"] * hpMod, 10), 1)
    info["cs"] = round(min(infoRes["cs"] * csMod, 10), 1)
    info["bpm"] = round(infoRes["bpm"] * bpmMod, 1)

    print(json.dumps(info, indent=2))
