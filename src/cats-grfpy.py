import grf
import json

import group as G
import vehicle as V
import make as M

catsGrf = grf.NewGRF(
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
    catsGrf.bind(grf.Train),
    catsGrf.bind(grf.VehicleSpriteTable),
    catsGrf.bind(grf.Switch)
)


def main():

    global catsGrf, Train, VehicleSpriteTable, Switch

    # this is here up top to remove vanilla trains
    catsGrf.add(grf.DisableDefault(grf.TRAIN))
    # fix sprites being cut off in the depot
    catsGrf.add(grf.SetGlobalTrainMiscFlag(grf.GlobalTrainMiscFlag.DEPOT_FULL_TRAIN_WIDTH))
    # fix sprites being too high in depot
    catsGrf.add(grf.SetGlobalTrainDepotYOffset(2))

    with open("./props/cargo-table.json", "r") as cargoTableFile:
        catsGrf.set_cargo_table(json.load(cargoTableFile))

    with open("./props/vehicle-stats-sprites.json", "r") as vehicleFile:
        vehicles: list[V.Vehicle] = [V.Vehicle(**e) for e in json.load(vehicleFile)]
        for vehicle in vehicles:
            print(f"Making {vehicle.name} w/ id={vehicle.id}...", end=" ")
            if isinstance(vehicle.graphics.gs[0], G.Loco):
                match vehicle.graphics.gs[0].locoType:
                    case G.LT.SteamTank:
                        # unused
                        pass
                    case G.LT.SteamTender:
                        M.makeSteamTender(vehicle, Train, VehicleSpriteTable, Switch)
                    case G.LT.SteamArticulatedTank:
                        # unused
                        pass
                    case G.LT.SteamArticulatedTender:
                        # TODO makeArticulatedSteamEngine(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.DieselSingle:
                        M.makeDieselSingle(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.DieselAA:
                        M.makeDieselAA(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.DieselAB:
                        M.makeDieselAB(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.DieselABBA:
                        M.makeDieselABBA(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.ElectricSingle:
                        M.makeElectricSingle(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.ElectricArticulated:
                        M.makeElectricArticulated(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
                    case G.LT.ElectricAA:
                        M.makeElectricAA(vehicle, Train, VehicleSpriteTable, Switch)
                        pass
            elif isinstance(vehicle.graphics.gs[0], G.Car):
                # TODO
                pass
            print("Done!", end="\n")

    grf.main(catsGrf, "dist/cats.grf")


if __name__ == "__main__":
    main()
