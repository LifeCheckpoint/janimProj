#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (A: "0|1,R, 1|0,R"),
    HALT: none,
  ),

  labels: (
    A: [A],
    HALT: [H],
  ),

  layout: layout.grid.with(
    spacing: 0.5,
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
    ),
  )
)
