import dataclasses
import json

from group import ID_TO_GROUPS, Car, Loco, Purchase, Tender
from vehicle import Vehicle, SpriteGroup
from enums import Loc
import grffile


def extractProps():
    nars = grffile.GRFFile("./decompiled/newnars.grf")
    trains = [train for train in nars.trains.values()]
    trains.sort(key=lambda row: row.id)

    with open("./props/cargo-table.json", "w") as cargoTableJson:
        json.dump(nars.cargo_table, cargoTableJson)

    with open("./props/vehicle-stats.json", "w") as vehicleStatsJson:
        rowsDict = [dataclasses.asdict(train) for train in trains]
        json.dump(rowsDict, vehicleStatsJson, indent=4, default=str)

    with open("./props/sprites.json", "w") as spritesJson:
        s = [dataclasses.asdict(e) for e in nars.sprites]
        json.dump(s, spritesJson, indent=4, default=str)

    with open("./props/vehicle-stats-sprites.json", "w") as vehicleStatsSpritesJson:  # \
        # open("./props/simple-vehicle-stats.json", "w") as simpleVehicleStatsJson:

        statsDict: dict[int, Vehicle] = {train.id: train for train in trains}
        spriteGroups: dict[str, SpriteGroup] = {sprite.group: sprite for sprite in nars.sprites}
        # simpleStatSprites: list[Vehicle] = []

        for id, stat in statsDict.items():
            if id in ID_TO_GROUPS:
                groups = ID_TO_GROUPS[id]
                stat.graphics.gs = [g for g in groups if isinstance(g, (Loco, Tender, Car))]
                for group in groups:
                    spriteGroup: SpriteGroup = spriteGroups[group.group]
                    if isinstance(group, (Loco, Tender, Car)):
                        stat.graphics.spriteGroups[group.group] = spriteGroup
                    elif isinstance(group, Purchase):
                        stat.graphics.purchaseSprite = spriteGroup

        # for spriteGroup in spriteGroups:
        #     groupName = spriteGroup.group
        #     if groupName in GROUP_TO_ID:
        #         e = GROUP_TO_ID[groupName]
        #         if e.id == -1:
        #             continue  # skip groups that are not vehicles
        #         if spriteGroup.loc == Loc.Unset:
        #             spriteGroup.loc = e.loc

        #         stat: Vehicle = statsDict[e.id]
        #         if e.isPurchaseSprite:
        #             stat.graphics.purchaseSprite = spriteGroup
        #         elif e.id == stat.id:
        #             stat.graphics.sprites.append(spriteGroup)

        #         # also set length
        #         if e.length != 8:
        #             stat.props.length = e.length
        #             if stat.props.shorten_by == 0:
        #                 stat.props.shorten_by = None

        #         outputStats.append(stat)

        #         #! temp filter for "simple" vehicles
        #         #! currently, anything that has exactly 8 sprites, and no purchase sprites
        #         # if groupName in simpleVehicles() and len(spriteGroup.realSprites) == 8:
        #         #     simpleStatSprites.append(stat)

        stasSpritesDict = [dataclasses.asdict(stat) for stat in statsDict.values()]
        json.dump(stasSpritesDict, vehicleStatsSpritesJson, default=str, indent=4)

        # # simpleStatSpritesDict = [dataclasses.asdict(stat) for stat in simpleStatSprites]
        # # json.dump(simpleStatSpritesDict, simpleVehicleStatsJson, default=str, indent=4)


if __name__ == "__main__":
    extractProps()
