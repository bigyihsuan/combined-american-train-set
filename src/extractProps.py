import dataclasses
import json
import os
import re
import shutil
from typing import Any
import yaml

from group import G, ID_TO_GROUPS, Car, Loco, Purchase, Tender
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

    # checklist = open("./checklist.md", "w")
    # checklist.write("|Train|ID|Sprites Reorganized|Graphics YAML|Programmed|Fully Functional|\n")
    # checklist.write("|-|-|-|-|-|-|\n")
    # checklist.writelines([f"|{train._name}|{train._id}|||||\n" for train in trains.values()])
    # checklist.close()

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

        # write to the train's yaml file
        with open(os.path.join(sprite_path, f"{id}-{train_name}.yaml"), "w") as veh:
            d = {k: v for k, v in dataclasses.asdict(train).items() if k not in ["graphics"]}
            d["props"] = {k: list(v) if type(v) is tuple else v
                          for k, v in d["props"].items() if v != default_props[k]}
            # d["graphics"] = {k: v for k, v in d["graphics"].items() if k in ["purchaseSprite", "spriteGroups"]}
            yaml.dump(d, veh, indent=4, default_flow_style=False)

        # create a graphics yaml for this train
        graphics_path = os.path.join(sprite_path, "graphics.yaml")
        with open(graphics_path, "w") as graphics_file:
            # take each sprite in realsprites, and everything except file and x/y
            d = {
                "sprite_groups": {},
                "purchase_sprite": {}
            }
            for sprite in sprites:
                group_path = os.path.join(RES, f"{sprite.group}.png")
                real_path = os.path.join(sprite_path, f"{sprite.group}-real.png")
                purchase_path = os.path.join(sprite_path, f"{sprite.group}-purchase.png")
                spriteGroup: SpriteGroup = spriteGroups[sprite.group]
                path = ""
                if isinstance(sprite, (Loco, Tender, Car)):
                    d["sprite_groups"]["realsprites"] = [dataclasses.asdict(
                        sprite) for sprite in spriteGroup.realSprites]
                    for i, sprite in enumerate(d["sprite_groups"]["realsprites"]):
                        d["sprite_groups"]["realsprites"][i]["x"] = -1  # for later filling
                        d["sprite_groups"]["realsprites"][i]["y"] = -1  # for later filling
                        del d["sprite_groups"]["realsprites"][i]["file"]  # handled 1 level up
                    d["sprite_groups"]["file"] = real_path
                    path = real_path

                elif isinstance(sprite, Purchase):
                    d["purchase_sprite"] = dataclasses.asdict(spriteGroup.realSprites[0])
                    d["purchase_sprite"]["x"] = 0  # purchase sprites always appear at (0,0)
                    d["purchase_sprite"]["y"] = 0  # purchase sprites always appear at (0,0)
                    d["purchase_sprite"]["file"] = purchase_path
                    path = purchase_path
                # do not overwrite the modified files
                if not os.path.exists(path):
                    # move the sprites for this train
                    shutil.copy(group_path, path)

            yaml.dump(d, graphics_file)


if __name__ == "__main__":
    extractProps()
