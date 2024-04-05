from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

from enums import Loc, TenderSpriteLocation

false = False
true = True


@dataclass
class E:
    id: int = -1
    isPurchaseSprite: bool = False
    reversable: bool = False
    loc: Loc = Loc.Full
    liv: list[str] = field(default_factory=list)
    alt: list[str] = field(default_factory=list)
    mu: bool = False  # whether this group is a car for an MU.
    length: int = 8  # number of 1/8tl units the sprite is
    locoSprites: int = 8
    tender: TenderSpriteLocation = TenderSpriteLocation.No
    bUnitSprites: int = -1
    parts: list[str] = field(default_factory=list)
    cars: list[str] = field(default_factory=list)
    locoForCars: str = ""


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
    pass


@dataclass
class Tender(G):
    pass


@dataclass
class Car(G):
    pass


@dataclass
class Purchase(G):
    pass


front = Loc.Front
back = Loc.Back
tender = Loc.Tender
end = Loc.End

no = TenderSpriteLocation.No
same = TenderSpriteLocation.Same
separate = TenderSpriteLocation.Separate

GROUP_TO_ID: dict[str, E] = {
    # groupnamm: (id, isPurchaseSprite, notes?)
    # "train_0": E(),
    "train_1": E(0, tender=same),
    "train_2": E(0, isPurchaseSprite=true),
    "train_3": E(1, locoSprites=4, tender=same),
    "train_4": E(1, isPurchaseSprite=true),
    "train_5": E(2, locoSprites=4, tender=same),
    "train_6": E(2, isPurchaseSprite=true),
    "train_7": E(3, locoSprites=4, tender=same),
    "train_8": E(3, isPurchaseSprite=true),
    "train_9": E(4, locoSprites=4, tender=same),
    "train_10": E(4, isPurchaseSprite=true),
    "train_11": E(5, locoSprites=4, tender=same),
    "train_12": E(5, isPurchaseSprite=true),
    "train_13": E(6, locoSprites=4, tender=same),
    "train_14": E(6, isPurchaseSprite=true),
    "train_15": E(7, locoSprites=4, tender=same),
    "train_16": E(7, isPurchaseSprite=true),
    "train_17": E(8, locoSprites=4, tender=same),
    "train_18": E(8, reversable=true, locoSprites=4, tender=same),
    "train_19": E(8, isPurchaseSprite=true),
    "train_20": E(9, locoSprites=4, tender=same),
    "train_21": E(9, isPurchaseSprite=true),
    "train_22": E(10, locoSprites=4, tender=same),
    "train_23": E(10, isPurchaseSprite=true),
    "train_24": E(11, locoSprites=4, tender=same),
    "train_25": E(11, isPurchaseSprite=true),
    "train_26": E(12, locoSprites=4, tender=same),
    "train_27": E(12, isPurchaseSprite=true),
    "train_28": E(13, locoSprites=4, tender=same),
    "train_29": E(13, isPurchaseSprite=true),
    "train_30": E(14, loc=back, locoSprites=4, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_31": E(14, loc=front, locoSprites=4, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_32": E(14, loc=front, locoSprites=4, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_33": E(14, loc=front, locoSprites=4, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_34": E(14, loc=tender, tender=same, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_35": E(14, isPurchaseSprite=true),
    "train_36": E(15, locoSprites=4, tender=same),
    "train_37": E(15, isPurchaseSprite=true),
    "train_38": E(16, liv=["train_38", "train_39", "train_40"], locoSprites=4, tender=separate, parts=["train_38", "train_39"]),
    "train_39": E(16, loc=tender, liv=["train_38", "train_39", "train_40"], tender=same, parts=["train_38", "train_39"]),
    "train_40": E(16, isPurchaseSprite=true, liv=["train_38", "train_39", "train_40"]),
    "train_41": E(17, loc=back, locoSprites=4, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_42": E(17, loc=front, locoSprites=4, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_43": E(17, loc=front, locoSprites=4, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_44": E(17, loc=front, locoSprites=4, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_45": E(17, loc=tender, tender=same, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_46": E(17, isPurchaseSprite=true),
    "train_47": E(16, liv=["train_47", "train_48", "train_49"], alt=["train_70"], locoSprites=4, tender=separate, parts=["train_47", "train_48"]),
    "train_48": E(16, loc=tender, liv=["train_47", "train_48", "train_49"], alt=["train_70"], tender=same, parts=["train_47", "train_48"]),
    "train_49": E(16, isPurchaseSprite=true, liv=["train_47", "train_48", "train_49"], alt=["train_70"]),
    "train_50": E(18, locoSprites=4, tender=same),
    "train_51": E(18, isPurchaseSprite=true),
    "train_52": E(19, locoSprites=4, tender=same),
    "train_53": E(19, isPurchaseSprite=true),
    "train_54": E(20, bUnitSprites=8),
    "train_55": E(21, reversable=true, locoSprites=16*8, bUnitSprites=16*8),
    "train_56": E(21, isPurchaseSprite=true),
    "train_57": E(22, reversable=true),
    "train_58": E(22, isPurchaseSprite=true),
    "train_59": E(23, reversable=true, locoSprites=16*8, bUnitSprites=16*8),
    "train_60": E(23, isPurchaseSprite=true),
    "train_61": E(24, reversable=true),
    "train_62": E(24, isPurchaseSprite=true),
    "train_63": E(25),
    "train_64": E(26, reversable=true),
    "train_65": E(26, isPurchaseSprite=true),
    "train_66": E(27),
    "train_67": E(28, length=10),  # emd centennial, 40px = 10/8tl
    "train_68": E(28, isPurchaseSprite=true, length=10),  # emd centennial, 40px = 10/8tl
    "train_69": E(29),
    "train_70": E(30),
    "train_71": E(30, isPurchaseSprite=true),
    "train_72": E(31),
    "train_73": E(31, isPurchaseSprite=true),
    "train_74": E(32, reversable=true, bUnitSprites=8),
    "train_75": E(32, isPurchaseSprite=true),
    "train_76": E(33),
    "train_77": E(34, liv=["train_77"]),
    "train_78": E(34, liv=["train_78"]),
    "train_79": E(34, isPurchaseSprite=true),
    "train_80": E(35, reversable=true),
    "train_81": E(35, isPurchaseSprite=true),
    "train_82": E(36, bUnitSprites=8),
    "train_83": E(37, reversable=true, bUnitSprites=8),
    "train_84": E(37, isPurchaseSprite=true),
    "train_85": E(38, reversable=true),
    "train_86": E(38, isPurchaseSprite=true),
    "train_87": E(39),
    "train_88": E(40, reversable=true),
    "train_89": E(40, isPurchaseSprite=true),
    "train_90": E(41),
    "train_91": E(42),
    "train_92": E(43),
    "train_93": E(44),
    "train_94": E(45),
    "train_95": E(46),
    "train_96": E(47, reversable=true, bUnitSprites=8),
    "train_97": E(47, isPurchaseSprite=true),
    "train_98": E(48),
    "train_99": E(49, reversable=true),
    "train_100": E(49, isPurchaseSprite=true),
    "train_101": E(50, reversable=true),
    "train_102": E(50, isPurchaseSprite=true),
    "train_103": E(51, reversable=true),
    "train_104": E(51, isPurchaseSprite=true),
    "train_105": E(52, parts=["train_105", "train_105"], bUnitSprites=8),
    "train_106": E(52, isPurchaseSprite=true),
    "train_107": E(53),
    "train_108": E(54),
    "train_109": E(55, reversable=true),
    "train_110": E(55, isPurchaseSprite=true),
    "train_111": E(56, reversable=true),
    "train_112": E(56, isPurchaseSprite=true),
    "train_113": E(57, reversable=true),
    "train_114": E(57, isPurchaseSprite=true),
    "train_115": E(58),
    "train_116": E(59),
    "train_117": E(60),
    "train_118": E(61, locoSprites=4),
    "train_119": E(62, reversable=true, parts=["train_119", "train_119", "train_119", "train_119"], bUnitSprites=8, locoForCars="train_119"),
    "train_120": E(62, isPurchaseSprite=true),
    "train_121": E(63, parts=["train_121", "train_121"], bUnitSprites=8, cars=["train_123", "train_123"]),
    "train_122": E(63, isPurchaseSprite=true),
    "train_123": E(63, mu=true, parts=["train_121", "train_121"], cars=["train_123", "train_123"], locoForCars="train_121"),
    "train_124": E(64, parts=["train_124", "train_124"], bUnitSprites=8, cars=["train_126", "train_126"]),
    "train_125": E(64, isPurchaseSprite=true),
    "train_126": E(64, mu=true, cars=["train_126", "train_126"], locoForCars="train_124"),
    "train_127": E(65),
    "train_128": E(66, cars=["train_130", "train_130"]),
    "train_129": E(66, isPurchaseSprite=true),
    "train_130": E(66, locoForCars="train_128"),
    "train_131": E(67, mu=true, cars=["train_133"]),
    "train_132": E(67, isPurchaseSprite=true),
    "train_133": E(67, locoForCars="train_131"),
    "train_134": E(68, parts=["train_134", "train_134"], bUnitSprites=8, cars=["train_136", "train_136"]),
    "train_135": E(68, isPurchaseSprite=true),
    "train_136": E(68, mu=true, locoForCars="train_134"),
    "train_137": E(69, cars=["train_139"]),
    "train_138": E(69, isPurchaseSprite=true),
    "train_139": E(69, locoForCars="train_137"),
    "train_140": E(80, loc=end),
    "train_141": E(80, isPurchaseSprite=true),
    "train_142": E(81),
    "train_143": E(82, liv=["train_143"]),
    "train_144": E(82, liv=["train_144"]),
    "train_145": E(83, liv=["train_145"]),
    "train_146": E(83, liv=["train_146"]),
    "train_147": E(84),
    "train_148": E(85),
    "train_149": E(85, isPurchaseSprite=true),
    "train_150": E(86),
    "train_151": E(86, isPurchaseSprite=true),
    "train_152": E(87),
    "train_153": E(87, loc=end),
    "train_154": E(88),
    "train_155": E(88, loc=end),
    "train_156": E(89),
    "train_157": E(89, loc=end),
    "train_158": E(82, liv=["train_158"]),
    "train_159": E(82, isPurchaseSprite=true, liv=["train_158"]),
    "train_160": E(90),
    "train_161": E(90, isPurchaseSprite=true),
    "train_162": E(91),
    "train_163": E(91, isPurchaseSprite=true),
    "train_164": E(92),
    "train_165": E(92, isPurchaseSprite=true),
    "train_166": E(93),
    "train_167": E(93, isPurchaseSprite=true),
    "train_168": E(94, loc=end),
    "train_169": E(94),
    "train_170": E(94, isPurchaseSprite=true),
    "train_171": E(95, loc=end),
    "train_172": E(95),
    "train_173": E(95, isPurchaseSprite=true),
    "train_174": E(96),
    "train_175": E(96, isPurchaseSprite=true),
    "train_176": E(97),
    "train_177": E(97, isPurchaseSprite=true),
    "train_178": E(98),
    "train_179": E(98, isPurchaseSprite=true),
    "train_180": E(99),
    "train_181": E(99, isPurchaseSprite=true),
    "train_182": E(100),
    "train_183": E(100, isPurchaseSprite=true),
    "train_184": E(101),
    "train_185": E(101, isPurchaseSprite=true),
    "train_186": E(102),
    "train_187": E(102),
    "train_188": E(102, isPurchaseSprite=true),
    "train_189": E(103),
    "train_190": E(103, loc=end),
    "train_191": E(104),
    "train_192": E(104, loc=end),
    "train_193": E(105),
    "train_194": E(105, loc=end),
    "train_195": E(105, isPurchaseSprite=true),
    "train_196": E(106, isPurchaseSprite=true),
    "train_197": E(106),
    "train_198": E(107, isPurchaseSprite=true),
    "train_199": E(107),
    "train_200": E(108, isPurchaseSprite=true),
    "train_201": E(108, loc=end),
    "train_202": E(108),
    "train_203": E(109, loc=end),
    "train_204": E(109),
    "train_205": E(110, isPurchaseSprite=true),
    "train_206": E(110),
    "train_207": E(111, isPurchaseSprite=true),
    "train_208": E(111),
    "train_209": E(112, loc=end),
    "train_210": E(112),
    "train_211": E(113),
    "train_212": E(113),
    "train_213": E(113, loc=end),
    "train_214": E(113),
    "train_215": E(113, isPurchaseSprite=true),
    "train_216": E(114, loc=end),
    "train_217": E(114),
    "train_218": E(115, loc=end),
    "train_219": E(115),
    "train_220": E(116),
    "train_221": E(116, isPurchaseSprite=true),
    "train_222": E(117),
    "train_223": E(117, isPurchaseSprite=true),
    "train_224": E(118, loc=end, liv=["train_224", "train_225"]),
    "train_225": E(118, liv=["train_224", "train_225"]),
    "train_226": E(119, loc=end),
    "train_227": E(119),
    "train_228": E(120),
    "train_229": E(120, isPurchaseSprite=true),
    "train_230": E(121),
    "train_231": E(121, isPurchaseSprite=true),
}

ID_TO_GROUPS: dict[int, list[G]] = {
    0: [Loco("train_1", false, tender=same, tenderLength=2), Purchase("train_2")],
    1: [Loco("train_3", frames=4, tender=same), Purchase("train_4")],
    2: [Loco("train_5", frames=4, tender=same), Purchase("train_6")],
    3: [Loco("train_7", frames=4, tender=same), Purchase("train_8")],
    4: [Loco("train_9", frames=4, tender=same), Purchase("train_10")],
    5: [Loco("train_11", frames=4, tender=same), Purchase("train_12")],
    6: [Loco("train_13", frames=4, tender=same), Purchase("train_14")],
    7: [Loco("train_15", frames=4, tender=same), Purchase("train_16")],
    8: [Loco("train_17", frames=4, tender=same), Loco("train_18", reversable=true, frames=4, tender=same), Purchase("train_19")],
    9: [Loco("train_20", frames=4, tender=same), Purchase("train_21")],
    10: [Loco("train_22", frames=4, tender=same), Purchase("train_23")],
    11: [Loco("train_24", frames=4, tender=same), Purchase("train_25")],
    12: [Loco("train_26", frames=4, tender=same), Purchase("train_27")],
    13: [Loco("train_28", frames=4, tender=same), Purchase("train_29")],
    14: [Loco("train_30", loc=back, frames=4, tender=separate),
         Loco("train_31", loc=front, frames=4, tender=separate),
         Loco("train_32", loc=front, frames=4, tender=separate),
         Loco("train_33", loc=front, frames=4, tender=separate),
         Tender("train_34", loc=tender, tender=same),
         Purchase("train_35")],
    15: [Loco("train_36", frames=4, tender=same), Purchase("train_37")],
    16: [Loco("train_38", frames=4, tender=separate),
         Tender("train_39", loc=tender, tender=same),
         Purchase("train_40", liv=["train_38", "train_39", "train_40"])],
    17: [Loco("train_41", loc=back, frames=4, tender=separate),
         Loco("train_42", loc=front, frames=4, tender=separate),
         Loco("train_43", loc=front, frames=4, tender=separate),
         Loco("train_44", loc=front, frames=4, tender=separate),
         Tender("train_45", loc=tender, tender=same),
         Purchase("train_46")],
    16: [Loco("train_47", frames=4, tender=separate),
         Tender("train_48", loc=tender, tender=same),
         Purchase("train_49")],
    18: [Loco("train_50", frames=4, tender=same), Purchase("train_51")],
    19: [Loco("train_52", frames=4, tender=same), Purchase("train_53")],
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


SIMPLE_VEHICLES = {}


def simpleVehicles() -> dict[str, E]:
    global SIMPLE_VEHICLES
    if SIMPLE_VEHICLES != {}:
        return SIMPLE_VEHICLES

    '''
    a simple vehicle is:
    - its id only appears once as a value
    - does not have a dedicated purchase sprite
    - has no liveries
    '''
    # invert the mapping
    invGroups = {}
    for name, e in GROUP_TO_ID.items():
        if not e.isPurchaseSprite and e.liv == []:
            invGroups[e.id] = invGroups.get(e.id, []) + [name]

    simpleNames = [names[0] for id, names in invGroups.items() if len(names) == 1]
    SIMPLE_VEHICLES = {name: GROUP_TO_ID[name] for name in simpleNames}

    return SIMPLE_VEHICLES
