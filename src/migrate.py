import dataclasses
import os
import re
import shutil

import yaml
import grffile
from group import ID_TO_GROUPS
from vehicle import VehicleProps

SPRITES_PATH = "./vehicles"
RES_PATH = "./res"

if __name__ == "__main__":
    default_props = dataclasses.asdict(VehicleProps.default())
    nars = grffile.GRFFile("./decompiled/newnars.grf")
    trains = {train._id: train for train in nars.trains.values()}

    for id, sprites in ID_TO_GROUPS.items():
        train = trains[id]

        train_name = train._name
        train_name = re.sub(r'[^\w\s-]', '', train_name.lower()).strip('-_')
        train_name = re.sub('-', '', train_name)
        train_name = re.sub(r' ', '_', train_name)

        sprite_path = os.path.join(SPRITES_PATH, f"{id}-{train_name}")
        if not os.path.isdir(sprite_path):
            os.mkdir(sprite_path)
        for sprite in sprites:
            group_path = os.path.join(RES_PATH, f"{sprite.group}.png")
            shutil.copy(group_path, sprite_path)

        with open(os.path.join(sprite_path, f"{id}-{train_name}.yaml"), "w") as veh:
            d = {k: v for k, v in dataclasses.asdict(trains[id]).items() if k != "graphics"}
            d["props"] = {k: list(v) if type(v) is tuple else v
                          for k, v in d["props"].items() if v != default_props[k]}
            yaml.dump(d, veh, indent=4, default_flow_style=False)
