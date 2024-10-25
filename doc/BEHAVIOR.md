# Vehicle-specific special behavior

This file documents special behavior and interactions between certain locomotives and certain cars.

## B-units

B-units only appear in chains of identical locomotives (i.e. train of EMD FP9, EMD FT, and EMD FP9, the middle FT will be an A-unit).
This is called a ***chain*** (see NML docs, which uses the same term).

Locos with B-units have the following conditions:

|     Location in chain      | Orientation | Appearance  |
| :------------------------: | :---------: | :---------: |
|           First            |   Normal    |      A      |
|           First            |   Flipped   | B (Flipped) |
|           Middle           |   Normal    |      B      |
|           Middle           |   Flipped   | B (Flipped) |
|            Last            |   Normal    |      B      |
|            Last            |   Flipped   | A (Flipped) |
| Last & First (single unit) |   Normal    |      A      |
| Last & First (single unit) |   Flipped   |      B      |

## Reversing locomotives

Some locomotives, instead of flipping when reversing at a station/waypoint/signal, will instead reverse in the same orientation.
They usually are switchers.

The reversing state can be read with `vehicle_is_reversed` and interacts weirdly with flipping:

| Reversing State | Orientation |    Graphics     |
| :-------------: | :---------: | :-------------: |
|     Forward     |   Normal    |     Forward     |
|     Forward     |   Flipped   | Forward Flipped |
|    Reversed     |   Normal    |    Reversed     |
|    Reversed     |   Flipped   | Forward Flipped |

What is strange is that the NARS devs did not write a set of offsets for the final reversed-and-flipped case.
This arrangement leads to reversed-and-flipped locos having the usual flip-when-reversing behavior instead of the custom reverse-instead-of-flip behavior.

As for graphics, some locos have a 3-row forward-reverse-flipped arrangemeent. the Alco RS3 has only 2 rows.
