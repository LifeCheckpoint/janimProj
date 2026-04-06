#set page(width: 80em)

#let get-color(i) = {
  let hue = calc.rem(i * 1.37508, 360) 
  color.hsl(hue * 1deg, 70%, 50%)
}
#let width = 20
#let height = 15
#grid(
  columns: (auto,) * width,
  column-gutter: 2.5em,
  row-gutter: 1em,
  ..for i in range(width * height) {
    (block(inset: 1em)[$H_#i$],)
    // (text(fill: white)[$H_#i$],)
  }
)
