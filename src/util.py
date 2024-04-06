from typing import Iterator, TypeVar

T = TypeVar("T")


def chunk(l: list[T], n: int) -> list[list[T]]:
    return [l[i:i + n] for i in range(0, len(l), n)]
