import dataclasses
from typing import Any
import grf
import json

from extract.vehicle import Sprite, SpriteGroup, Vehicle, VehicleGraphics, VehicleProps

g = grf.NewGRF(
    grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="id_map.json"
)

Train = g.bind(grf.Train)

# this is here up top to remove vanilla trains
g.add(grf.DisableDefault(grf.TRAIN))

with open("./props/cargo-table.json", "r") as cargoTableFile:
    g.set_cargo_table(json.load(cargoTableFile))

# with open("./props/simple-vehicle-stats.json", "r") as vehicleFile:
with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
    vehicles: list[Vehicle] = [Vehicle(**e) for e in json.load(vehicleFile)]
    assert all(isinstance(vehicle, Vehicle) for vehicle in vehicles)

    for vehicle in vehicles:
        gr: Any = vehicle.graphics
        vehicle.graphics = VehicleGraphics(**gr)
        p: Any = vehicle.props
        vehicle.props = VehicleProps(**p)
        spriteInfos = vehicle.graphics.sprites
        sprites = []
        for glr in spriteInfos:
            sg: Any = glr
            glr = SpriteGroup(**sg)
            rs: list[Any] = glr.realSprites
            glr.realSprites = [Sprite(**r) for r in rs]
            groupName = glr.group
            image = grf.ImageFile(f"./res/{groupName}.png")
            sprites.extend([grf.FileSprite(
                image,
                rs.x,
                rs.y,
                rs.width,
                rs.height,
                xofs=rs.xofs,
                yofs=rs.yofs,
                zoom=rs.zoom
            ) for rs in glr.realSprites])

        train = Train(
            id=vehicle.id,
            name="CATS " + vehicle.name,
            max_speed=Train.kmhish(vehicle.props.max_speed),
            weight=Train.ton(vehicle.props.weight_low),
            liveries=[{"name": "Default", "sprites": sprites}],
            introduction_date=grf.datetime.date(*vehicle.props.introduction_date),
            **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
                "introduction_date",
                "max_speed",
                "length" if vehicle.props.shorten_by is not None else "shorten_by"
            ]})


grf.main(g, "dist/cats.grf")
