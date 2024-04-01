from collections import defaultdict
import json
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
        self.sprites = {}
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
                self.trains[s.id] = Vehicle(s.id, "", s.props)
            if isinstance(s, grf.DefineMultiple) and "cargo_table" in s.props:
                self.cargo_table = [e.decode("utf-8") for e in s.props["cargo_table"]]

        generators = iter(self.g.generators)
        for s in generators:
            if isinstance(s, grf.DefineStrings) and s.feature == grf.TRAIN:
                if s.offset in self.trains:
                    name: bytes = s.strings[-1]
                    self.trains[s.offset].name = name.decode()

        # unwrap single-element list
        for id, vehicle in self.trains.items():
            newprops = {k: v[0]
                        for k, v in vehicle.props.items() if len(v) == 1}
            self.trains[id].props = newprops
        # cleanup
        for id, vehicle in self.trains.items():
            for field in ["refittable_cargo_classes", "non_refittable_cargo_classes"]:
                self.trains[id].props[field] = Vehicle.toReadableCargoClasses(self.trains[id].props[field])
            for field in ["cargo_allow_refit", "cargo_disallow_refit"]:
                self.trains[id].props[field] = Vehicle.toReadableCargo(self.trains[id].props[field], self.cargo_table)
            self.trains[id].props["cb_flags"] = Vehicle.toReadableCallback(self.trains[id].props["cb_flags"])
            self.trains[id].props["misc_flags"] = Vehicle.toReadableFlag(self.trains[id].props["misc_flags"])

        groups = [(group, sprite_id) for sprite_id in self.context.sprites if (
            group := self.context.sprites[sprite_id][-1]) is not None]
        groupToSpriteIds = defaultdict(list)
        for (group, sprite_id) in groups:
            groupToSpriteIds[group].append(sprite_id)

        real_sprites = []
        for (group, ids) in groupToSpriteIds.items():
            rgss = [self.real_sprites[id][-1] for id in ids]
            sprites = [
                {"width": sprite.width, "height": sprite.height, "xofs": sprite.xofs, "yofs": sprite.yofs,
                 "zoom": sprite.zoom, "bpp": sprite.bpp} for sprite in rgss]
            real_sprites.append({"group": group, "sprites": sprites})

        self.sprites = real_sprites

        # traverse the DAG of action3,2,1,0s
        # action3s = [sprite for nfoLine in self.pseudo_sprites if isinstance(
        #     (sprite := self.pseudo_sprites[nfoLine]), grf.actions.Action3)]
        # action2s = [
        #     sprite for nfoLine in self.pseudo_sprites
        #     if
        #     isinstance(
        #         (sprite := self.pseudo_sprites[nfoLine]),
        #         (grf.actions.Switch, grf.actions.RandomSwitch, grf.actions.GenericSpriteLayout))]

        # for action in action3s:
        #     assert isinstance(action, grf.actions.Action3)
        #     # print(action.ids, action.maps)
        #     if 0xFF in action.maps:
        #         ref = action.maps[255]
        #         assert isinstance(ref, grf.Ref)
        #         referencedActions = [action for action in action2s if action.ref_id == ref.ref_id]
        #         for a in referencedActions:
        #             print(type(a), a.__dict__)

        # for action in action2s:
        #     print(type(action), action.__dict__)


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
