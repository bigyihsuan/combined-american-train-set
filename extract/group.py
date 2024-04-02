from dataclasses import dataclass, field
from enum import Enum, auto

false = False
true = True


class K(Enum):
    Full = auto()
    Front = auto()
    Back = auto()
    Tender = auto()
    End = auto()

    def __repr__(self) -> str:
        if self == K.Full:
            return "Full"
        elif self == K.Front:
            return "Front"
        elif self == K.Back:
            return "Back"
        elif self == K.Tender:
            return "Tender"
        elif self == K.End:
            return "End"
        else:
            return "K.INVALID"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class E:
    id: int = -1
    isPurchaseSprite: bool = False
    reversed: bool = False
    loc: K = K.Full
    liv: list[int] = field(default_factory=list)
    alt: list[int] = field(default_factory=list)
    mu: bool = False  # whether this group is a car for an MU.

    def ok(self) -> bool:
        return id == -1


front = K.Front
back = K.Back
tender = K.Tender
end = K.End
reversed = true

GROUP_TO_ID: dict[str, E] = {
    # groupnamm: (id, isPurchaseSprite, notes?)
    "train_0": E(),
    "train_1": E(0),
    "train_2": E(0, true),
    "train_3": E(1),
    "train_4": E(1, true),
    "train_5": E(2),
    "train_6": E(2, true),
    "train_7": E(3),
    "train_8": E(3, true),
    "train_9": E(4),
    "train_10": E(4, true),
    "train_11": E(5),
    "train_12": E(5, true),
    "train_13": E(6),
    "train_14": E(6, true),
    "train_15": E(7),
    "train_16": E(7, true),
    "train_17": E(8),
    "train_18": E(8, reversed),
    "train_19": E(8, true),
    "train_20": E(9),
    "train_21": E(9, true),
    "train_22": E(10),
    "train_23": E(10, true),
    "train_24": E(11),
    "train_25": E(11, true),
    "train_26": E(12),
    "train_27": E(12, true),
    "train_28": E(13),
    "train_29": E(13, true),
    "train_30": E(14, loc=back),
    "train_31": E(14, loc=front),
    "train_32": E(14, loc=front),
    "train_33": E(14, loc=front),
    "train_34": E(14, loc=tender),
    "train_35": E(14, true),
    "train_36": E(15),
    "train_37": E(15, true),
    "train_38": E(16, liv=[38, 39, 40]),
    "train_39": E(16, loc=tender, liv=[38, 39, 40]),
    "train_40": E(16, true, liv=[38, 39, 40]),
    "train_41": E(17, loc=back),
    "train_42": E(17, loc=front),
    "train_43": E(17, loc=front),
    "train_44": E(17, loc=front),
    "train_45": E(17, loc=tender),
    "train_46": E(17, true),
    "train_47": E(16, liv=[47, 48, 49], alt=[70]),
    "train_48": E(16, loc=tender, liv=[47, 48, 49], alt=[70]),
    "train_49": E(16, true, liv=[47, 48, 49], alt=[70]),
    "train_50": E(18),
    "train_51": E(18, true),
    "train_52": E(19),
    "train_53": E(19, true),
    "train_54": E(20),
    "train_55": E(21),
    "train_56": E(21, true),
    "train_57": E(22),
    "train_58": E(22, true),
    "train_59": E(23),
    "train_60": E(23, true),
    "train_61": E(24),
    "train_62": E(24, true),
    "train_63": E(25),
    "train_64": E(26),
    "train_65": E(26, true),
    "train_66": E(27),
    "train_67": E(28),
    "train_68": E(28, true),
    "train_69": E(29),
    "train_70": E(30),
    "train_71": E(30, true),
    "train_72": E(31),
    "train_73": E(31, true),
    "train_74": E(32),
    "train_75": E(32, true),
    "train_76": E(33),
    "train_77": E(34, liv=[77]),
    "train_78": E(34, liv=[78]),
    "train_79": E(34, true),
    "train_80": E(35),
    "train_81": E(35),
    "train_82": E(36, true),
    "train_83": E(37),
    "train_84": E(37, true),
    "train_85": E(38),
    "train_86": E(38, true),
    "train_87": E(39),
    "train_88": E(40),
    "train_89": E(40, true),
    "train_90": E(41),
    "train_91": E(42),
    "train_92": E(43),
    "train_93": E(44),
    "train_94": E(45),
    "train_95": E(46),
    "train_96": E(47),
    "train_97": E(47, true),
    "train_98": E(48),
    "train_99": E(49),
    "train_100": E(49, true),
    "train_101": E(50),
    "train_102": E(50, true),
    "train_103": E(51),
    "train_104": E(51, true),
    "train_105": E(52),
    "train_106": E(52, true),
    "train_107": E(53),
    "train_108": E(54),
    "train_109": E(55),
    "train_110": E(55, true),
    "train_111": E(56),
    "train_112": E(56, true),
    "train_113": E(57),
    "train_114": E(57, true),
    "train_115": E(58),
    "train_116": E(59),
    "train_117": E(60),
    "train_118": E(61),
    "train_119": E(62),
    "train_120": E(62, true),
    "train_121": E(63),
    "train_122": E(63, true),
    "train_123": E(63, mu=true),
    "train_124": E(64),
    "train_125": E(64, true),
    "train_126": E(64, mu=true),
    "train_127": E(65),
    "train_128": E(66),
    "train_129": E(66, true),
    "train_130": E(66, mu=true),
    "train_131": E(67),
    "train_132": E(67, true),
    "train_133": E(67, mu=true),
    "train_134": E(68),
    "train_135": E(68, true),
    "train_136": E(68, mu=true),
    "train_137": E(69),
    "train_138": E(69, true),
    "train_139": E(69, mu=true),
    "train_140": E(80),
    "train_141": E(80, true),
    "train_142": E(81),
    "train_143": E(82, liv=[143]),
    "train_144": E(82, liv=[144]),
    "train_145": E(83, liv=[145]),
    "train_146": E(83, liv=[146]),
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
    "train_158": E(82, liv=[158]),
    "train_159": E(82, true, liv=[158]),
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
    "train_224": E(118, loc=end, liv=[224, 225]),
    "train_225": E(118, liv=[224, 225]),
    "train_226": E(119, loc=end),
    "train_227": E(119),
    "train_228": E(120),
    "train_229": E(120, true),
    "train_230": E(121),
    "train_231": E(121, true),
}

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
