import dataclasses
from pprint import pprint
import grf
import json

from enums import Loc, TenderSpriteLocation
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

    IGNORE_FOR_NOW = [20]  # TODO

    with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
        vehicles: list[V.Vehicle] = [V.Vehicle(**e) for e in json.load(vehicleFile)]
        for vehicle in vehicles[:max(IGNORE_FOR_NOW)+1]:
            if vehicle.id in IGNORE_FOR_NOW:
                print(f"SKIPPING {vehicle.name}...")
                continue
            makeEngine(vehicle)

    grf.main(catsGrf, "dist/cats.grf")


def makeEngine(vehicle: V.Vehicle):
    if vehicle.id in [14, 17]:  # mallet, challenger
        # makeArticulatedSteamEngine(vehicle)
        return

    print(f"Making {vehicle.name}...", end=" ")

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

    # get the engine and tender graphics
    forwardEngine = None
    forwardTender = None
    backwardEngine = None
    backwardTender = None
    tenderIndex = -1
    for i, g in enumerate(vehicle.graphics.gs):
        if isinstance(g, G.Purchase):
            raise Exception(f"Somehow got a Purchase in vehicle.gs at {i} for {vehicle.name}!")
        if isinstance(g, G.Tender) and tenderIndex != -1:
            continue

        sg = vehicle.graphics.spriteGroups[g.group]

        tenderGraphics = None
        tenderGraphicsLocation = []
        engineRealSprites = []
        if not isinstance(g, G.Tender) and g.tender == TenderSpriteLocation.Same:
            print("Tender is on same spritesheet...", end=" ")
            # if the tender is on the same spritesheet,
            # last set of 8 sprites is the tender
            # get the real sprites for the engine.
            engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites[:g.frames * 8]]
            tenderGraphicsLocation = sg.realSprites[g.frames * 8:]
        elif not isinstance(g, G.Tender) and g.tender == TenderSpriteLocation.Separate:
            print("Tender is on separate spritesheet...", end=" ")
            # if the tender is on a different spritesheet,
            # current g is not a tender, i.e. a loco, and has its tender on a separate sprite
            engineRealSprites = [s.asGrfFileSprite() for s in sg.realSprites]
            # find the tender group
            tenderIndex, tender = vehicle.getTender()
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

    mainUnitGraphics = None
    articulatedGraphics = None

    # if the current sprite group is for the reversed version...
    if reversedIndex != -1:
        # handle engines that reverse direction when reversed

        # when reversed, the tender is "locomotive"/leading unit, no animations
        # when reversed, the engine is the following articulated unit, with animations
        # switch on vehicle_is_reversed to change the graphics

        mainUnitGraphics = grf.Switch(
            code="vehicle_is_reversed",
            ranges={
                0: forwardEngine,
                1: backwardTender,
            },
            default=forwardEngine,
            # also check the other cars of the consist. vehicle_is_reversed by default only checks the first car.
            related_scope=True
        )
        articulatedGraphics = grf.Switch(
            code="vehicle_is_reversed",
            ranges={
                0: forwardTender,
                1: backwardEngine,
            },
            default=forwardTender,
            related_scope=True
        )
    else:
        mainUnitGraphics = forwardEngine
        articulatedGraphics = forwardTender

    train = Train(
        id=vehicle.id,
        name="CATS " + vehicle.name,
        max_speed=Train.kmhish(vehicle.props.max_speed),
        weight=Train.ton(vehicle.props.weight_low),
        introduction_date=grf.datetime.date(year=vehicle.props.introduction_date[0], month=1, day=1),
        **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
            "introduction_date",
            "introduction_days_since_1920",
            "max_speed",
        ]},
        callbacks={
            "graphics": grf.GraphicsCallback(mainUnitGraphics, purchaseLayout)
        }
    )
    if articulatedGraphics is not None:
        train.add_articulated_part(
            id=vehicle.id+TENDER_ID_OFFSET,
            skip_props_check=True,
            length=vehicle.graphics.gs[0].tenderLength,
            callbacks={
                "graphics": grf.GraphicsCallback(articulatedGraphics)
            },
        )

    print("Done!", end="\n")


def makeArticulatedSteamEngine(vehicle: V.Vehicle):
    print(f"Making {vehicle.name}...", end=" ")

    # make a new spritetable for this vehicle
    spriteTable = VehicleSpriteTable(grf.TRAIN)
    # add purchase sprite
    purchaseLayout = spriteTable.get_layout(
        spriteTable.add_purchase_graphics(
            vehicle.graphics.purchaseSprite.realSprites[0].asGrfFileSprite()
        )
    )

    # TODO: add support for articulateds with 3+ parts (e.g. malllet = fixed frame, front articulated, tender)
    # TODO: NARS seems to use curv_info_cur_next, so switch over that.
    # TODO: per https://newgrf-specs.tt-wiki.net/wiki/NML:Vehicles#:~:text=is%2045%20degrees.-,curv_info_cur_next,-%2D2%20...%202
    # TODO: the range is from -2 to 2, inclusive. each unit is a 45 deg turn, so it ranges from 90 deg left (-2) to 90 deg right (+2).
    # TODO: NARS articulateds sprites have structure
    # TODO:     fixed -> articulated straight -> articulated left -> articulated right -> tender.
    # TODO: fixed and tender would use existing code for any other engine.
    # TODO: articulated would need 3 makings.
    # TODO: NARS only uses 1 and 15 (-1?) and defaults to straight.

    frontArticulatedStraight = None
    frontArticulatedLeft = None
    frontArticulatedRight = None
    fixedUnit = None
    tender = None
    tenderLength = 8

    for g in vehicle.graphics.gs:
        sg = vehicle.graphics.spriteGroups[g.group]

        # tender is always separate
        if isinstance(g, G.Tender):
            print("Tender is on separate spritesheet...", end=" ")
            _, tenderGroup = vehicle.getTender()
            tenderGraphicsLocation = vehicle.graphics.spriteGroups[tenderGroup.group].realSprites
            tenderRealSprites = [s.asGrfFileSprite() for s in tenderGraphicsLocation]
            assert len(tenderRealSprites) > 0
            # tender has no animations, so no switch for animations
            tender = spriteTable.get_layout(spriteTable.add_row(tenderRealSprites))
            tenderLength = tenderGroup.tenderLength
            continue

        # same process for each part of the engine
        realSprites = [s.asGrfFileSprite() for s in sg.realSprites]
        assert len(realSprites) > 0
        engineFrames = util.chunk(realSprites, 8)
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
        match g.loc:
            case Loc.Back:
                fixedUnit = engineGraphics
            case Loc.FrontStraight:
                frontArticulatedStraight = engineGraphics
            case Loc.FrontLeft:
                frontArticulatedLeft = engineGraphics
            case Loc.FrontRight:
                frontArticulatedRight = engineGraphics

    assert frontArticulatedStraight is not None
    assert frontArticulatedLeft is not None
    assert frontArticulatedRight is not None
    assert fixedUnit is not None
    assert tender is not None

    # all parts gotten, now to make the engine
    articulatedTurnSwitch = grf.Switch(
        code="curv_info_cur_next",  # cur is the front articulated, next is the fixed unit
        ranges={
            -1: frontArticulatedLeft,
            +1: frontArticulatedRight,
        },
        default=frontArticulatedStraight,
        related_scope=True,
    )

    fixedLength = {
        14: 4,
        17: 4,
    }

    train = Train(
        id=vehicle.id,
        name="CATS " + vehicle.name,
        max_speed=Train.kmhish(vehicle.props.max_speed),
        weight=Train.ton(vehicle.props.weight_low),
        introduction_date=grf.datetime.date(year=vehicle.props.introduction_date[0], month=1, day=1),
        length=4,
        **{k: v for k, v in dataclasses.asdict(vehicle.props).items() if k not in [
            "introduction_date",
            "introduction_days_since_1920",
            "max_speed",
            "length"
        ]},
        callbacks={
            "graphics": grf.GraphicsCallback(articulatedTurnSwitch, purchaseLayout)
        }
    ).add_articulated_part(
        id=vehicle.id+(2*TENDER_ID_OFFSET),
        skip_props_check=True,
        # length=fixedLength[vehicle.id],
        length=6,
        callbacks={
            "graphics": grf.GraphicsCallback(fixedUnit)
        },
    ).add_articulated_part(
        id=vehicle.id+TENDER_ID_OFFSET,
        skip_props_check=True,
        length=tenderLength,
        callbacks={
            "graphics": grf.GraphicsCallback(tender)
        },
    )

    print("Done!", end="\n")


if __name__ == "__main__":
    main()
