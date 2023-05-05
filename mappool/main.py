from auth import refreshToken
from util import getBeatmapInfo
import re

refreshToken()
with open("input.txt") as input:
    pool = list(filter(None, (line.rstrip() for line in input)))

with open("output.txt", "w+") as output:
    modCounter = dict()
    output.write(
        "Mod\tCover\tSong Name\tDifficulty\tStar Rating\tLength\tBPM\tCS\tHP\tAR\tOD\tBeatmap ID\n")
    for beatmap in pool:
        beatmapId = re.findall(r'\d+', beatmap)[-1]
        mod = beatmap[:2].upper()
        if modCounter.get(mod) == None:
            modCounter[mod] = 0
        modCounter[mod] += 1
        mods = []
        if mod != "FM" and mod != "NM" and mod != "TB":
            mods.append(mod)
        info = getBeatmapInfo(beatmapId, mods)

        t = '\t'
        fBanner = f"=IMAGE(\"{info['cover_url']}\")"
        fTitle = f"=HYPERLINK(\"https://osu.ppy.sh/beatmaps/{beatmapId}\", \"{info['artist']} - {info['title']}\")"
        fMod = f"{mod}{modCounter[mod]}"
        print(f"Processed: {fMod}")
        output.write(fMod + t
                     + fBanner + t
                     + fTitle + t
                     + info['diff_name'] + t
                     + str(info['star_rating']) + t
                     + str(info['length']) + t
                     + str(info['bpm']) + t
                     + str(info['cs']) + t + str(info['hp']) + t +
                     str(info['ar']) + t + str(info['od']) + t
                     + beatmapId
                     + '\n')

    print(f"{len(pool)} maps processed, results available in output.txt")
