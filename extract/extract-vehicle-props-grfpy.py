import csv
import json

import grffile


FIELDNAMES = ['id', 'name', 'introduction_days_since_1920', 'introduction_date', 'reliability_decay', 'vehicle_life', 'model_life', 'track_type', 'climates_available', 'loading_speed', 'max_speed', 'power', 'weight_low', 'weight_high', 'tractive_effort_coefficient', 'cost_factor', 'running_cost_factor', 'shorten_by', 'visual_effect_and_powered', 'engine_class', 'running_cost_base', 'sprite_id', 'dual_headed',
              'cargo_capacity', 'default_cargo_type', 'ai_special_flag', 'ai_engine_rank', 'sort_purchase_list', 'extra_power_per_wagon', 'refit_cost', 'refittable_cargo_types''cb_flags', 'air_drag_coefficient', 'extra_weight_per_wagon', 'bitmask_vehicle_info''retire_early', 'misc_flags', 'refittable_cargo_classes', 'non_refittable_cargo_classes', 'cargo_age_period', 'cargo_allow_refit', 'cargo_disallow_refit',
              'retire_early', 'bitmask_vehicle_info', 'cb_flags', 'refittable_cargo_types']
CARGO_FIELDS = ['cargo_allow_refit', 'cargo_disallow_refit']


def main():
    with open("./vehicle-stats.csv", "w") as vehicleStatsCsv, open("./vehicle-stats.json", "w") as vehicleStatsJson:
        nars = grffile.GRFFile("../decompiled/newnars.grf")
        statsWriter = csv.DictWriter(vehicleStatsCsv, FIELDNAMES)
        statsWriter.writeheader()

        rows = [train.flatten() for train in nars.trains.values()]
        rows.sort(key=lambda row: row["id"])
        statsWriter.writerows(rows)
        json.dump(rows, vehicleStatsJson,
                  sort_keys=True, default=str, indent=4)


if __name__ == "__main__":
    main()
