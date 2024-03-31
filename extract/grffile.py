import grf
from grf.sprites import THIS_FILE

from PIL import Image
import numpy as np
from vehicle import Vehicle


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
        self.load()

    def load(self):
        if self.real_sprites != {}:
            return
        self.context = grf.decompile.ParsingContext()
        self.f = open(self.path, 'rb')
        self.g, self.container, self.real_sprites, self.pseudo_sprites = grf.decompile.read(
            self.f, self.context)  # type: ignore

        nameToId = {}
        purchaseGroupToId = {}
        purchaseIds = []
        generators = iter(self.g.generators)
        for s in generators:
            # vehicle defs
            if isinstance(s, grf.Define) and s.feature == grf.TRAIN:
                # print(type(s))
                self.trains[s.id] = Vehicle(s.id, "", s.props)
            elif isinstance(s, grf.DefineMultiple) and "cargo_table" in s.props:
                self.cargo_table = [e.decode("utf-8") for e in s.props["cargo_table"]]

        generators = iter(self.g.generators)
        for s in generators:
            if isinstance(s, grf.DefineStrings) and s.feature == grf.TRAIN:
                # then a DefineStrings with the name
                # print(type(s))
                if s.offset not in self.trains:
                    self.trains[s.offset] = Vehicle()
                name = s.strings[0].decode("utf-8")
                self.trains[s.offset].name = name
                nameToId[name] = s.offset
                s = next(generators)
                if isinstance(s, grf.PyComment):
                    s = next(generators)
                if isinstance(s, grf.Action1) and s.feature == grf.TRAIN and name != "":
                    # then an Action1 with sprite counts
                    # print(f"{type(s)} for {name} set_count={s.set_count} * sprite_count={s.sprite_count}")
                    # get sprites for this group
                    trainId = nameToId[name]
                    set_count = s.set_count
                    sprite_count = s.sprite_count
                    sprites = []
                    # groupName = ""
                    for i in range(set_count):  # sets
                        for j in range(sprite_count):  # sprites per set
                            # get sprite placeholders
                            s = next(generators)
                            if isinstance(s, grf.PyComment):
                                s = next(generators)
                            # print(type(s))
                            assert isinstance(s, grf.decompile.SpritePlaceholder)
                            realSprite = self.real_sprites[s.sprite_id][-1]
                            assert isinstance(realSprite, grf.decompile.RealGraphicsSprite)
                            groupName = self.context.sprites[s.sprite_id][-1]
                            sprites.append({
                                "width": realSprite.width,
                                "height": realSprite.height,
                                "xofs": realSprite.xofs,
                                "yofs": realSprite.yofs,
                                "zoom": realSprite.zoom,
                                "bpp": realSprite.bpp,
                            })
                    # split = groupName.split("_")
                    # purchaseId = int(split[-1])+1
                    # purchaseGroupName = split[0]+"_"+str(purchaseId)

                    # self.trains[trainId].sprites = sprites
                    # self.trains[trainId].purchaseGroupName = purchaseGroupName
                    # self.trains[trainId].groupName = groupName
                    # purchaseGroupToId[purchaseGroupName] = trainId
                    # purchaseIds.append(purchaseId)

        generators = iter(self.g.generators)
        for s in generators:
            if isinstance(s, grf.SpriteSet) and s.sprite_count == 1:
                # purchase sprite
                s = next(generators)
                if isinstance(s, grf.PyComment):
                    s = next(generators)
                assert isinstance(s, grf.decompile.SpritePlaceholder)
                purchaseSprite = self.real_sprites[s.sprite_id][-1]
                assert isinstance(purchaseSprite, grf.decompile.RealGraphicsSprite)
                purchaseGroupName: str = self.context.sprites[s.sprite_id][-1]
                id = int(purchaseGroupName.split("_")[-1])
                if id not in purchaseIds:
                    continue
                trainId = purchaseGroupToId[purchaseGroupName]
                self.trains[trainId].purchaseSprite = {
                    "width": purchaseSprite.width,
                    "height": purchaseSprite.height,
                    "xofs": purchaseSprite.xofs,
                    "yofs": purchaseSprite.yofs,
                    "zoom": purchaseSprite.zoom,
                    "bpp": purchaseSprite.bpp,
                }

        # unwrap single-element list
        for id, vehicle in self.trains.items():
            newprops = {k: v[0]
                        for k, v in vehicle.props.items() if len(v) == 1}
            self.trains[id].props = newprops
        # cleanup
        for id, vehicle in self.trains.items():
            for field in ["refittable_cargo_classes", "non_refittable_cargo_classes"]:
                self.trains[id].props[field] = self.trains[id].toReadableCargoClasses(
                    self.trains[id].props[field])
            for field in ["cargo_allow_refit", "cargo_disallow_refit"]:
                self.trains[id].props[field] = self.trains[id].toReadableCargo(
                    self.trains[id].props[field], self.cargo_table)

    def unload(self):
        self.context = grf.decompile.ParsingContext()
        self.gen = None
        self.container = None
        self.real_sprites = {}
        self.f.close()

    def get_sprite_data(self, sprite_id, num):
        s = self.real_sprites[sprite_id + self.real_offset][num]
        self.f.seek(s.offset)
        data, _ = grf.decompile.decode_sprite(self.f, s, self.container)
        return data

    def get_sprites(self, sprite_id):
        return [
            GRFSprite(self, s.type, s.bpp, sprite_id, i, w=s.width, h=s.height, xofs=s.xofs, yofs=s.yofs, zoom=s.zoom, crop=False)
            for i, s in enumerate(self.real_sprites[sprite_id + self.real_offset])
        ]

    def get_recolour_sprite(self, sprite_id):
        s = self.pseudo_sprites[sprite_id + self.pseudo_offset]
        assert isinstance(s, grf.decompile.RealRemapSprite)
        return np.frombuffer(s.data[1:], dtype=np.uint8)


class GRFSprite(grf.Sprite):

    def __init__(self, file, type, grf_bpp, sprite_id, num, *args, **kw):
        super().__init__(*args, **kw)
        self.file = file
        self.type = type
        self.grf_bpp = grf_bpp
        self.sprite_id = sprite_id
        self.num = num  # index with the same sprite_id

        bpp = grf_bpp
        if self.type & 0x04:
            bpp -= 1

        if bpp == 3:
            self.bpp = grf.BPP_24
        elif bpp == 4:
            self.bpp = grf.BPP_32
        else:
            self.bpp = grf.BPP_8

        self._image = None

    def get_resource_files(self):
        return (self.file, THIS_FILE)

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sprite_id': self.sprite_id,
        }

    def load(self):
        if self._image is not None:
            return

        data = self.file.get_sprite_data(self.sprite_id, self.num)

        a = np.frombuffer(data, dtype=np.uint8)
        assert a.size == self.w * self.h * \
            self.grf_bpp, (a.size, self.w, self.h, self.grf_bpp)

        bpp = self.grf_bpp
        a.shape = (self.h, self.w, bpp)

        mask = None
        if self.type & 0x04 > 0:
            bpp -= 1
            mask = Image.fromarray(a[:, :, -1], mode='P')
            mask.putpalette(grf.PIL_PALETTE)

        if bpp == 3:
            self._image = Image.fromarray(
                a[:, :, :bpp], mode='RGB'), grf.BPP_24
        elif bpp == 4:
            self._image = Image.fromarray(
                a[:, :, :bpp], mode='RGBA'), grf.BPP_32
        else:
            self._image = mask, grf.BPP_8
            mask = None

        # return self._image[0].show()

    def get_image(self):
        self.load()
        return self._image
