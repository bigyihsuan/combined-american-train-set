import dataclasses
import grf
import json

from enums import TenderSpriteLocation
from vehicle import Vehicle
import util

TENDER_ID_OFFSET = 1000

# def makeAnimation(vehicle: Vehicle, realSprites: list[grf.FileSprite], frameCount: int) -> grf.Switch:
#     assert len(realSprites) > 0
#     chunked = util.chunk(realSprites, 8)
#     return grf.Switch(
#         code=f"motion_counter % {frameCount}",
#         ranges={i: chunked for i in range(frameCount)},
#         default=realSprites[0]
#     )


def main():
    catsGrf = grf.NewGRF(
        grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
        name="Combined American Train Set",
        description="An American train set for the modern age.",
        id_map_file="id_map.json"
    )

    Train: type[grf.Train] = catsGrf.bind(grf.Train)
    VehicleSpriteTable: type[grf.VehicleSpriteTable] = catsGrf.bind(grf.VehicleSpriteTable)
    Switch: type[grf.Switch] = catsGrf.bind(grf.Switch)

    # initGroups()

    # this is here up top to remove vanilla trains
    catsGrf.add(grf.DisableDefault(grf.TRAIN))
    # fix sprites being cut off in the depot
    catsGrf.add(grf.SetGlobalTrainMiscFlag(grf.GlobalTrainMiscFlag.DEPOT_FULL_TRAIN_WIDTH))

    with open("./props/cargo-table.json", "r") as cargoTableFile:
        catsGrf.set_cargo_table(json.load(cargoTableFile))

    # with open("./props/simple-vehicle-stats.json", "r") as vehicleFile:
    with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
        vehicles: list[Vehicle] = [Vehicle(**e) for e in json.load(vehicleFile)]
        for i in range(14):
            vehicle = vehicles[i]

            for g in vehicle.graphics.gs:
                spriteTable = VehicleSpriteTable(grf.TRAIN)
                sg = vehicle.graphics.spriteGroups[g.group]
                purchaseLayout = spriteTable.get_layout(spriteTable.add_purchase_graphics(
                    vehicle.graphics.purchaseSprite.realSprites[0].asGrfFileSprite()))
                if g.tender == TenderSpriteLocation.Same:
                    engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[:-8]]
                    engineFrames = util.chunk(engineRealSprites, 8)
                    assert len(engineFrames) == g.frames

                    engineLayouts = []
                    for frame in engineFrames:
                        engineLayouts.append(spriteTable.get_layout(spriteTable.add_row(frame)))

                    engineGraphics = grf.Switch(
                        code=f"motion_counter % {g.frames}",
                        ranges={i: row for i, row in enumerate(engineLayouts)},
                        default=engineLayouts[0]
                    )

                    # last set of 8 sprites is the tender
                    tenderRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[-8:]]
                    tenderGraphics = spriteTable.get_layout(spriteTable.add_row(tenderRealSprites))

                    train = Train(
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
                            "graphics": grf.GraphicsCallback(engineGraphics, purchaseLayout)
                        }
                    ).add_articulated_part(
                        id=vehicle.id+TENDER_ID_OFFSET,
                        skip_props_check=True,
                        weight=Train.ton(vehicle.props.weight_low),
                        length=g.tenderLength if g.tenderLength >= 8 else None,
                        shorten_by=8-g.tenderLength if g.tenderLength < 8 else None,
                        callbacks={
                            "graphics": grf.GraphicsCallback(tenderGraphics)
                        },
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

    grf.main(catsGrf, "dist/cats.grf")


if __name__ == "__main__":
    main()
