#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (B: "0|1,R", C: "1|1,L"),
    B: (C: "0|1,R", B: "1|1,R"),
    C: (D: "0|1,R", E: "1|0,L"),
    D: (A: "0|1,L", D: "1|1,L"),
    E: (Z: "0|1,R", A: "1|0,L"),
    Z: none
  ),

  labels: (
    A: [#box[A] <A>],
    B: [#box[B] <B>],
    C: [#box[C] <C>],
    D: [#box[D] <D>],
    E: [#box[E] <E>],
    Z: [#box[H] <H>],
  ),

  layout: layout.grid.with(
    columns: 3,
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
    A-C: (curve: -1, label: (dist: -0.3)),
    B-C: (curve: 0, label: (pos: 0.5, dist: 0.25)),
    C-D: (curve: -0.3, label: (pos: 0.45, dist: -0.3)),
    C-E: (curve: 0, label: (pos: 0.45, dist: 0.3)),
    D-A: (curve: 0, label: (pos: 0.45, dist: -0.25)),
    E-Z: (curve: 0, label: (pos: 0.5, dist: 0.25)),
    E-A: (curve: 0, label: (pos: 0.25, dist: -0.25)),
  )
)