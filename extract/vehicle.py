from typing import Any


CARGO_CLASSES = [
    "CC_PASSENGERS", "CC_MAIL", "CC_EXPRESS", "CC_ARMOURED", "CC_BULK", "CC_PIECE_GOODS", "CC_LIQUID",
    "CC_REFRIGERATED", "CC_HAZARDOUS", "CC_COVERED", "CC_OVERSIZED", "CC_POWDERIZED", "CC_NON_POURABLE", "CC_NEO_BULK",
    "CC_SPECIAL",]


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
        copy = self.props.copy()
        copy["id"] = self.id
        copy["name"] = self.name
        # copy["groupName"] = self.groupName
        # copy["purchaseGroupName"] = self.purchaseGroupName
        # copy["sprites"] = self.sprites
        # copy["purchaseSprite"] = self.purchaseSprite
        return copy

    def toReadableCargoClasses(self, bitmask: int) -> list[str]:
        classes = []
        for i, cargoClass in enumerate(CARGO_CLASSES):
            if bitmask & (1 << i) != 0:
                classes.append(cargoClass)
        return classes

    def toReadableCargo(self, cargoes, cargoTable: list[str]) -> list[str]:
        return [cargoTable[c] for c in cargoes]
