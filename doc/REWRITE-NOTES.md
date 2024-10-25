# Rewrite Notes

This file notes down what will be done in this "manual rewite" branch.

## Rationale

Whatever I was doing when starting CATS is not feasible, IMO.
I have to deal with gigantic messy JSON files, undescriptive graphics filenames, duplicate sprites,
and the current requirement of every feature in NARS being ported over to CATS.
I don't think that this is sustainable.

## Things to Do

- [x] CONSIDER: Pick a different data serialization format for vehicle data.
- [x] Separate each vehicle into its own file.
- [ ] (While implementing) Document all special behavior from NARS. (e.g. auto-flip, B-units, coaches/mail cars having special graphics when used with certain locos)
- [x] Reorganize vehicle sprites into:
  - `cars`
  - `locos`
    - `steam`
    - `diesel`
    - `electric`
- [ ] Reimplement diesel locomotives:
  - [ ] Simple, single-unit
  - [ ] With B-units
  - [ ] Reversible
  - [ ] Passenger
- [ ] Reimplement electric locomotives
- [ ] Reimplement steam engines:
  - [ ] Non-articulated
  - [ ] Non-articulated, reversible
  - [ ] Articulated
- [ ] Reimplement coaches.
- [ ] Reimplement freight cars with invisible loads.
- [ ] Reimplement all other freight cars.
- [ ] Reimplement all multiple-unit locos.