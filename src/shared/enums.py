from enum import Enum


class Loc(str, Enum):
    Unset = "Unset"
    Purchase = "Purchase"
    Full = "Full"
    FrontStraight = "FrontStraight"
    FrontLeft = "FrontLeft"
    FrontRight = "FrontRight"
    Back = "Back"
    Tender = "Tender"
    End = "End"


class TenderSpriteLocation(str, Enum):
    No = "No"
    Same = "Same"
    Separate = "Separate"


class LocoType(str, Enum):
    Unset = "Unset"
    SteamTank = "SteamTank"
    SteamTender = "SteamTender"
    SteamArticulatedTank = "SteamArticulatedTank"
    SteamArticulatedTender = "SteamArticulatedTender"
    DieselSingle = "DieselSingle"
    DieselAA = "DieselAA"
    DieselAB = "DieselAB"
    DieselABBA = "DieselABBA"
    ElectricSingle = "ElectricSingle"
    ElectricArticulated = "ElectricArticulated"
    ElectricAA = "ElectricAA"
    Car = "Car"


class Orientation(int, Enum):
    INVALID = -1
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    PURCHASE = 6
