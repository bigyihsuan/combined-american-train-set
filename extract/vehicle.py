from typing import Any
from nml.global_constants import constant_numbers as CN


CARGO_CLASSES = ["CC_PASSENGERS", "CC_MAIL", "CC_EXPRESS", "CC_ARMOURED", "CC_BULK", "CC_PIECE_GOODS", "CC_LIQUID",
                 "CC_REFRIGERATED", "CC_HAZARDOUS", "CC_COVERED", "CC_OVERSIZED", "CC_POWDERIZED", "CC_NON_POURABLE", "CC_NEO_BULK", "CC_SPECIAL",]


class Vehicle:
    def __init__(self, id: int, name: str, props: dict[str, Any]) -> None:
        self.id = id
        self.name = name
        self.props = props

    def flatten(self) -> dict[str, Any]:
        copy = self.props.copy()
        copy["id"] = self.id
        copy["name"] = self.name
        return copy

    def toReadableCargoClasses(self, bitmask: int) -> list[str]:
        classes = []
        for i, cargoClass in enumerate(CARGO_CLASSES):
            if bitmask & (1 << i) != 0:
                classes.append(cargoClass)
        return classes

    def toReadableCargo(self, cargoBytes: bytes, cargoTable: list[str]) -> list[str]:
        cargoes = [cargoTable[c] for c in list(cargoBytes)]
        return cargoes


def chunk(l, n: int):
    for i in range(0, len(l), n):
        yield l[i:i + n]
