#import "@preview/cetz:0.4.2"
#import "@preview/cetz-venn:0.1.4"

#cetz.canvas({
  cetz-venn.venn3(
    name: "venn",
    stroke: white,
    fill: black,
  )
 
  import cetz.draw: *
  content("venn.a", [#text(size: 0.75em, fill: white)[#box[左右镜像] <lr>]])
  content("venn.b", [#text(size: 0.75em, fill: white)[#box[符号交换] <syn>]])
  content("venn.c", [#text(size: 0.75em, fill: white)[#box[状态重标号] <re>]])
  line(
    "venn.abc",
    (rel: (2.2,-2.5)),
    stroke: white,
    mark: (start: "o", stroke: white, fill: white),
    name: "arrow"
  )
  content(
    "arrow.end",
    text(fill: white)[$8800$ 万],
    anchor: "north",
    padding: .1
  )
}, stroke: none)
