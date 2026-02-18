#set page(width: 60em)

#let get-color(i) = {
  let hue = calc.rem(i * 1.37508, 360) 
  color.hsl(hue * 1deg, 70%, 50%)
}
#let radius = 20
#grid(
  columns: (auto,) * radius,
  column-gutter: 2.5em,
  row-gutter: 1em,
  ..for i in range(radius * radius) {
    ([$H_#i$],)
    // (text(fill: white)[$H_#i$],)
  }
)
