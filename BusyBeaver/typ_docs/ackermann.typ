#set page(width: 60em)

#columns(2, gutter: 4em)[
  #box[
    #[
      #show math.equation: set align(left)
      #show math.equation: set block(inset: (left: 0em))
      #text(fill: color.rgb("#FFB6B6"))[Ackermann 函数] (Ackermann function)

      $ A(m, n) = cases(
          n+1 quad & m = 0,
          A(m-1\, 1) quad & m>0\, n=0,
          A(m-1\, A(m\, n-1)) quad & m>0\, n>0
      ) $
    ]

    对于足够大的 $m, n$，$A(m,n)>>underbrace(m^m^dots.up^m,n 个)$
  ] <intro>

  #colbreak()

  #box[
    #grid(
      columns: 1,
      align: center + horizon,
      inset: (x: 1.0em, y: 0.2em),
      rows: 2em,
      stroke: white,

      [$ g_1 = 3 arrow.t arrow.t arrow.t arrow.t 3 = 3 arrow.t^4 3 $ ],
      [$ g_2 = 3 arrow.t^(g_1) 3 $],
      [$ g_3 = 3 arrow.t^(g_2) 3 $],
      [$ ... $],
      [$ g_n = 3 arrow.t^(g_(n-1)) 3 $],
      [#box[$ G = g_(64) $] <GDef>],
    )
  ] <calc>
]
