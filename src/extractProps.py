import dataclasses
import json
import os
import re
import shutil
import yaml

from group import ID_TO_GROUPS, Car, Loco, Purchase, Tender
from vehicle import Vehicle, SpriteGroup, VehicleProps
from enums import Loc
import grffile


def extractProps():
    RES = "./res"
    VEHICLES = "./vehicles"
    CARS = "cars"
    LOCOS = "locos"
    STEAM = "steam"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    PAX = "pax"
    LOCO = "loco"

    default_props = dataclasses.asdict(VehicleProps.default())

    nars = grffile.GRFFile("./decompiled/newnars.grf")
    trains = {train._id: train for train in nars.trains.values()}
    spriteGroups: dict[str, SpriteGroup] = {sprite.group: sprite for sprite in nars.sprites}

    with open(os.path.join(VEHICLES, "cargo-table.yaml"), "w") as cargoTable:
        yaml.dump(nars.cargo_table, cargoTable)

    for id, sprites in ID_TO_GROUPS.items():
        train = trains[id]

        # process train name
        train_name = train._name
        train_name = re.sub(r'[^\w\s-]', '', train_name.lower()).strip('-_')
        train_name = re.sub('-', '', train_name)
        train_name = re.sub(r' ', '_', train_name)

        # create the folder that the train will go in
        path_prefix = ""
        veh_type = LOCOS if train.props.power > 0 else CARS
        tractive_type = ""
        loco_type = PAX if veh_type == LOCOS and train.props.refittable_cargo_classes == 1 \
            else LOCO if veh_type == LOCOS \
            else ""
        match train.props.engine_class:
            case 0: tractive_type = STEAM if veh_type == LOCOS else ""
            case 8: tractive_type = DIESEL
            case 40: tractive_type = ELECTRIC
        if veh_type == CARS:
            path_prefix = os.path.join(VEHICLES, CARS)
        else:
            path_prefix = os.path.join(VEHICLES, LOCOS, tractive_type, loco_type)

        # make the train's directory as needed
        sprite_path = os.path.join(path_prefix, f"{id}-{train_name}")
        if not os.path.isdir(sprite_path):
            os.makedirs(sprite_path)
        # move the sprites for this train
        for sprite in sprites:
            group_path = os.path.join(RES, f"{sprite.group}.png")
            shutil.copy(group_path, sprite_path)
        # # add graphics offsets to the train struct
        # groups = ID_TO_GROUPS[id]
        # train.graphics.gs = [g for g in groups if isinstance(g, (Loco, Tender, Car))]
        # for group in groups:
        #     spriteGroup: SpriteGroup = spriteGroups[group.group]
        #     if isinstance(group, (Loco, Tender, Car)):
        #         train.graphics.spriteGroups[group.group] = spriteGroup
        #     elif isinstance(group, Purchase):
        #         train.graphics.purchaseSprite = spriteGroup

        # write to the train's yaml file
        with open(os.path.join(sprite_path, f"{id}-{train_name}.yaml"), "w") as veh:
            d = {k: v for k, v in dataclasses.asdict(train).items() if k not in ["graphics"]}
            d["props"] = {k: list(v) if type(v) is tuple else v
                          for k, v in d["props"].items() if v != default_props[k]}
            # d["graphics"] = {k: v for k, v in d["graphics"].items() if k in ["purchaseSprite", "spriteGroups"]}
            yaml.dump(d, veh, indent=4, default_flow_style=False)


if __name__ == "__main__":
    extractProps()
