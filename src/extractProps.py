import dataclasses
import itertools
import os
import re
import shutil

import yaml
from shared.enums import Orientation
from shared.grffile import GRFFile
from shared.group import ID_TO_GROUPS, Car, Loco, Purchase, Tender
from shared.vehicle import Props, SpriteGroup, VehicleProps


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

    orientations = [Orientation.N, Orientation.NE, Orientation.E, Orientation.SE,
                    Orientation.S, Orientation.SW, Orientation.W, Orientation.NW]

    default_props = dataclasses.asdict(Props.default())

    nars = GRFFile("./decompiled/newnars.grf")
    trains = {train._id: train for train in nars.trains.values()}
    spriteGroups: dict[str, SpriteGroup] = {sprite.file: sprite for sprite in nars.sprites}

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
            d["props"] = {k: v if type(v) is not tuple else list(v)
                          for k, v in d["props"].items() if v != default_props[k]}
            d["props"]["id"] = id
            d["props"]["name"] = train._name
            yaml.dump(d, veh, indent=4, default_flow_style=False)

        # create a graphics yaml for this train
        graphics_path = os.path.join(sprite_path, "graphics.yaml")
        with open(graphics_path, "w") as graphics_file:
            # take each sprite in realsprites, and everything except file and x/y
            d = {
                "sprite_groups": [],
                "purchase_sprite": None
            }
            for sprite in sprites:
                group_path = os.path.join(RES, f"{sprite.group}.png")
                real_path = os.path.join(sprite_path, f"{sprite.group}-real.png")
                purchase_path = os.path.join(sprite_path, f"{sprite.group}-purchase.png")
                spriteGroup: SpriteGroup = spriteGroups[sprite.group]
                path = ""
                if isinstance(sprite, (Loco, Tender, Car)):
                    sg = {}
                    sg["real_sprites"] = [dataclasses.asdict(
                        sprite) for sprite in spriteGroup.real_sprites]
                    for i, (sprite, orientation) in enumerate(
                        zip(sg["real_sprites"],
                            itertools.cycle(orientations))):
                        del sg["real_sprites"][i]["file"]  # file path is handled 1 level up
                        sg["real_sprites"][i]["orientation"] = orientation.value
                    sg["file"] = real_path
                    path = real_path
                    d["sprite_groups"].append(sg)

                elif isinstance(sprite, Purchase):
                    d["purchase_sprite"] = dataclasses.asdict(spriteGroup.real_sprites[0])
                    d["purchase_sprite"]["orientation"] = Orientation.PURCHASE.value
                    d["purchase_sprite"]["file"] = purchase_path
                    path = purchase_path
                # move the sprites for this train
                if not os.path.exists(path):
                    shutil.copy(group_path, path)

            yaml.dump(d, graphics_file)


if __name__ == "__main__":
    extractProps()
