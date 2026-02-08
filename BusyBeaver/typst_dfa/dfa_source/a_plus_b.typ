#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (A: "1|1,R", B: "0|0,R"),
    B: (C: "1|0,L", HALT: "0|0,R"),
    C: (A: "0|1,R"),
    HALT: none
  ),

  labels: (
    A: [A#sub[start]],
    B: [B],
    C: [C],
    HALT: [H#sub[stop]]
  ),

  layout: layout.grid.with(
    columns: 2,
    spacing: 3,
  ),

  style: (
    state: (
      stroke: white,
      fill: none,
      label: (fill: white),
    ),
    transition: (
      stroke: white,
      label: (fill: white)
    ),
    B-C: (curve: 0),
    B-HALT: (curve: 0),
    A-B: (curve: 0),
  )
)
