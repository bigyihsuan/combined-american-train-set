from dataclasses import dataclass, field
import datetime
from typing import Any
import group as G

import grf


CARGO_CLASSES = [
    "CC_PASSENGERS", "CC_MAIL", "CC_EXPRESS", "CC_ARMOURED", "CC_BULK", "CC_PIECE_GOODS", "CC_LIQUID",
    "CC_REFRIGERATED", "CC_HAZARDOUS", "CC_COVERED", "CC_OVERSIZED", "CC_POWDERIZED", "CC_NON_POURABLE", "CC_NEO_BULK",
    "CC_SPECIAL",]
CALLBACKS = ["VEH_CBF_VISUAL_EFFECT_AND_POWERED", "VEH_CBF_WAGON_LENGTH", "VEH_CBF_LOAD_AMOUNT",
             "VEH_CBF_REFITTED_CAPACITY", "VEH_CBF_ARTICULATED_PARTS", "VEH_CBF_CARGO_SUFFIX",
             "VEH_CBF_COLOUR_MAPPING", "Sound effect callbacks (unused)"]
FLAGS = ["TRAIN_FLAG_TILT", "TRAIN_FLAG_2CC", "TRAIN_FLAG_MU", "TRAIN_FLAG_FLIP", "TRAIN_FLAG_AUTOREFIT",
         "Cargo multiplier (unused)", "TRAIN_FLAG_NO_BREAKDOWN_SMOKE", "TRAIN_FLAG_SPRITE_STACK"]


@dataclass
class VehicleProps:
    introduction_days_since_1920: int = 0
    introduction_date: list[int] = field(default_factory=lambda: [1900, 1, 1])
    reliability_decay: int = 0
    vehicle_life: int = 0
    model_life: int = 0
    track_type: int = 0
    climates_available: int = 0
    loading_speed: int = 0
    max_speed: int = 0
    power: int = 0
    weight_low: int = 0
    weight_high: int = 0
    tractive_effort_coefficient: int = 0
    cost_factor: int = 0
    running_cost_factor: int = 0
    shorten_by: int | None = 0
    visual_effect_and_powered: int = 0
    engine_class: int = 0
    running_cost_base: int = 0
    sprite_id: int = 0
    dual_headed: int = 0
    cargo_capacity: int = 0
    default_cargo_type: int = 0
    ai_special_flag: int = 0
    ai_engine_rank: int = 0
    sort_purchase_list: int = 0
    extra_power_per_wagon: int = 0
    refit_cost: int = 0
    refittable_cargo_types: int = 0
    cb_flags: int = 0
    air_drag_coefficient: int = 0
    extra_weight_per_wagon: int = 0
    bitmask_vehicle_info: int = 0
    retire_early: int = 0
    misc_flags: int = 0
    refittable_cargo_classes: int = 0
    non_refittable_cargo_classes: int = 0
    cargo_age_period: int = 0
    cargo_allow_refit: list[int] = field(default_factory=list)
    cargo_disallow_refit: list[int] = field(default_factory=list)
    length: int = 8


@dataclass
class Sprite:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    xofs: int = 0
    yofs: int = 0
    zoom: int = 0
    bpp: int = 0


@dataclass
class SpriteGroup:
    group: str = ""
    loc: str = G.Loc.Unset
    realSprites: list[Sprite] = field(default_factory=list)


@dataclass
class VehicleGraphics:
    purchaseSprite: SpriteGroup = field(default_factory=SpriteGroup)
    sprites: list[SpriteGroup] = field(default_factory=list)


@dataclass
class Vehicle:
    id: int = -1
    name: str = ""
    props: VehicleProps = field(default_factory=VehicleProps)
    graphics: VehicleGraphics = field(default_factory=VehicleGraphics)

    @staticmethod
    def toReadableCargoClasses(bitmask: int) -> list[str]:
        classes = []
        for i, cargoClass in enumerate(CARGO_CLASSES):
            if bitmask & (1 << i) != 0:
                classes.append(cargoClass)
        return classes

    @staticmethod
    def toReadableCargo(cargoes, cargoTable: list[str]) -> list[str]:
        return [cargoTable[c] for c in cargoes]

    @staticmethod
    def toReadableCallback(bitmask) -> list[str]:
        callbacks = []
        for i, cb in enumerate(CALLBACKS):
            if bitmask & (1 << i) != 0:
                callbacks.append(cb)
        return callbacks

    @staticmethod
    def toReadableFlag(bitmask) -> list[str]:
        flags = []
        for i, flag in enumerate(FLAGS):
            if bitmask * (1 << i) != 0:
                flags.append(flag)
        return flags
