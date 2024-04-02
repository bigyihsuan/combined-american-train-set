from typing import Any


CARGO_CLASSES = [
    "CC_PASSENGERS", "CC_MAIL", "CC_EXPRESS", "CC_ARMOURED", "CC_BULK", "CC_PIECE_GOODS", "CC_LIQUID",
    "CC_REFRIGERATED", "CC_HAZARDOUS", "CC_COVERED", "CC_OVERSIZED", "CC_POWDERIZED", "CC_NON_POURABLE", "CC_NEO_BULK",
    "CC_SPECIAL",]
CALLBACKS = ["VEH_CBF_VISUAL_EFFECT_AND_POWERED", "VEH_CBF_WAGON_LENGTH", "VEH_CBF_LOAD_AMOUNT",
             "VEH_CBF_REFITTED_CAPACITY", "VEH_CBF_ARTICULATED_PARTS", "VEH_CBF_CARGO_SUFFIX",
             "VEH_CBF_COLOUR_MAPPING", "Sound effect callbacks (unused)"]
FLAGS = ["TRAIN_FLAG_TILT", "TRAIN_FLAG_2CC", "TRAIN_FLAG_MU", "TRAIN_FLAG_FLIP", "TRAIN_FLAG_AUTOREFIT",
         "Cargo multiplier (unused)", "TRAIN_FLAG_NO_BREAKDOWN_SMOKE", "TRAIN_FLAG_SPRITE_STACK"]


class Vehicle:
    def __init__(
            self, id: int = -1, name: str = "", props: dict[str, Any] = {},
            groupName: str = "", purchaseGroupName: str = "", sprites: list[dict[str, int]] = [],
            purchaseSprite: dict[str, int] = {}) -> None:
        self.id = id
        self.name = name
        self.props = props
        self.groupName = groupName
        self.purchaseGroupName = purchaseGroupName
        self.sprites = sprites
        self.purchaseSprite = purchaseSprite

    def flatten(self) -> dict[str, Any]:
        copy = {"id": self.id, "name": self.name, **self.props}
        return copy

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
