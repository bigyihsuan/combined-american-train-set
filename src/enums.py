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
