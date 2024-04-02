import json
from typing import Any
import grf

import grffile
from group import GROUP_TO_ID

import numpy as np


def main():
    nars = grffile.GRFFile("../decompiled/newnars.grf")
    with open("./vehicle-stats.json", "w") as vehicleStatsJson:
        rows = [train.flatten() for train in nars.trains.values()]
        rows.sort(key=lambda row: row["id"])
        json.dump(rows, vehicleStatsJson, sort_keys=False, default=str, indent=4)

    with open("./sprites.json", "w") as spritesJson:
        json.dump(nars.sprites, spritesJson, indent=4)

    with open("./vehicle-stats.json", "r") as vehicleStatsJson, open("./sprites.json", "r") as spritesJson, open("./vehicle-stats-sprites.json", "w") as vehicleStatsSpritesJson:
        stats: list[dict[str, Any]] = json.load(vehicleStatsJson)
        sprites: list[dict[str, Any]] = json.load(spritesJson)
        statsSprites = {stat["id"]: stat for stat in stats}

        group: dict[str, Any]
        for group in sprites:
            groupName = group["group"]
            if groupName in GROUP_TO_ID:
                e = GROUP_TO_ID[groupName]
                if e.id == -1:
                    continue  # skip groups that are not vehicles
                stat = statsSprites[e.id]
                if "purchaseSprite" not in stat:
                    stat["purchaseSprite"] = {}
                if "sprites" not in stat:
                    stat["sprites"] = []

                if e.isPurchaseSprite:
                    stat["purchaseSprite"] = {groupName: group["sprites"]}
                else:
                    stat["sprites"].append({
                        "group": groupName,
                        "loc": e.loc,
                        "realSprites": group["sprites"]
                    })
                statsSprites[e.id] = stat
        statsSprites = [stat for stat in statsSprites.values()]
        json.dump(statsSprites, vehicleStatsSpritesJson, sort_keys=False, default=str, indent=4)


if __name__ == "__main__":
    main()
