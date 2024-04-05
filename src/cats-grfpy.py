import dataclasses
import grf
import json

from enums import TenderSpriteLocation
from vehicle import Vehicle
import util

# initGroups()

g = grf.NewGRF(
    grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="id_map.json"
)

Train: type[grf.Train] = g.bind(grf.Train)
VehicleSpriteTable: type[grf.VehicleSpriteTable] = g.bind(grf.VehicleSpriteTable)
Switch: type[grf.Switch] = g.bind(grf.Switch)

# this is here up top to remove vanilla trains
g.add(grf.DisableDefault(grf.TRAIN))
# fix sprites being cut off in the depot
g.add(grf.SetGlobalTrainMiscFlag(grf.GlobalTrainMiscFlag.DEPOT_FULL_TRAIN_WIDTH))

with open("./props/cargo-table.json", "r") as cargoTableFile:
    g.set_cargo_table(json.load(cargoTableFile))

# with open("./props/simple-vehicle-stats.json", "r") as vehicleFile:
with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
    vehicles: list[Vehicle] = [Vehicle(**e) for e in json.load(vehicleFile)]
    assert all(isinstance(vehicle, Vehicle) for vehicle in vehicles)

    vehicle = vehicles[0]
    tenderIndex = -1
    spriteTable = VehicleSpriteTable(grf.TRAIN)
    for row in vehicle.graphics.spriteGroups:
        realSprites = [
            grf.FileSprite(
                grf.ImageFile(rs.file),
                rs.x, rs.y, rs.width, rs.height, xofs=rs.xofs, yofs=rs.yofs, zoom=rs.zoom)
            for rs in row.realSprites]
        chunked = util.chunk(realSprites, 8)
        for _ in range(row.g.frames):
            s = next(chunked)
            spriteTable.add_row(s)
        if row.g.tender == TenderSpriteLocation.Same:
            tenderIndex = spriteTable.add_row(next(chunked))
    layout = spriteTable.get_layout(0)
    tenderLayout = spriteTable.get_layout(tenderIndex)
    purchaseLayout = spriteTable.get_layout(spriteTable.add_purchase_graphics([grf.FileSprite(
        grf.ImageFile(rs.file),
        rs.x, rs.y, rs.width, rs.height,
        xofs=rs.xofs, yofs=rs.yofs, zoom=rs.zoom)
        for rs in vehicle.graphics.purchaseSprite.realSprites][0]))

    norris = Train(
        id=vehicle.id,
        name="CATS " + vehicle.name,
        max_speed=Train.kmhish(vehicle.props.max_speed),
        weight=Train.ton(vehicle.props.weight_low),
        introduction_date=grf.datetime.date(*vehicle.props.introduction_date),
        **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
            "introduction_date",
            "max_speed",
            "length" if vehicle.props.shorten_by is not None else "shorten_by"
        ]},
        callbacks={
            "graphics": grf.GraphicsCallback(layout, purchaseLayout)
        }
    ).add_articulated_part(
        id=vehicle.id+1000,
        callbacks={
            "graphics": grf.GraphicsCallback(tenderLayout)
        },
        skip_props_check=True,
        weight=Train.ton(vehicle.props.weight_low),
        length=vehicle.graphics.spriteGroups[0].g.tenderLength
    )

    # for vehicle in vehicles:
    #     gr: Any = vehicle.graphics
    #     vehicle.graphics = VehicleGraphics(**gr)
    #     p: Any = vehicle.props
    #     vehicle.props = VehicleProps(**p)
    #     spriteInfos = vehicle.graphics.sprites
    #     sprites = []
    #     for glr in spriteInfos:
    #         sg: Any = glr
    #         glr = SpriteGroup(**sg)
    #         rs: list[Any] = glr.realSprites
    #         glr.realSprites = [Sprite(**r) for r in rs]
    #         groupName = glr.group
    #         image = grf.ImageFile(f"./res/{groupName}.png")
    #         sprites.extend([grf.FileSprite(
    #             image,
    #             rs.x,
    #             rs.y,
    #             rs.width,
    #             rs.height,
    #             xofs=rs.xofs,
    #             yofs=rs.yofs,
    #             zoom=rs.zoom
    #         ) for rs in glr.realSprites])

    #     engineLayouts, tenderLayouts = [], []
    #     spriteTable = SpriteTable(grf.TRAIN)
    #     for i, row in enumerate(util.chunk(sprites, 8)):
    #         spriteTable.add_row(row)

    #     train = Train(
    #         id=vehicle.id,
    #         name="CATS " + vehicle.name,
    #         max_speed=Train.kmhish(vehicle.props.max_speed),
    #         weight=Train.ton(vehicle.props.weight_low),
    #         liveries=[{"name": "Default", "sprites": sprites}],
    #         introduction_date=grf.datetime.date(*vehicle.props.introduction_date),
    #         **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
    #             "introduction_date",
    #             "max_speed",
    #             "length" if vehicle.props.shorten_by is not None else "shorten_by"
    #         ]})


grf.main(g, "dist/cats.grf")
