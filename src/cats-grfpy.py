import dataclasses
from pprint import pprint
import grf
import json

from enums import TenderSpriteLocation
import group as G
import vehicle as V
import util

TENDER_ID_OFFSET = 1000

catsGrf = grf.NewGRF(
    grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="./id_map.json",
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

    IGNORE_FOR_NOW = [14, 17, 20]

    with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
        vehicles: list[V.Vehicle] = [V.Vehicle(**e) for e in json.load(vehicleFile)]
        for vehicle in vehicles[:max(IGNORE_FOR_NOW)+1]:
            if vehicle.id in IGNORE_FOR_NOW:
                print(f"SKIPPING {vehicle.name}...")
                continue
            print(f"Making {vehicle.name}...", end="")

            makeEngine(vehicle)

            print(" Done!")

    grf.main(catsGrf, "dist/cats.grf")


def makeEngine(vehicle: V.Vehicle):
    # get the index of the reversed spritesheet
    reversedIndex = l.index(True) if True in (l := list(g.reversable for g in vehicle.graphics.gs)) else -1

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
    tenderIndex = -1
    for i, g in enumerate(vehicle.graphics.gs):
        if isinstance(g, G.Purchase):
            print(f"Somehow got a Purchase in vehicle.gs at {i} for {vehicle.name}!")
            continue
        if isinstance(g, G.Tender) and tenderIndex != -1:
            continue

        sg = vehicle.graphics.spriteGroups[g.group]

        tenderGraphics = None
        tenderGraphicsLocation = []
        engineRealSprites = []
        if not isinstance(g, G.Tender) and g.tender == TenderSpriteLocation.Same:
            # if the tender is on the same spritesheet
            # last set of 8 sprites is the tender
            # get the real sprites for the engine.
            engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[:g.frames * 8]]
            tenderGraphicsLocation = sg.realSprites[g.frames * 8:]
        elif not isinstance(g, G.Tender) and g.tender == TenderSpriteLocation.Separate:
            # current g is not a tender, i.e. a loco, and has its tender on a separate sprite
            engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites]
            # find the tender group
            tenderIndex = list(isinstance(g, G.Tender) for g in vehicle.graphics.gs).index(True)
            t: G.G = vehicle.graphics.gs[tenderIndex]
            assert isinstance(t, G.Tender)
            tender: G.Tender = t
            tenderGraphicsLocation = vehicle.graphics.spriteGroups[tender.group].realSprites

        tenderRealSprites = [s.asGrfFileSprite() for s in tenderGraphicsLocation]
        # tender has no animations, so no switch for animations
        tenderGraphics = spriteTable.get_layout(spriteTable.add_row(tenderRealSprites))

        if i != reversedIndex:
            forwardTender = tenderGraphics
        else:
            backwardTender = tenderGraphics

        # chunk into rows of 8 sprites, 1 per frame of animation
        engineFrames = util.chunk(engineRealSprites, 8)
        assert len(engineFrames) == g.frames
        assert all(len(f) == 8 for f in engineFrames)
        # make the layouts for each engine frame
        engineLayouts = []
        for frame in engineFrames:
            engineLayouts.append(
                spriteTable.get_layout(spriteTable.add_row(frame))
            )
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

    # if the current sprite group is for the reversed version...
    if reversedIndex != -1:
        # handle engines that reverse direction when reversed

        # when reversed, the tender is "locomotive"/leading unit, no animations
        # when reversed, the engine is the following articulated unit, with animations
        # switch on vehicle_is_reversed to change the graphics

        frontUnitGraphics = grf.Switch(
            code="vehicle_is_reversed",
            ranges={
                0: forwardEngine,
                1: backwardTender,
            },
            default=forwardEngine,
            # also check the other cars of the consist. vehicle_is_reversed by default only checks the first car.
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
