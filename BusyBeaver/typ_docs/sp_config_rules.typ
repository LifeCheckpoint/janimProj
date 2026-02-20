#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R0*], $ C(4k) -> "Halt"((3^(k+3)-11)/2) $,
  )
] <R0>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R1*], $ C(4k + 1) -> C((3^(k+3)-11)/2) $,
  )
] <R1>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R1*], $ C(4 dot 1 + 1) -> C((3^(1+3)-11)/2) $,
  )
] <R1.2>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R1*], $ C(5) -> C((3^4-11)/2) $,
  )
] <R1.3>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R1*], $ C(5) -> C(35) $,
  )
] <R1.4>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R2*], $ C(4k + 2) -> C((3^(k+3)-11)/2) $,
  )
] <R2>

#box[
  #grid(
    align: horizon,
    column-gutter: 1em,
    columns: 2,
    [- *R3*], $ C(4k + 3) -> C((3^(k+3)+1)/2) $,
  )
] <R3>

#[
  #let C(arg) = {
    let color = rgb("#87CEEB")
    $ C (#text(fill: color)[$#arg$]) $
  }

  #box[$ #C(5) $] <RC.1>

  #box[$ #C(5) -> C(#text(yellow)[$ (3^(1+3)-11)/2 $]) $] <RC.2>

  #box[$ #C(5) -> #C(35) $] <RC.3>

  #box[$ #C(5) -> #C(35) -> C(#text(yellow)[$ (3^(8+3)+1)/2 $]) $] <RC.4>

  #box[$ #C(5) -> #C(35) -> #C(88574) $] <RC.5>

  #box[$ #C(5) -> #C(35) -> #C(88574) -> C(#text(yellow)[$ (3^(22143+3)-11)/2 $]) $] <RC.6>

  #box[$ #C(5) -> #C(35) -> #C(88574) -> C(#text(rgb("#87CEEB"))[$ 1062300...696959 $]) $] <RC.7>
]
