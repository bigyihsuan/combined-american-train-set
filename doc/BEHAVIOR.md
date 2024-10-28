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

## Locomotives with custom PAX/Mail graphics

The following locos have custom graphics for coaches and mail cars on the same train:

| Loco              | Car         | Notes                                   |
| ----------------- | ----------- | --------------------------------------- |
| EMD F59PHI        | Bilevel     | Changes to Coaster livery               |
| UAC TurboTrain    | Highspeed   |                                         |
| RTL Turboliner    | Highspeed   |                                         |
| Budd Metroliner   | Lightweight |                                         |
| Bombardier EMU    | Lightweight |                                         |
| Bombardier Acela  | Highspeed   |                                         |
| Nippon Sharyo EMU | Bilevel     | Bilevel changes to stainless steel look |

## Alternate graphics

### Passenger Car

- Last car has red lamp (2nd row).

### Heavyweight Car

- Last car has red lamp (2nd row).
- Car with logo, if not last in the train, appears in the middle of the chain (3rd row).
  - If even number of cars, choose the coach to the back.
- All cars after the logo car have alternate graphics (4th row).

### Lightweight Car

- Pre-1980:
  - Last car is an observation car with red lamp (3rd, 4th row).
  - Middle of the train has transition car (5th row).
  - Dome cars appear randomly in the back half of the train after the empty spot car. Last car can be a dome/observation car.
  - Front half of the train has offset windows (6th row).
- Post-1980:
  - Last car has red lamp.
  - Middle of the train has transition car.
- Mail:
  - Last car has red lamp (both forms).

### Bilevel Car

- Last car has caution stripes (both forms).

### Highspeed Cars

- The first (and last, if multiple cars) Highspeed (Mail) Car in a chain have fins.
- The last car has a flipped fin.
- Highspeed cars are meant for use with the Cabbage car.

## Date-dependent coach graphics

The following cars have date-dependent graphics:

| Car                  | Date | Group Before | Group After | Notes                                                      |
| -------------------- | ---- | ------------ | ----------- | ---------------------------------------------------------- |
| Lightweight Car      | 1980 | 143          | 144         | Black roof with observation car and domes, then metal roof |
| Bilevel Car          | 1990 | 145          | 146         | Black roof + CC walls, then to Bombardier BiLevel Coach    |
| Lightweight Mail Car | 1980 | 154/155      | 156/157     | Black roof, then metal roof                                |