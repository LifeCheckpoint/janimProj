#set text(
  font: ("Inria Serif", "LXGW WenKai"), 
  lang: "zh"
)
#show math.equation: set text(font: ("New Computer Modern Math", "LXGW WenKai"))

#let conf(body) = {
  set text(
    font: ("Inria Serif", "LXGW WenKai"), 
    lang: "zh"
  )
  show math.equation: set text(font: ("New Computer Modern Math", "LXGW WenKai"))
  body
}