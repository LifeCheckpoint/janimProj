#import "@preview/finite:0.5.0": automaton

#automaton(
  (
    start: (start: "0|0, R", stop: "1|1, R"),
    stop: none
  ),
  style: (
    state: (
      stroke: red,
      fill: none,
      label: (fill: red),
    ),
    transition: (
      stroke: red,
      label: (fill: red)
    )
  )
)
