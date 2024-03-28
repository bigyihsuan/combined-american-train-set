import csv
import json
from collections import defaultdict
import pprint
from typing import Any

from PIL import Image, ImageDraw, ImageFont
import numpy as np

import grf
from grf.sprites import THIS_FILE


class GRFFile(grf.LoadedResourceFile):
    def __init__(self, path, *, real_offset=1, pseudo_offset=0):
        self.path = path
        self.real_sprites = None
        self.pseudo_sprites = None
        self.real_offset = real_offset
        self.pseudo_offset = pseudo_offset
        self.trains = {}
        self.load()

    def load(self):
        if self.real_sprites is not None:
            return
        print(f'Decompiling {self.path}...')
        self.context = grf.decompile.ParsingContext()
        self.f = open(self.path, 'rb')
        self.g, self.container, self.real_sprites = grf.decompile.read(  # type: ignore
            self.f, self.context)

        for s in self.g.generators:
            if isinstance(s, grf.Define):
                self.trains[s.id] = s.props
        for s in self.g.generators:
            if isinstance(s, grf.DefineStrings) and s.feature == grf.TRAIN:
                self.trains[s.offset]["name"] = s.strings

        for id, props in self.trains.items():
            newprops = {k: v[0] for k, v in props.items()}
            self.trains[id] = newprops

    def unload(self):
        self.context = None
        self.gen = None
        self.container = None
        self.real_sprites = None
        self.f.close()

    def get_sprite_data(self, sprite_id, num):
        s = self.real_sprites[sprite_id + self.real_offset][num]
        self.f.seek(s.offset)
        data, _ = grf.decompile.decode_sprite(self.f, s, self.container)
        return data

    def get_sprites(self, sprite_id):
        return [
            GRFSprite(self, s.type, s.bpp, sprite_id, i, w=s.width,
                      h=s.height, xofs=s.xofs, yofs=s.yofs, zoom=s.zoom, crop=False)
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


nars = GRFFile("./decompiled/newnars.grf")
with open("./vehicle-stats2.csv", "w") as vehicleStatsCsv, open("./vehicle-stats2.json", "w") as vehicleStatsJson:
    FIELDNAMES = ['id', 'name', 'introduction_days_since_1920', 'introduction_date', 'reliability_decay', 'vehicle_life', 'model_life', 'track_type', 'climates_available', 'loading_speed', 'max_speed', 'power', 'weight_low', 'weight_high', 'tractive_effort_coefficient', 'cost_factor', 'running_cost_factor', 'shorten_by', 'visual_effect_and_powered', 'engine_class', 'running_cost_base', 'sprite_id', 'dual_headed',
                  'cargo_capacity', 'default_cargo_type', 'ai_special_flag', 'ai_engine_rank', 'sort_purchase_list', 'extra_power_per_wagon', 'refit_cost', 'refittable_cargo_types''cb_flags', 'air_drag_coefficient', 'extra_weight_per_wagon', 'bitmask_vehicle_info''retire_early', 'misc_flags', 'refittable_cargo_classes', 'non_refittable_cargo_classes', 'cargo_age_period', 'cargo_allow_refit', 'cargo_disallow_refit',
                  'retire_early', 'bitmask_vehicle_info', 'cb_flags', 'refittable_cargo_types']
    statsWriter = csv.DictWriter(vehicleStatsCsv, FIELDNAMES)
    statsWriter.writeheader()
    rows = []
    for id, train in nars.trains.items():
        row = train.copy()
        row["id"] = id
        for k, v in row.items():
            if isinstance(v, bytes):
                row[k] = v.decode("utf-8")
        rows.append(row)

    rows.sort(key=lambda row: row["id"])
    statsWriter.writerows(rows)
    json.dump(rows, vehicleStatsJson, sort_keys=True, default=str, indent=4)
