from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

from enums import Loc, TenderSpriteLocation

false = False
true = True


# @dataclass
# class E:
#     id: int = -1
#     isPurchaseSprite: bool = False
#     reversable: bool = False
#     loc: Loc = Loc.Full
#     liv: list[str] = field(default_factory=list)
#     alt: list[str] = field(default_factory=list)
#     mu: bool = False  # whether this group is a car for an MU.
#     length: int = 8  # number of 1/8tl units the sprite is
#     locoSprites: int = 8
#     tender: TenderSpriteLocation = TenderSpriteLocation.No
#     bUnitSprites: int = -1
#     parts: list[str] = field(default_factory=list)
#     cars: list[str] = field(default_factory=list)
#     locoForCars: str = ""


@dataclass
class G:
    group: str = ""
    reversable: bool = False
    loc: Loc = Loc.Full
    liv: list[str] = field(default_factory=list)
    alt: list[str] = field(default_factory=list)
    mu: bool = False  # whether this group is a car for an MU.
    length: int = 8  # number of 1/8tl units the sprite is
    frames: int = 1
    tender: TenderSpriteLocation = TenderSpriteLocation.No
    tenderLength: int = 8
    bUnitSprites: int = -1
    parts: list[str] = field(default_factory=list)
    cars: list[str] = field(default_factory=list)
    locoForCars: str = ""


@dataclass
class Loco(G):
    kind: str = "Loco"

    def __post_init__(self):
        self.kind = "Loco" if self.kind != "Loco" else "Loco"


@dataclass
class Tender(G):
    kind: str = "Tender"

    def __post_init__(self):
        self.kind = "Tender" if self.kind != "Tender" else "Tender"


@dataclass
class Car(G):
    kind: str = "Car"

    def __post_init__(self):
        self.kind = "Car" if self.kind != "Car" else "Car"


@dataclass
class Purchase(G):
    kind: str = "Purchase"

    def __post_init__(self):
        self.kind = "Purchase" if self.kind != "Purchase" else "Purchase"


front = Loc.Front
back = Loc.Back
tender = Loc.Tender
end = Loc.End

no = TenderSpriteLocation.No
same = TenderSpriteLocation.Same
separate = TenderSpriteLocation.Separate

ID_TO_GROUPS: dict[int, list[G]] = {
    0: [Loco("train_1", false, tender=same, tenderLength=2), Purchase("train_2")],
    1: [Loco("train_3", frames=4, tender=same, tenderLength=3), Purchase("train_4")],
    2: [Loco("train_5", frames=4, tender=same, tenderLength=3), Purchase("train_6")],
    3: [Loco("train_7", frames=4, tender=same, tenderLength=3), Purchase("train_8")],
    4: [Loco("train_9", frames=4, tender=same, tenderLength=4), Purchase("train_10")],
    5: [Loco("train_11", frames=4, tender=same, tenderLength=4), Purchase("train_12")],
    6: [Loco("train_13", frames=4, tender=same, tenderLength=5), Purchase("train_14")],
    7: [Loco("train_15", frames=4, tender=same, tenderLength=5), Purchase("train_16")],
    8: [Loco("train_17", frames=4, tender=same, tenderLength=4), Loco("train_18", reversable=true, frames=4, tender=same, tenderLength=4), Purchase("train_19")],
    9: [Loco("train_20", frames=4, tender=same, tenderLength=5), Purchase("train_21")],
    10: [Loco("train_22", frames=4, tender=same, tenderLength=5), Purchase("train_23")],
    11: [Loco("train_24", frames=4, tender=same, tenderLength=6), Purchase("train_25")],
    12: [Loco("train_26", frames=4, tender=same, tenderLength=6), Purchase("train_27")],
    13: [Loco("train_28", frames=4, tender=same, tenderLength=6), Purchase("train_29")],
    14: [Loco("train_30", loc=back, frames=4, tender=separate),
         Loco("train_31", loc=front, frames=4, tender=separate),
         Loco("train_32", loc=front, frames=4, tender=separate),
         Loco("train_33", loc=front, frames=4, tender=separate),
         Tender("train_34", loc=tender, tender=same, tenderLength=6),
         Purchase("train_35")],
    15: [Loco("train_36", frames=4, tender=same, tenderLength=6), Purchase("train_37")],
    16: [Loco("train_38", frames=4, tender=separate),
         Tender("train_39", loc=tender, tender=same, tenderLength=6),
         Purchase("train_40", liv=["train_38", "train_39", "train_40"])],
    17: [Loco("train_41", loc=back, frames=4, tender=separate),
         Loco("train_42", loc=front, frames=4, tender=separate),
         Loco("train_43", loc=front, frames=4, tender=separate),
         Loco("train_44", loc=front, frames=4, tender=separate),
         Tender("train_45", loc=tender, tender=same, tenderLength=6),
         Purchase("train_46")],
    16: [Loco("train_47", frames=4, tender=separate),
         Tender("train_48", loc=tender, tender=same, tenderLength=6),
         Purchase("train_49")],
    18: [Loco("train_50", frames=4, tender=same, tenderLength=5), Purchase("train_51")],
    19: [Loco("train_52", frames=4, tender=same, tenderLength=7), Purchase("train_53")],
    20: [Loco("train_54", bUnitSprites=8)],
    21: [Loco("train_55", reversable=true, frames=2, bUnitSprites=2*8), Purchase("train_56")],
    22: [Loco("train_57", reversable=true), Purchase("train_58")],
    23: [Loco("train_59", reversable=true, frames=2, bUnitSprites=2*8), Purchase("train_60")],
    24: [Loco("train_61", reversable=true), Purchase("train_62")],
    25: [Loco("train_63")],
    26: [Loco("train_64", reversable=true), Purchase("train_65")],
    27: [Loco("train_66")],
    28: [Loco("train_67", length=10), Purchase("train_68", length=10)],  # emd centennial, 40px = 10/8tl
    29: [Loco("train_69")],
    30: [Loco("train_70"), Purchase("train_71")],
    31: [Loco("train_72"), Purchase("train_73")],
    32: [Loco("train_74", reversable=true, bUnitSprites=8), Purchase("train_75")],
    33: [Loco("train_76")],
    34: [Loco("train_77", liv=["train_77"]), Loco("train_78", liv=["train_78"]), Purchase("train_79")],
    35: [Loco("train_80", reversable=true), Purchase("train_81")],
    36: [Loco("train_82", bUnitSprites=8)],
    37: [Loco("train_83", reversable=true, bUnitSprites=8), Purchase("train_84")],
    38: [Loco("train_85", reversable=true), Purchase("train_86")],
    39: [Loco("train_87")],
    40: [Loco("train_88", reversable=true), Purchase("train_89")],
    41: [Loco("train_90")],
    42: [Loco("train_91")],
    43: [Loco("train_92")],
    44: [Loco("train_93")],
    45: [Loco("train_94")],
    46: [Loco("train_95")],
    47: [Loco("train_96", reversable=true, bUnitSprites=8), Purchase("train_97")],
    48: [Loco("train_98")],
    49: [Loco("train_99", reversable=true), Purchase("train_100")],
    50: [Loco("train_101", reversable=true), Purchase("train_102")],
    51: [Loco("train_103", reversable=true), Purchase("train_104")],
    52: [Loco("train_105", parts=["train_105", "train_105"], bUnitSprites=8), Purchase("train_106")],
    53: [Loco("train_107")],
    54: [Loco("train_108")],
    55: [Loco("train_109", reversable=true), Purchase("train_110")],
    56: [Loco("train_111", reversable=true), Purchase("train_112")],
    57: [Loco("train_113", reversable=true), Purchase("train_114")],
    58: [Loco("train_115")],
    59: [Loco("train_116")],
    60: [Loco("train_117")],
    61: [Loco("train_118", frames=4)],
    62: [Loco("train_119", reversable=true, parts=["train_119", "train_119", "train_119", "train_119"], bUnitSprites=8, locoForCars="train_119"), Purchase("train_120")],
    63: [Loco("train_121", parts=["train_121", "train_121"], bUnitSprites=8, cars=["train_123", "train_123"]), Purchase("train_122"), Car("train_123", mu=true, parts=["train_121", "train_121"], cars=["train_123", "train_123"], locoForCars="train_121")],
    64: [Loco("train_124", parts=["train_124", "train_124"], bUnitSprites=8, cars=["train_126", "train_126"]), Purchase("train_125"), Car("train_126", mu=true, cars=["train_126", "train_126"], locoForCars="train_124")],
    65: [Loco("train_127")],
    66: [Loco("train_128", cars=["train_130", "train_130"]), Purchase("train_129"), Car("train_130", locoForCars="train_128")],
    67: [Loco("train_131", mu=true, cars=["train_133"]), Purchase("train_132"), Car("train_133", locoForCars="train_131")],
    68: [Loco("train_134", parts=["train_134", "train_134"], bUnitSprites=8, cars=["train_136", "train_136"]), Purchase("train_135"), Car("train_136", mu=true, locoForCars="train_134")],
    69: [Loco("train_137", cars=["train_139"]), Purchase("train_138"), Car("train_139", locoForCars="train_137")],
    80: [Car("train_140", loc=end), Purchase("train_141")],
    81: [Car("train_142")],
    82: [Car("train_143", liv=["train_143"]), Car("train_144", liv=["train_144"])],
    83: [Car("train_145", liv=["train_145"]), Car("train_146", liv=["train_146"])],
    84: [Car("train_147")],
    85: [Car("train_148"), Purchase("train_149")],
    86: [Car("train_150"), Purchase("train_151")],
    87: [Car("train_152"), Car("train_153", loc=end)],
    88: [Car("train_154"), Car("train_155", loc=end)],
    89: [Car("train_156"), Car("train_157", loc=end)],
    82: [Car("train_158", liv=["train_158"]), Purchase("train_159", liv=["train_158"])],
    90: [Car("train_160"), Purchase("train_161")],
    91: [Car("train_162"), Purchase("train_163")],
    92: [Car("train_164"), Purchase("train_165")],
    93: [Car("train_166"), Purchase("train_167")],
    94: [Car("train_168", loc=end), Car("train_169"), Purchase("train_170")],
    95: [Car("train_171", loc=end), Car("train_172"), Purchase("train_173")],
    96: [Car("train_174"), Purchase("train_175")],
    97: [Car("train_176"), Purchase("train_177")],
    98: [Car("train_178"), Purchase("train_179")],
    99: [Car("train_180"), Purchase("train_181")],
    100: [Car("train_182"), Purchase("train_183")],
    101: [Car("train_184"), Purchase("train_185")],
    102: [Car("train_186"), Car("train_187"), Purchase("train_188")],
    103: [Car("train_189"), Car("train_190", loc=end)],
    104: [Car("train_191"), Car("train_192", loc=end)],
    105: [Car("train_193"), Car("train_194", loc=end), Purchase("train_195")],
    106: [Purchase("train_196"), Car("train_197")],
    107: [Purchase("train_198"), Car("train_199")],
    108: [Purchase("train_200"), Car("train_201", loc=end), Car("train_202")],
    109: [Car("train_203", loc=end), Car("train_204")],
    110: [Purchase("train_205"), Car("train_206")],
    111: [Purchase("train_207"), Car("train_208")],
    112: [Car("train_209", loc=end), Car("train_210")],
    113: [Car("train_211"), Car("train_212"), Car("train_213", loc=end), Car("train_214"), Purchase("train_215")],
    114: [Car("train_216", loc=end), Car("train_217")],
    115: [Car("train_218", loc=end), Car("train_219")],
    116: [Car("train_220"), Purchase("train_221")],
    117: [Car("train_222"), Purchase("train_223")],
    118: [Car("train_224", loc=end, liv=["train_224", "train_225"]), Car("train_225", liv=["train_224", "train_225"])],
    119: [Car("train_226", loc=end), Car("train_227")],
    120: [Car("train_228"), Purchase("train_229")],
    121: [Car("train_230"), Purchase("train_231")],
}


# def initGroups():
#     for id in GROUP_TO_ID:
#         e = GROUP_TO_ID[id]
#         if e.isPurchaseSprite:
#             e.loc = Loc.Purchase

# init id to group
# for id in GROUP_TO_ID:
# e = GROUP_TO_ID[id]
# if e.id not in ID_TO_GROUPS:
#  ID_TO_GROUPS[e.id] = []

# if


# SIMPLE_VEHICLES = {}


# def simpleVehicles() -> dict[str, E]:
#     global SIMPLE_VEHICLES
#     if SIMPLE_VEHICLES != {}:
#         return SIMPLE_VEHICLES

#     '''
#     a simple vehicle is:
#     - its id only appears once as a value
#     - does not have a dedicated purchase sprite
#     - has no liveries
#     '''
#     # invert the mapping
#     invGroups = {}
#     for name, e in GROUP_TO_ID.items():
#         if not e.isPurchaseSprite and e.liv == []:
#             invGroups[e.id] = invGroups.get(e.id, []) + [name]

#     simpleNames = [names[0] for id, names in invGroups.items() if len(names) == 1]
#     SIMPLE_VEHICLES = {name: GROUP_TO_ID[name] for name in simpleNames}

#     return SIMPLE_VEHICLES
