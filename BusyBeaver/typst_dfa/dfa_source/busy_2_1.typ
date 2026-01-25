#import "@preview/finite:0.5.0": automaton

#automaton(
  (
    A: (B: ("0|1,R", "1|1,L")),
    B: (A: "0|1,L", HALT: "1|1,R"),
    HALT: none
  ),

  labels: (
    A: [A#sub[start]],
    B: [B],
    HALT: [H#sub[stop]]
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
    )
  )
)
