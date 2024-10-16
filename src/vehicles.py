
import dataclasses
import os
from typing import Any

import yaml
import shared.vehicle as V

default_props = dataclasses.asdict(V.VehicleProps.default())


def load_yaml(root: str, name: str) -> dict[str, Any]:
    loco_yaml = os.path.join(root, f"{name}.yaml")
    print(loco_yaml)

    with open(loco_yaml, "r") as loco_yaml_file:
        loco_props: dict[str, Any] = yaml.safe_load(loco_yaml_file)
        # fill in default values
        for k, default in default_props.items():
            if k not in loco_props["props"]:
                loco_props["props"][k] = default
            # add name and id to the loco props
            loco_props["props"]["id"] = loco_props["_id"]
            loco_props["props"]["name"] = loco_props["_name"]
        return loco_props


def make_livestock_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_single_hopper(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_two_bay_hopper(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_large_hopper(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_woodchip_hopper(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_covered_hopper(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_gondola(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_40_gondola(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_50_gondola(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_steel_coil_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_flat_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_50_flat_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_container_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_double_stack_intermodal(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_centerbeam_flat_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_autorack(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_tank_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_40_tank_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_60_tank_car_oil(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_60_tank_car_cc(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_caboose_short(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_caboose_long(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_passenger_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_heavyweight_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_lightweight_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_bilevel_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_superliner_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_highspeed_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_mail_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_heavyweight_mail_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_lightweight_mail_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_highspeed_mail_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_cabbage_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_express_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_boxcar(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_40_boxcar(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_50_boxcar(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_hicube_boxcar(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_reefer(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_40_reefer(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_50_reefer(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_cattle_car(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emc_e3(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_ft(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sw1200(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_fp9(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_gp9(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sd9(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sw1500(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sd45(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_centennial(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sd402(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_gp382(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_f40ph(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_gp60(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_sd70mac(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_f59phi(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alco_s2(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alco_pa(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alco_fa(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alco_rs3(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alco_century(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_u25b(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_u30c(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_c367(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_c408(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_c449w(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_p42dc_genesis(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_evolution(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_baldwin_rf16(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_fm_train_master(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_hybrid_switcher(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emc_doodlebug(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_budd_rdc(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_emd_aerotrain(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_uac_turbotrain(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_rtl_turboliner(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_steeplecab(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_baldwin_boxcab(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_alcoge_boxcab(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_pennsylvania_gg1(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_virginian_elc(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_gmd_sw1200mg(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_ge_e60c(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_aseaemd_aem7(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_gmd_gf6c(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_siemens_acs64(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_bombardier_acela(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_electric_interurban(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_budd_metroliner(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_bombardier_emu(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_nippon_sharyo_emu(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_420_norris(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_440_american(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_462_pacific(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_2102_santa_fe(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_482_mountain(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_284_berkshire(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_2882_mallet(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_2104_selkirk(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_464_hudson(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_4664_challenger(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_444_jubilee(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_4444_duplex(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_260_mogul(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_280_consolidation(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_460_tenwheeler(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_440_express(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_280_consolidation_ii(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_442_atlantic(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_464_baltic(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_060_switcher(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


def make_282_mikado(root: str, name: str):
    loco_props = load_yaml(root, name)
    pass


MAKE_VEHICLE = {
    "100-livestock_car": make_livestock_car,
    "101-single_hopper": make_single_hopper,
    "102-two_bay_hopper": make_two_bay_hopper,
    "103-large_hopper": make_large_hopper,
    "104-woodchip_hopper": make_woodchip_hopper,
    "105-covered_hopper": make_covered_hopper,
    "106-gondola": make_gondola,
    "107-40_gondola": make_40_gondola,
    "108-50_gondola": make_50_gondola,
    "109-steel_coil_car": make_steel_coil_car,
    "110-flat_car": make_flat_car,
    "111-50_flat_car": make_50_flat_car,
    "112-container_car": make_container_car,
    "113-double_stack_intermodal": make_double_stack_intermodal,
    "114-centerbeam_flat_car": make_centerbeam_flat_car,
    "115-autorack": make_autorack,
    "116-tank_car": make_tank_car,
    "117-40_tank_car": make_40_tank_car,
    "118-60_tank_car": make_60_tank_car_cc,
    "119-60_tank_car": make_60_tank_car_oil,
    "120-caboose": make_caboose_short,
    "121-caboose": make_caboose_long,
    "80-passenger_car": make_passenger_car,
    "81-heavyweight_car": make_heavyweight_car,
    "82-lightweight_car": make_lightweight_car,
    "83-bilevel_car": make_bilevel_car,
    "84-superliner_car": make_superliner_car,
    "85-highspeed_car": make_highspeed_car,
    "86-mail_car": make_mail_car,
    "87-heavyweight_mail_car": make_heavyweight_mail_car,
    "88-lightweight_mail_car": make_lightweight_mail_car,
    "89-highspeed_mail_car": make_highspeed_mail_car,
    "90-cabbage_car": make_cabbage_car,
    "91-express_car": make_express_car,
    "92-boxcar": make_boxcar,
    "93-40_boxcar": make_40_boxcar,
    "94-50_boxcar": make_50_boxcar,
    "95-hicube_boxcar": make_hicube_boxcar,
    "96-reefer": make_reefer,
    "97-40_reefer": make_40_reefer,
    "98-50_reefer": make_50_reefer,
    "99-cattle_car": make_cattle_car,
    "20-emc_e3": make_emc_e3,
    "21-emd_ft": make_emd_ft,
    "22-emd_sw1200": make_emd_sw1200,
    "23-emd_fp9": make_emd_fp9,
    "24-emd_gp9": make_emd_gp9,
    "25-emd_sd9": make_emd_sd9,
    "26-emd_sw1500": make_emd_sw1500,
    "27-emd_sd45": make_emd_sd45,
    "28-emd_centennial": make_emd_centennial,
    "29-emd_sd402": make_emd_sd402,
    "30-emd_gp382": make_emd_gp382,
    "31-emd_f40ph": make_emd_f40ph,
    "32-emd_gp60": make_emd_gp60,
    "33-emd_sd70mac": make_emd_sd70mac,
    "34-emd_f59phi": make_emd_f59phi,
    "35-alco_s2": make_alco_s2,
    "36-alco_pa": make_alco_pa,
    "37-alco_fa": make_alco_fa,
    "38-alco_rs3": make_alco_rs3,
    "39-alco_century": make_alco_century,
    "40-ge_u25b": make_ge_u25b,
    "41-ge_u30c": make_ge_u30c,
    "42-ge_c367": make_ge_c367,
    "43-ge_c408": make_ge_c408,
    "44-ge_c449w": make_ge_c449w,
    "45-ge_p42dc_genesis": make_ge_p42dc_genesis,
    "46-ge_evolution": make_ge_evolution,
    "47-baldwin_rf16": make_baldwin_rf16,
    "48-fm_train_master": make_fm_train_master,
    "49-hybrid_switcher": make_hybrid_switcher,
    "60-emc_doodlebug": make_emc_doodlebug,
    "61-budd_rdc": make_budd_rdc,
    "62-emd_aerotrain": make_emd_aerotrain,
    "63-uac_turbotrain": make_uac_turbotrain,
    "64-rtl_turboliner": make_rtl_turboliner,
    "50-ge_steeplecab": make_ge_steeplecab,
    "51-baldwin_boxcab": make_baldwin_boxcab,
    "52-alcoge_boxcab": make_alcoge_boxcab,
    "53-pennsylvania_gg1": make_pennsylvania_gg1,
    "54-virginian_elc": make_virginian_elc,
    "55-gmd_sw1200mg": make_gmd_sw1200mg,
    "56-ge_e60c": make_ge_e60c,
    "57-aseaemd_aem7": make_aseaemd_aem7,
    "58-gmd_gf6c": make_gmd_gf6c,
    "59-siemens_acs64": make_siemens_acs64,
    "68-bombardier_acela": make_bombardier_acela,
    "65-electric_interurban": make_electric_interurban,
    "66-budd_metroliner": make_budd_metroliner,
    "67-bombardier_emu": make_bombardier_emu,
    "69-nippon_sharyo_emu": make_nippon_sharyo_emu,
    "0-420_norris": make_420_norris,
    "1-440_american": make_440_american,
    "10-462_pacific": make_462_pacific,
    "11-2102_santa_fe": make_2102_santa_fe,
    "12-482_mountain": make_482_mountain,
    "13-284_berkshire": make_284_berkshire,
    "14-2882_mallet": make_2882_mallet,
    "15-2104_selkirk": make_2104_selkirk,
    "16-464_hudson": make_464_hudson,
    "17-4664_challenger": make_4664_challenger,
    "18-444_jubilee": make_444_jubilee,
    "19-4444_duplex": make_4444_duplex,
    "2-260_mogul": make_260_mogul,
    "3-280_consolidation": make_280_consolidation,
    "4-460_tenwheeler": make_460_tenwheeler,
    "5-440_express": make_440_express,
    "6-280_consolidation_ii": make_280_consolidation_ii,
    "7-442_atlantic": make_442_atlantic,
    "70-464_baltic": make_464_baltic,
    "8-060_switcher": make_060_switcher,
    "9-282_mikado": make_282_mikado,
}


def make_vehicle(root: str, name: str):
    MAKE_VEHICLE[name](root, name)
