# Rewrite Notes

This file notes down what will be done in this "manual rewite" branch.

## Rationale

Whatever I was doing when starting CATS is not feasible, IMO.
I have to deal with gigantic messy JSON files, undescriptive graphics filenames, duplicate sprites,
and the current requirement of every feature in NARS being ported over to CATS.
I don't think that this is sustainable.

## Things to Do

- [ ] CONSIDER: Pick a different data serialization format for vehicle data.
- [ ] Separate each vehicle into its own file.
- [ ] Rename each image in `res` to something more descriptive than an `train_$ID.png`.
- [ ] (While implementing) Document all special behavior from NARS. (e.g. auto-flip, B-units, coaches/mail cars having special graphics when used with certain locos)
- [ ] Reorganize vehicle sprites into:
  - `cars`
    - `freight`
    - `coach`
    - `other`
  - `locos`
    - `steam`
    - `diesel`
    - `electric`
- [ ] Rework vehicle sprites to use less cryptic offsets.
  - Base on 4px = 1/8tl.
  - Each orientation is a column.
  - Each animation frame is a new row.
- [ ] Reimplement single-unit diesel/electric locomotives with no animations.
- [ ] Reimplement single-unit diesel/electric locomotives with animations.
- [ ] Reimplement non-articulated steam engines.
- [ ] Reimplement articulated steam engines.
- [ ] Reimplement coaches.
- [ ] Reimplement freight cars with invisible loads.
- [ ] Reimplement all other freight cars.
- [ ] Reimplement all multiple-unit locos.