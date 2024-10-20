from collections import defaultdict
import grf

from shared.vehicle import Sprite, SpriteGroup, Vehicle, VehicleProps


class GRFFile(grf.LoadedResourceFile):
    def __init__(self, path, *, real_offset=1, pseudo_offset=0):
        self.path = path
        self.real_sprites = {}
        self.pseudo_sprites = {}
        self.real_offset = real_offset
        self.pseudo_offset = pseudo_offset
        self.trains: dict[int, Vehicle] = {}
        self.cargo_table: list[str] = []
        self.context = grf.decompile.ParsingContext()
        self.sprites: list[SpriteGroup] = []
        self.load()

    def load(self):
        if self.real_sprites != {}:
            return
        self.context = grf.decompile.ParsingContext()
        self.f = open(self.path, 'rb')
        self.g, self.container, self.real_sprites, self.pseudo_sprites = grf.decompile.read(
            self.f, self.context)  # type: ignore

        generators = iter(self.g.generators)
        for s in generators:
            # vehicle defs
            if isinstance(s, grf.Define) and s.feature == grf.TRAIN:
                # print(type(s))
                # convert props to VehicleProps
                propsDict = {k: v[0] for k, v in s.props.items()}
                introDate = propsDict["introduction_date"]
                propsDict["introduction_date"] = [introDate.year, introDate.month, introDate.day]
                if "shorten_by" in propsDict:
                    propsDict["length"] = 8 - propsDict["shorten_by"]
                    del propsDict["shorten_by"]
                props = VehicleProps(**propsDict)
                self.trains[s.id] = Vehicle(s.id, "", props)
            # cargo table
            if isinstance(s, grf.DefineMultiple) and "cargo_table" in s.props:
                self.cargo_table = [e.decode("utf-8") for e in s.props["cargo_table"]]

        generators = iter(self.g.generators)
        for s in generators:
            if isinstance(s, grf.DefineStrings) and s.feature == grf.TRAIN:
                if s.offset in self.trains:
                    name: bytes = s.strings[-1]
                    self.trains[s.offset]._name = name.decode()

        # get sprite gorup names
        groups = [(group, sprite_id) for sprite_id in self.context.sprites if (
            group := self.context.sprites[sprite_id][-1]) is not None]
        # map group names to sprite ids
        groupToSpriteIds = defaultdict(list)
        for (group, sprite_id) in groups:
            groupToSpriteIds[group].append(sprite_id)

        # get the real sprites for each group
        real_sprites: list[SpriteGroup] = []
        for (group, ids) in groupToSpriteIds.items():
            rgss = [self.real_sprites[id][-1] for id in ids]
            sprites: list[Sprite] = []

            # adapted from:
            # https://github.com/citymania-org/grf-py/blob/965f222d7dbd5641db86ac51b4e1e9343f4f1c75/grf/decompile.py#L1369-L1418
            # i do not have the brainpower to understand this right now
            PADDING = 5
            N = 8
            w = 0
            h = 0
            line_ofs = []
            # get line offsets for yofs
            for i in range(0, len(rgss), N):
                lw = sum(s.width for s in rgss[i: i + N]) + PADDING * 2 * N
                lh = PADDING * 2 + max(s.height for s in rgss[i: i + N])
                w = max(w, lw)
                line_ofs.append(h)
                h += lh

            xofs = 0
            for (i, sprite) in enumerate(rgss):
                yofs = PADDING + line_ofs[i // N]
                if i % N == 0:
                    xofs = PADDING
                x = xofs
                y = yofs
                sprites.append(Sprite(group, x, y, sprite.width, sprite.height,
                                      xofs=sprite.xofs, yofs=sprite.yofs, zoom=sprite.zoom, bpp=sprite.bpp))
                xofs += sprite.width + 2 * PADDING
            real_sprites.append(SpriteGroup(file=group, real_sprites=sprites))
        self.sprites = real_sprites
