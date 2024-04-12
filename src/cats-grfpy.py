import dataclasses
from pprint import pprint
import grf
import json

from enums import TenderSpriteLocation
import group as G
import vehicle as V
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

catsGrf = grf.NewGRF(
    grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="id_map.json"
)

Train: type[grf.Train] = catsGrf.bind(grf.Train)
VehicleSpriteTable: type[grf.VehicleSpriteTable] = catsGrf.bind(grf.VehicleSpriteTable)
Switch: type[grf.Switch] = catsGrf.bind(grf.Switch)


def main():

    global catsGrf, Train, VehicleSpriteTable, Switch

    # initGroups()

    # this is here up top to remove vanilla trains
    catsGrf.add(grf.DisableDefault(grf.TRAIN))
    # fix sprites being cut off in the depot
    catsGrf.add(grf.SetGlobalTrainMiscFlag(grf.GlobalTrainMiscFlag.DEPOT_FULL_TRAIN_WIDTH))
    # fix sprites being too high in depot
    catsGrf.add(grf.SetGlobalTrainDepotYOffset(2))

    with open("./props/cargo-table.json", "r") as cargoTableFile:
        catsGrf.set_cargo_table(json.load(cargoTableFile))

    # with open("./props/simple-vehicle-stats.json", "r") as vehicleFile:
    with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
        vehicles: list[V.Vehicle] = [V.Vehicle(**e) for e in json.load(vehicleFile)]
        for vehicle in vehicles[:14]:
            print(f"Making {vehicle.name}...", end="")

            tenderLocation = [
                isinstance(graphic, G.Tender) or graphic.tender == TenderSpriteLocation.Same
                for graphic in vehicle.graphics.gs].index(True)

            spriteTable = VehicleSpriteTable(grf.TRAIN)
            purchaseLayout = spriteTable.get_layout(spriteTable.add_purchase_graphics(
                vehicle.graphics.purchaseSprite.realSprites[0].asGrfFileSprite()))
            makeEngine(vehicle, spriteTable, purchaseLayout)
            print(" Done!")

    grf.main(catsGrf, "dist/cats.grf")


def makeEngine(
        vehicle: V.Vehicle,
        spriteTable: grf.VehicleSpriteTable,
        purchaseLayout: grf.GenericSpriteLayout):
    # get the index of the reversed spritesheet
    reversedIndex = -1
    for i, g in enumerate(vehicle.graphics.gs):
        if g.reversable:
            reversedIndex = i

    # make a new spritetable for this vehicle
    spriteTable = VehicleSpriteTable(grf.TRAIN)
    # add purchase sprite
    purchaseLayout = spriteTable.get_layout(
        spriteTable.add_purchase_graphics(
            vehicle.graphics.purchaseSprite.realSprites[0].asGrfFileSprite()
        )
    )

    forwardEngine = None
    forwardTender = None
    backwardEngine = None
    backwardTender = None

    for i, g in enumerate(vehicle.graphics.gs):
        sg = vehicle.graphics.spriteGroups[g.group]

        # all but the last 8 sprites are the tender
        engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[:-8]]
        # chunk into rows of 8 sprites, 1 per frame of animation
        engineFrames = util.chunk(engineRealSprites, 8)
        assert len(engineFrames) == g.frames
        # make the layouts for each engine frame
        engineLayouts = []
        for frame in engineFrames:
            engineLayouts.append(spriteTable.get_layout(spriteTable.add_row(frame)))
        # switch over motion_counter mod framecount to make animations
        engineGraphics = grf.Switch(
            code=f"motion_counter % {g.frames}",
            ranges={i: row for i, row in enumerate(engineLayouts)},
            default=engineLayouts[0]
        )

        if i != reversedIndex:
            forwardEngine = engineGraphics
        else:
            backwardEngine = engineGraphics

        # TODO: handle engines that reverse direction when reversed
        # TODO: if has a tender, tender should be first. otherwise use the other set of sprites
        # TODO: use vehicle_is_reversed variable in a switch

        # if the tender is on the same spritesheet...
        if g.tender == TenderSpriteLocation.Same:
            # last set of 8 sprites is the tender, no animations
            tenderRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[-8:]]
            tenderGraphics = spriteTable.get_layout(spriteTable.add_row(tenderRealSprites))
            if i != reversedIndex:
                forwardTender = tenderGraphics
            else:
                backwardTender = tenderGraphics
        # elif g.tender == TenderSpriteLocation.Separate:
        #     makeEngineWithTenderSeparately(vehicle, spriteTable, sg, g, purchaseLayout)

    # if the current sprite group is for the reversed version...
    if reversedIndex != -1:
        # the tender is "locomotive"/leading unit, no animations
        # engine is the following articulated unit, with animations
        # change the two to use switches
        frontUnitGraphics = grf.Switch(
            code="vehicle_is_reversed",
            ranges={
                0: forwardEngine,
                1: backwardTender,
            },
            default=forwardEngine,
            related_scope=True
        )
        backUnitGraphics = grf.Switch(
            code="vehicle_is_reversed",
            ranges={
                0: forwardTender,
                1: backwardEngine,
            },
            default=forwardTender,
            related_scope=True
        )
    else:
        frontUnitGraphics = forwardEngine
        backUnitGraphics = forwardTender

    print(vehicle.name, type(frontUnitGraphics), type(backUnitGraphics))

    train = Train(
        id=vehicle.id,
        name="CATS " + vehicle.name,
        max_speed=Train.kmhish(vehicle.props.max_speed),
        weight=Train.ton(vehicle.props.weight_low),
        introduction_date=grf.datetime.date(*vehicle.props.introduction_date),
        **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
            "introduction_date",
            "max_speed",
        ]},
        callbacks={
            "graphics": grf.GraphicsCallback(frontUnitGraphics, purchaseLayout)
        }
    )
    if backUnitGraphics is not None:
        train.add_articulated_part(
            id=vehicle.id+TENDER_ID_OFFSET,
            skip_props_check=True,
            weight=Train.ton(vehicle.props.weight_low),
            length=vehicle.graphics.gs[0].tenderLength,
            callbacks={
                "graphics": grf.GraphicsCallback(backUnitGraphics)
            },
        )


if __name__ == "__main__":
    main()
