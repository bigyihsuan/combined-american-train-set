import dataclasses
import os

import grf
import yaml

import shared.vehicle as vehicle
from make_vehicles import *
from make_vehicles.vehicles.cars import *
from shared.enums import Orientation
from util import animated_vehicle

DEFAULT_PROPS = dataclasses.asdict(vehicle.Props.default())

newgrf: grf.NewGRF
Train: type[grf.Train]
VehicleSpriteTable: type[grf.VehicleSpriteTable]
Switch: type[grf.Switch]


def bind_grf(g: grf.NewGRF):
    global newgrf, Train, VehicleSpriteTable, Switch
    (
        newgrf,
        Train,
        VehicleSpriteTable,
        Switch
    ) = (
        g,
        g.bind(grf.Train),
        g.bind(grf.VehicleSpriteTable),
        g.bind(grf.Switch)
    )


def load_yaml(root: str, name: str) -> tuple[vehicle.Props, vehicle.Graphics]:
    loco_yaml_path = os.path.join(root, f"{name}.yaml")
    loco_graphics_path = os.path.join(root, f"graphics.yaml")

    print(loco_yaml_path, loco_graphics_path)

    loco_props: vehicle.Props
    with open(loco_yaml_path, "r") as loco_yaml_file:
        d = yaml.safe_load(loco_yaml_file)
        loco_props = vehicle.Props(**d["props"])

    loco_graphics: vehicle.Graphics
    with open(loco_graphics_path, "r") as loco_graphics_file:
        d = yaml.safe_load(loco_graphics_file)
        loco_graphics = vehicle.Graphics(**d)

    return (loco_props, loco_graphics)


def simple_vehicle(
        root: str, name: str,
        orientation_count: int = 8,
        animation_frame_count: int = 1,
        length: int | None = None
) -> grf.Train:
    (loco_props, loco_graphics) = load_yaml(root, name)
    sprite_table = VehicleSpriteTable(grf.TRAIN)

    engine_length = loco_props.length
    if length != None:
        engine_length = length

    # set up loco graphics
    engine_sprites: list[grf.FileSprite] = []
    engine_layouts: list[grf.GenericSpriteLayout] = []
    for sprite_group in loco_graphics.sprite_groups:
        engine_sprites = sprite_group.file_sprites()[:orientation_count]  # 8 sprites, 1 for each orientation
        # make the engine layout
        engine_layouts.append(sprite_table.get_layout(sprite_table.add_row(engine_sprites)))

    # set up purchase sprite
    purchase_sprite = loco_graphics.purchase_sprite
    if purchase_sprite == None:
        # no dedicated purchase sprite; use W realsprite instead
        purchase_sprite = engine_sprites[Orientation.PURCHASE]
    else:
        purchase_sprite = purchase_sprite.to_grf_file_sprite()
    purchase_layout = sprite_table.get_layout(
        sprite_table.add_purchase_graphics(
            purchase_sprite
        )
    )

    train = Train(
        id=loco_props.id, name="CATS " + loco_props.name, max_speed=Train.kmhish(loco_props.max_speed),
        weight=Train.ton(loco_props.weight_low),
        introduction_date=grf.datetime.date(
            year=loco_props.introduction_date[0],
            month=loco_props.introduction_date[1],
            day=loco_props.introduction_date[2]),
        length=engine_length, **
        {k: v for k, v in dataclasses.asdict(loco_props).items()
         if k not in ["id", "name", "introduction_date", "introduction_days_since_1920", "max_speed", "length",]},
        callbacks={"graphics": grf.GraphicsCallback(
            default=animated_vehicle(Switch, engine_layouts, animation_frame_count),
            purchase=purchase_layout)})
    return train


def simple_vehicle_long(
        root: str, name: str,
        orientation_count: int = 8,
        animation_frame_count: int = 1,
        length: int | None = None
) -> grf.Train:
    '''
    Builds a simple vehicle with exactly 8 orientations, no animations, consists of a single unit,
    and is longer than 8 length.

    This is uses a workaround for a current bug/incompatibility/limitation/??? with auto-articulation in grfpy 0.3.0.
    With vehicles of a length > 8, you cannot use any switches (or at least GraphicsCallback) on it
    The workaround is to use a livery instead of a GraphicsCallback.
    '''
    (loco_props, loco_graphics) = load_yaml(root, name)

    engine_length = loco_props.length
    if length != None:
        engine_length = length

    # set up loco graphics
    engine_sprites: list[grf.FileSprite] = []
    for sprite_group in loco_graphics.sprite_groups:
        engine_sprites.extend(sprite_group.file_sprites()[:orientation_count])  # 8 sprites, 1 for each orientation

    train = Train(
        id=loco_props.id, name="CATS " + loco_props.name, max_speed=Train.kmhish(loco_props.max_speed),
        weight=Train.ton(loco_props.weight_low),
        introduction_date=grf.datetime.date(
            year=loco_props.introduction_date[0],
            month=loco_props.introduction_date[1],
            day=loco_props.introduction_date[2]),
        length=engine_length,
        liveries=[{  # using a livery to bypass limitation in grfpy 0.3.0 with auto-articulation
            "name": "Default",
            "sprites": engine_sprites
        }],
        **
        {k: v for k, v in dataclasses.asdict(loco_props).items()
            if k not in ["id", "name", "introduction_date", "introduction_days_since_1920", "max_speed", "length",]})
    return train
