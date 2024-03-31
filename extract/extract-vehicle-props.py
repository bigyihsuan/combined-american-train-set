import json
import grf

import grffile


def main():
    nars = grffile.GRFFile("../decompiled/newnars.grf")
    with open("./vehicle-stats.json", "w") as vehicleStatsJson:
        rows = [train.flatten() for train in nars.trains.values()]
        rows.sort(key=lambda row: row["id"])
        json.dump(rows, vehicleStatsJson, sort_keys=True, default=str, indent=4)

    with open("./sprites.json", "w") as spritesJson:
        json.dump(nars.sprites, spritesJson, indent=4)


if __name__ == "__main__":
    main()
