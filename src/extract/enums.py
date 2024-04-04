from enum import Enum


class Loc(str, Enum):
    Unset = "Unset"
    Purchase = "Purchase"
    Full = "Full"
    Front = "Front"
    Back = "Back"
    Tender = "Tender"
    End = "End"


class TenderSpriteLocation(str, Enum):
    No = "No"
    Same = "Same"
    Separate = "Separate"
