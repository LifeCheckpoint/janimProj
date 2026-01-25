#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (B: "0|1,R", A: "1|1,R"),
    B: (C: "0|1,R", Z: "1|1,R"),
    C: (D: "0|1,L", F: "1|0,R"),
    D: (A: "0|1,R", E: "1|0,L"),
    E: (D: "0|0,L", C: "1|1,R"),
    F: (A: "0|1,R", E: "1|0,R"),
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
    B-C: (curve: 0, label: (pos: 0.5, dist: 0.25)),
    B-Z: (curve: -1.5, label: (dist: -0.3)),
    C-D: (label: (pos: 0.45, dist: -0.25)),
    C-F: (label: (pos: 0.45, dist: -0.25)),
    F-A: (curve: 1, label: (pos: 0.75, dist:-0.3)),
    F-E: (curve: 0, label: (pos: 0.25)),
    D-A: (curve: -1.2, label: (dist: -0.3)),
    D-E: (curve: 1.8),
    E-D: (curve: 1.2, label: (pos: 0.25, dist: -0.25)),
    E-C: (curve: 1.2),
  )
)
