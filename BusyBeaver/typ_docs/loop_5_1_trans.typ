#import "@preview/finite:0.5.0": automaton, layout

#automaton(
  (
    A: (B: "1"),
    B: (C: "2"),
    C: (D: "3"),
    D: (E: "4"),
    E: (B2: "5"),
    B2: (A: "6"),
  ),

  final: none,

  labels: (
    A: [#box[A] <posA>],
    B: [#box[B] <posB>],
    C: [#box[C] <posC>],
    D: [#box[D] <posD>],
    E: [#box[E] <posE>],
    B2: [#box[B] <posB2>],
  ),

  layout: layout.circular.with(offset: 45deg),

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
  )
)

#let place-below(label, content, offset-x: -6em, offset-y: -1em, align-x: center) = context {
  let results = query(label)
  if results.len() == 0 { return }
  
  let target = results.first()
  let loc = target.location()
  let (x, y) = loc.position()
  let current-page = here().page()
  
  if current-page == loc.page() {
    let final-x = if align-x == center {
      x - measure(content).width / 2
    } else if align-x == right {
      x - measure(content).width
    } else {
      x
    }
    
    place(
      top + left,
      dx: final-x + offset-x,
      dy: y + offset-y,
      content
    )
  }
}
