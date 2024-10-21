import os
from typing import Any

import grf
import yaml

from make_vehicles import make_vehicles
from make_vehicles.constructors.constructors import bind_grf

cats_grf = grf.NewGRF(
    grfid=b"BY\x01\x03",  # someone took BY\x01\x02???
    name="Combined American Train Set",
    description="An American train set for the modern age.",
    id_map_file="./id_map.json",
)

Train: type[grf.Train]
VehicleSpriteTable: type[grf.VehicleSpriteTable]
Switch: type[grf.Switch]

(
    Train,
    VehicleSpriteTable,
    Switch
) = (
    cats_grf.bind(grf.Train),
    cats_grf.bind(grf.VehicleSpriteTable),
    cats_grf.bind(grf.Switch)
)


def main():

    global cats_grf, Train, VehicleSpriteTable, Switch

    # remove vanilla trains
    cats_grf.add(grf.DisableDefault(grf.TRAIN))
    # fix sprites being cut off in the depot
    cats_grf.add(grf.SetGlobalTrainMiscFlag(grf.GlobalTrainMiscFlag.DEPOT_FULL_TRAIN_WIDTH))
    # fix sprites being too high in depot
    cats_grf.add(grf.SetGlobalTrainDepotYOffset(2))

    # set cargo table for default cargo assignments
    with open("./cargo-table.yaml", "r") as cargoTableFile:
        cats_grf.set_cargo_table(yaml.safe_load(cargoTableFile))

    # iterate through each vehicle in vehicles to generate the trains
    for root, subdirs, files in os.walk("./vehicles"):
        if len(subdirs) > 0:  # skip folders with folders inside
            continue
        bind_grf(cats_grf)
        make_vehicles.make_vehicle(root, os.path.basename(root))

    grf.main(cats_grf, "dist/cats.grf")


if __name__ == "__main__":
    main()
