#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (B: "0|1,R", D: "1|0,L"),
    B: (C: "0|1,R", F: "1|0,R"),
    C: (C: "0|1,L", A: "1|1,L"),
    D: (E: "0|0,L", Z: "1|1,R"),
    E: (F: "0|1,L", B: "1|0,R"),
    F: (C: "0|0,R", E: "1|0,R"),
    Z: none
  ),

  labels: (
    A: [A#sub[start]], B: [B], C: [C], D: [D], E: [E], F: [F], Z: [Z#sub[stop]]
  ),

  layout: layout.grid.with(
    columns: 4,
    spacing: 2,
  ),

  style: (
    state: (
      stroke: white,
      fill: none,
      label: (fill: white),
    ),
    transition: (
      stroke: white,
      label: (
        fill: white,
      ),
      curve: 0.5,
    ),
    A-B: (curve: 0, label: (pos: 0.5, dist: 0.25)),
    A-D: (curve: -1.3, label: (dist: -0.3)),
    B-C: (curve: -1.3, label: (pos: 0.5, dist: -0.25)),
    B-F: (curve: 0),
    C-A: (curve: 3, label: (dist: 0.3)),
    D-E: (curve: 0, label: (pos: 0.5)),
    D-Z: (curve: 0, label: (pos: 0.5, dist: 0.25)),
    E-B: (curve: 0, label: (dist: -0.25)),
    E-F: (curve: 0.5, label: (pos: 0.5)),
    F-C: (curve: 4, label: (pos: 0.5, dist: 0.3)),
    F-E: (curve: 0.5, label: (pos: 0.75, dist: 0.2)),
  )
)
