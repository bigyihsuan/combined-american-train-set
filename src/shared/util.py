from typing import TypeVar
import grf

T = TypeVar("T")


def chunk(l: list[T], n: int) -> list[list[T]]:
    return [l[i:i + n] for i in range(0, len(l), n)]


def animatedVehicleSwitch(Switch: type[grf.Switch], engineLayouts, frameCount=1) -> grf.Switch:
    return Switch(
        feature=grf.TRAIN,
        code=f"motion_counter % {frameCount}",
        ranges={i: row for i, row in enumerate(engineLayouts)},
        default=engineLayouts[0]
    )


def reversableVehicleSwitch(
        Switch: type[grf.Switch],
        forward,
        reverse,
        default=None,
        related_scope=False) -> grf.Switch:
    return Switch(
        feature=grf.TRAIN,
        code="vehicle_is_reversed",
        ranges={
            0: forward,
            1: reverse,
        },
        default=default if default is not None else forward,
        # also check the other cars of the consist. vehicle_is_reversed by default only checks the first car.
        related_scope=related_scope
    )
