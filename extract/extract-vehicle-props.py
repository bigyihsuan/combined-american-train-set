import json
from typing import Any
import grf

import grffile
from group import GROUP_TO_ID, simpleVehicles

import numpy as np


def main():
    nars = grffile.GRFFile("../decompiled/newnars.grf")
    with open("./cargo-table.json", "w") as cargoTableJson:
        json.dump(nars.cargo_table, cargoTableJson)

    with open("./vehicle-stats.json", "w") as vehicleStatsJson:
        rows = [train.flatten() for train in nars.trains.values()]
        rows.sort(key=lambda row: row["id"])
        json.dump(rows, vehicleStatsJson, sort_keys=False, default=str, indent=4)

    with open("./sprites.json", "w") as spritesJson:
        json.dump(nars.sprites, spritesJson, indent=4)

    with open("./vehicle-stats.json", "r") as vehicleStatsJson, open("./sprites.json", "r") as spritesJson, open("./vehicle-stats-sprites.json", "w") as vehicleStatsSpritesJson, open("./simple-vehicle-stats.json", "w") as simpleVehicleStatsJson:
        stats: list[dict[str, Any]] = json.load(vehicleStatsJson)
        sprites: list[dict[str, Any]] = json.load(spritesJson)
        statsSprites = {stat["id"]: stat for stat in stats}
        simpleStatSprites = []

        group: dict[str, Any]
        for group in sprites:
            groupName = group["group"]
            if groupName in GROUP_TO_ID:
                e = GROUP_TO_ID[groupName]
                if e.id == -1:
                    continue  # skip groups that are not vehicles
                stat = statsSprites[e.id]
                if "graphics" not in stat:
                    stat["graphics"] = {
                        "purchaseSprite": {},
                        "sprites": []
                    }

                if e.isPurchaseSprite:
                    stat["graphics"]["purchaseSprite"] = {groupName: group["sprites"]}
                else:
                    stat["graphics"]["sprites"].append({
                        "group": groupName,
                        "loc": e.loc,
                        "realSprites": group["sprites"]
                    })
                statsSprites[e.id] = stat

                if groupName in simpleVehicles() and len(group["sprites"]) == 8:
                    simpleStatSprites.append(stat)

        statsSprites = [stat for stat in statsSprites.values()]
        json.dump(statsSprites, vehicleStatsSpritesJson, sort_keys=False, default=str, indent=4)
        json.dump(simpleStatSprites, simpleVehicleStatsJson, sort_keys=False, default=str, indent=4)


if __name__ == "__main__":
    main()
