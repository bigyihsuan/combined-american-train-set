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
