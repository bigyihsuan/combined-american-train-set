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

    def ok(self) -> bool:
        return id == -1


front = Loc.Front
back = Loc.Back
tender = Loc.Tender
end = Loc.End

no = TenderSpriteLocation.No
same = TenderSpriteLocation.Same
separate = TenderSpriteLocation.Separate

GROUP_TO_ID: dict[str, E] = {
    # groupnamm: (id, isPurchaseSprite, notes?)
    "train_0": E(),
    "train_1": E(0, tender=same),
    "train_2": E(0, true),
    "train_3": E(1, locoSprites=32*8, tender=same),
    "train_4": E(1, true),
    "train_5": E(2, locoSprites=32*8, tender=same),
    "train_6": E(2, true),
    "train_7": E(3, locoSprites=32*8, tender=same),
    "train_8": E(3, true),
    "train_9": E(4, locoSprites=32*8, tender=same),
    "train_10": E(4, true),
    "train_11": E(5, locoSprites=32*8, tender=same),
    "train_12": E(5, true),
    "train_13": E(6, locoSprites=32*8, tender=same),
    "train_14": E(6, true),
    "train_15": E(7, locoSprites=32*8, tender=same),
    "train_16": E(7, true),
    "train_17": E(8, locoSprites=32*8, tender=same),
    "train_18": E(8, reversable=true, locoSprites=32*8, tender=same),
    "train_19": E(8, true),
    "train_20": E(9, locoSprites=32*8, tender=same),
    "train_21": E(9, true),
    "train_22": E(10, locoSprites=32*8, tender=same),
    "train_23": E(10, true),
    "train_24": E(11, locoSprites=32*8, tender=same),
    "train_25": E(11, true),
    "train_26": E(12, locoSprites=32*8, tender=same),
    "train_27": E(12, true),
    "train_28": E(13, locoSprites=32*8, tender=same),
    "train_29": E(13, true),
    "train_30": E(14, loc=back, locoSprites=32*8, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_31": E(14, loc=front, locoSprites=32*8, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_32": E(14, loc=front, locoSprites=32*8, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_33": E(14, loc=front, locoSprites=32*8, tender=separate, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_34": E(14, loc=tender, tender=same, parts=["train_30", "train_31", "train_32", "train_33", "train_34"]),
    "train_35": E(14, true),
    "train_36": E(15, locoSprites=32*8, tender=same),
    "train_37": E(15, true),
    "train_38": E(16, liv=["train_38", "train_39", "train_40"], locoSprites=32*8, tender=separate, parts=["train_38", "train_39"]),
    "train_39": E(16, loc=tender, liv=["train_38", "train_39", "train_40"], tender=same, parts=["train_38", "train_39"]),
    "train_40": E(16, true, liv=["train_38", "train_39", "train_40"]),
    "train_41": E(17, loc=back, locoSprites=32*8, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_42": E(17, loc=front, locoSprites=32*8, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_43": E(17, loc=front, locoSprites=32*8, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_44": E(17, loc=front, locoSprites=32*8, tender=separate, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_45": E(17, loc=tender, tender=same, parts=["train_41", "train_42", "train_43", "train_44", "train_45"]),
    "train_46": E(17, true),
    "train_47": E(16, liv=["train_47", "train_48", "train_49"], alt=["train_70"], locoSprites=32*8, tender=separate, parts=["train_47", "train_48"]),
    "train_48": E(16, loc=tender, liv=["train_47", "train_48", "train_49"], alt=["train_70"], tender=same, parts=["train_47", "train_48"]),
    "train_49": E(16, true, liv=["train_47", "train_48", "train_49"], alt=["train_70"]),
    "train_50": E(18, locoSprites=32*8, tender=same),
    "train_51": E(18, true),
    "train_52": E(19, locoSprites=32*8, tender=same),
    "train_53": E(19, true),
    "train_54": E(20, bUnitSprites=8),
    "train_55": E(21, reversable=true, locoSprites=16*8, bUnitSprites=16*8),
    "train_56": E(21, true),
    "train_57": E(22, reversable=true),
    "train_58": E(22, true),
    "train_59": E(23, reversable=true, locoSprites=16*8, bUnitSprites=16*8),
    "train_60": E(23, true),
    "train_61": E(24, reversable=true),
    "train_62": E(24, true),
    "train_63": E(25),
    "train_64": E(26, reversable=true),
    "train_65": E(26, true),
    "train_66": E(27),
    "train_67": E(28, length=10),  # emd centennial, 40px = 10/8tl
    "train_68": E(28, true, length=10),  # emd centennial, 40px = 10/8tl
    "train_69": E(29),
    "train_70": E(30),
    "train_71": E(30, true),
    "train_72": E(31),
    "train_73": E(31, true),
    "train_74": E(32, reversable=true, bUnitSprites=8),
    "train_75": E(32, true),
    "train_76": E(33),
    "train_77": E(34, liv=["train_77"]),
    "train_78": E(34, liv=["train_78"]),
    "train_79": E(34, true),
    "train_80": E(35, reversable=true),
    "train_81": E(35, true),
    "train_82": E(36, bUnitSprites=8),
    "train_83": E(37, reversable=true, bUnitSprites=8),
    "train_84": E(37, true),
    "train_85": E(38, reversable=true),
    "train_86": E(38, true),
    "train_87": E(39),
    "train_88": E(40, reversable=true),
    "train_89": E(40, true),
    "train_90": E(41),
    "train_91": E(42),
    "train_92": E(43),
    "train_93": E(44),
    "train_94": E(45),
    "train_95": E(46),
    "train_96": E(47, reversable=true, bUnitSprites=8),
    "train_97": E(47, true),
    "train_98": E(48),
    "train_99": E(49, reversable=true),
    "train_100": E(49, true),
    "train_101": E(50, reversable=true),
    "train_102": E(50, true),
    "train_103": E(51, reversable=true),
    "train_104": E(51, true),
    "train_105": E(52, parts=["train_105", "train_105"], bUnitSprites=8),
    "train_106": E(52, true),
    "train_107": E(53),
    "train_108": E(54),
    "train_109": E(55, reversable=true),
    "train_110": E(55, true),
    "train_111": E(56, reversable=true),
    "train_112": E(56, true),
    "train_113": E(57, reversable=true),
    "train_114": E(57, true),
    "train_115": E(58),
    "train_116": E(59),
    "train_117": E(60),
    "train_118": E(61, locoSprites=4),
    "train_119": E(62, reversable=true, parts=["train_119", "train_119", "train_119", "train_119"], bUnitSprites=8, locoForCars="train_119"),
    "train_120": E(62, true),
    "train_121": E(63, parts=["train_121", "train_121"], bUnitSprites=8, cars=["train_123", "train_123"]),
    "train_122": E(63, true),
    "train_123": E(63, mu=true, parts=["train_121", "train_121"], cars=["train_123", "train_123"], locoForCars="train_121"),
    "train_124": E(64, parts=["train_124", "train_124"], bUnitSprites=8, cars=["train_126", "train_126"]),
    "train_125": E(64, true),
    "train_126": E(64, mu=true, cars=["train_126", "train_126"], locoForCars="train_124"),
    "train_127": E(65),
    "train_128": E(66, cars=["train_130", "train_130"]),
    "train_129": E(66, true),
    "train_130": E(66, locoForCars="train_128"),
    "train_131": E(67, mu=true, cars=["train_133"]),
    "train_132": E(67, true),
    "train_133": E(67, locoForCars="train_131"),
    "train_134": E(68, parts=["train_134", "train_134"], bUnitSprites=8, cars=["train_136", "train_136"]),
    "train_135": E(68, true),
    "train_136": E(68, mu=true, locoForCars="train_134"),
    "train_137": E(69, cars=["train_139"]),
    "train_138": E(69, true),
    "train_139": E(69, locoForCars="train_137"),
    "train_140": E(80, loc=end),
    "train_141": E(80, true),
    "train_142": E(81),
    "train_143": E(82, liv=["train_143"]),
    "train_144": E(82, liv=["train_144"]),
    "train_145": E(83, liv=["train_145"]),
    "train_146": E(83, liv=["train_146"]),
    "train_147": E(84),
    "train_148": E(85),
    "train_149": E(85, true),
    "train_150": E(86),
    "train_151": E(86, true),
    "train_152": E(87),
    "train_153": E(87, loc=end),
    "train_154": E(88),
    "train_155": E(88, loc=end),
    "train_156": E(89),
    "train_157": E(89, loc=end),
    "train_158": E(82, liv=["train_158"]),
    "train_159": E(82, true, liv=["train_158"]),
    "train_160": E(90),
    "train_161": E(90, true),
    "train_162": E(91),
    "train_163": E(91, true),
    "train_164": E(92),
    "train_165": E(92, true),
    "train_166": E(93),
    "train_167": E(93, true),
    "train_168": E(94, loc=end),
    "train_169": E(94),
    "train_170": E(94, true),
    "train_171": E(95, loc=end),
    "train_172": E(95),
    "train_173": E(95, true),
    "train_174": E(96),
    "train_175": E(96, true),
    "train_176": E(97),
    "train_177": E(97, true),
    "train_178": E(98),
    "train_179": E(98, true),
    "train_180": E(99),
    "train_181": E(99, true),
    "train_182": E(100),
    "train_183": E(100, true),
    "train_184": E(101),
    "train_185": E(101, true),
    "train_186": E(102),
    "train_187": E(102),
    "train_188": E(102, true),
    "train_189": E(103),
    "train_190": E(103, loc=end),
    "train_191": E(104),
    "train_192": E(104, loc=end),
    "train_193": E(105),
    "train_194": E(105, loc=end),
    "train_195": E(105, true),
    "train_196": E(106, true),
    "train_197": E(106),
    "train_198": E(107, true),
    "train_199": E(107),
    "train_200": E(108, true),
    "train_201": E(108, loc=end),
    "train_202": E(108),
    "train_203": E(109, loc=end),
    "train_204": E(109),
    "train_205": E(110, true),
    "train_206": E(110),
    "train_207": E(111, true),
    "train_208": E(111),
    "train_209": E(112, loc=end),
    "train_210": E(112),
    "train_211": E(113),
    "train_212": E(113),
    "train_213": E(113, loc=end),
    "train_214": E(113),
    "train_215": E(113, true),
    "train_216": E(114, loc=end),
    "train_217": E(114),
    "train_218": E(115, loc=end),
    "train_219": E(115),
    "train_220": E(116),
    "train_221": E(116, true),
    "train_222": E(117),
    "train_223": E(117, true),
    "train_224": E(118, loc=end, liv=["train_224", "train_225"]),
    "train_225": E(118, liv=["train_224", "train_225"]),
    "train_226": E(119, loc=end),
    "train_227": E(119),
    "train_228": E(120),
    "train_229": E(120, true),
    "train_230": E(121),
    "train_231": E(121, true),
}


def initGroups():
    for id in GROUP_TO_ID:
        e = GROUP_TO_ID[id]
        if e.isPurchaseSprite:
            e.loc = Loc.Purchase


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
