from typing import Any, Generator


def chunk(l: list[Any], n: int) -> Generator[list[Any], Any, Any]:
    for i in range(0, len(l), n):
        yield l[i:i + n]
