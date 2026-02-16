#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (B: "0|0,R", Z: "1|_,_"),
    B: (C: "0|1,L", A: "1|0,L"),
    C: (D: "0|0,R", Z: "1|_,_"),
    D: (E: "1|1,L", Z: "0|_,_"),
    E: (B: "0|0,R", Z: "1|_,_"),
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
    A-B: (curve: 0.5),
    A-Z: (curve: -1.5, label: (dist: -0.3)),
    B-C: (curve: 0),
    B-A: (curve: 0.5, label: (pos: 0.5, dist: -0.3)),
    C-D: (curve: 0),
    C-Z: (curve: 0, label: (dist: -0.3)),
    D-E: (curve: 0),
    D-Z: (curve: 0, label: (pos: 0.1, dist: 0.3)),
    E-B: (curve: 0.5, label: (pos: 0.3, dist: -0.3)),
    E-Z: (curve: 0, label: (dist: -0.3)),
  )
)