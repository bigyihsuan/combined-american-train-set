from typing import TypeVar
import grf

T = TypeVar("T")


def chunk(l: list[T], n: int) -> list[list[T]]:
    '''
    Chunks a list into some number of chunks of length `n`.
    The final chunk may be shorter than length `n`.
    '''
    return [l[i:i + n] for i in range(0, len(l), n)]


def animated_vehicle(Switch: type[grf.Switch], engine_layouts, frame_count=1) -> grf.Switch:
    '''
    A Switch for animating a vehicle.
    '''
    return Switch(
        feature=grf.TRAIN,
        code=f"motion_counter % {frame_count}",
        ranges={i: row for i, row in enumerate(engine_layouts)},
        default=engine_layouts[0]
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
