import datetime
from typing import Any
import grf
import json

import sys

g = grf.NewGRF(
    # grfid=b"\x09\x00\x00\x01",
    grfid=b"BY\x01\x03",
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="id_map.json"
)

Train = g.bind(grf.Train)

g.add(grf.DisableDefault(grf.TRAIN))

with open("./props/cargo-table.json", "r") as cargoTableFile:
    g.set_cargo_table(json.load(cargoTableFile))

with open("./props/simple-vehicle-stats.json", "r") as vehicleFile:
    vehicleProps: list[dict[str, Any]] = json.load(vehicleFile)

    for vehicle in vehicleProps:
        if "sprites" not in vehicle["graphics"]:
            continue
        spriteInfos = vehicle["graphics"]["sprites"]
        sprites = []
        for glr in spriteInfos:
            groupName = glr["group"]
            image = grf.ImageFile(f"./res/{groupName}.png")
            sprites.extend([grf.FileSprite(
                image,
                rs["x"],
                rs["y"],
                rs["width"],
                rs["height"],
                xofs=rs["xofs"],
                yofs=rs["yofs"],
                zoom=rs["zoom"]
            ) for rs in glr["realSprites"]])

        introDate = datetime.datetime.strptime(vehicle["introduction_date"], "%Y-%m-%d").date()
        train = Train(
            id=vehicle["id"],
            name="CATS " + vehicle["name"],
            max_speed=Train.kmhish(vehicle["max_speed"]),
            weight=Train.ton(vehicle["weight_low"]),
            liveries=[{"name": "Default", "sprites": sprites}],
            introduction_date=datetime.date(introDate.year, introDate.month, introDate.day),
            **
            {k: v for k, v in vehicle.items() if k not in [
                "id", "name", "max_speed", "graphics", "introduction_date",
            ]})


grf.main(g, "dist/cats.grf")
