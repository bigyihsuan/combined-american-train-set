import ast
import datetime
from typing import Any
import grf
import csv
import json

FIELDNAMES = ['id', 'name', 'introduction_days_since_1920', 'introduction_date', 'reliability_decay', 'vehicle_life', 'model_life', 'track_type', 'climates_available', 'loading_speed', 'max_speed', 'power', 'weight_low', 'weight_high', 'tractive_effort_coefficient', 'cost_factor', 'running_cost_factor', 'shorten_by', 'visual_effect_and_powered', 'engine_class', 'running_cost_base', 'sprite_id', 'dual_headed',
              'cargo_capacity', 'default_cargo_type', 'ai_special_flag', 'ai_engine_rank', 'sort_purchase_list', 'extra_power_per_wagon', 'refit_cost', 'refittable_cargo_types''cb_flags', 'air_drag_coefficient', 'extra_weight_per_wagon', 'bitmask_vehicle_info''retire_early', 'misc_flags', 'refittable_cargo_classes', 'non_refittable_cargo_classes', 'cargo_age_period', 'cargo_allow_refit', 'cargo_disallow_refit',
              'retire_early', 'bitmask_vehicle_info', 'cb_flags', 'refittable_cargo_types']

with open("../decompiled/newnars/generate.py", "r") as originalGrfFile, open("./vehicle-stats.csv", "w") as vehicleStatsCsv, open("./vehicle-stats.json", "w") as vehicleStatsJson:
    statsWriter = csv.DictWriter(vehicleStatsCsv, FIELDNAMES)
    originalGrfPy: str = originalGrfFile.read()
    tree: ast.Module = ast.parse(originalGrfPy)

    trainDefines = [stmt.value for stmt in tree.body if isinstance(stmt, ast.Expr)
                    and isinstance(stmt.value, ast.Call)
                    and isinstance(stmt.value.func, ast.Name)
                    and stmt.value.func.id == "Define"
                    and any([keyword.arg == 'feature' and isinstance(keyword.value, ast.Name) and keyword.value.id == "TRAIN" for keyword in stmt.value.keywords])]

    trainStringsKws = [stmt.value.keywords for stmt in tree.body if isinstance(stmt, ast.Expr)
                       and isinstance(stmt.value, ast.Call)
                       and isinstance(stmt.value.func, ast.Name)
                       and stmt.value.func.id == "DefineStrings"
                       and any([keyword.arg == 'feature' and isinstance(keyword.value, ast.Name) and keyword.value.id == "TRAIN" for keyword in stmt.value.keywords])]
    trainNames = {eval(ast.unparse(kw[2].value)): eval(
        ast.unparse(kw[4].value))[0] for kw in trainStringsKws}

    statsWriter.writeheader()
    rows = []
    for call in trainDefines:
        idKws = [kw for kw in call.keywords if kw.arg == "id"][0]
        id: int = eval(ast.unparse(idKws.value))
        propKws = [kw for kw in call.keywords if kw.arg == "props"][0]
        props: dict[str, Any] = eval(ast.unparse(propKws.value))
        for k, v in props.items():
            if isinstance(v, bytes) and len(v) == 0:
                props[k] = v.decode("utf-8")
        row = props.copy()
        row["id"] = id
        row["name"] = trainNames[id].decode("utf-8")
        statsWriter.writerow(row)
        rows.append(row)
    json.dump(rows, vehicleStatsJson, sort_keys=True, default=str, indent=4)
