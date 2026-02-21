#set page(margin: (x: 1cm, y: 1cm), width: 15cm, height: auto)
#set text(font: "Linux Libertine", size: 10.5pt)
#set par(justify: true)

#block(fill: white)[

  // === Red header bar ===
  #block(fill: rgb("#6b241d"), width: 100%, inset: (x: 14pt, y: 7pt))[
    #text(fill: white, size: 20pt)[
      a#text(size: 20pt)[r]#text(size: 24pt, style: "italic")[X]#text(size: 20pt)[iv]
    ]
    #text(fill: white, size: 11pt)[ > cs > arXiv:2107.12475]
  ]

  #v(-8pt)

  // === Category subheader ===
  #block(fill: rgb("#e8e8e8"), width: 100%, inset: (x: 14pt, y: 7pt))[
    #text(weight: "bold", size: 10.5pt, fill: black)[Computer Science > Logic in Computer Science]
  ]

  #v(2pt)
  #pad(left: 14pt, right: 14pt)[

  #v(-8pt)

  // === Title ===
  #text(size: 18pt, weight: "bold", fill: black)[Hardness of busy beaver value BB(15)]

  #v(-12pt)

  // === Authors ===
  #text(fill: rgb("#0000cc"), size: 11pt)[Tristan Stérin]#text(size: 11pt)[, ]#text(fill: rgb("#0000cc"), size: 11pt)[Damien Woods]

  #v(4pt)

  // === Abstract ===
  #pad(left: 20pt, right: 20pt)[
    #text(weight: "bold", size: 10.5pt, fill: black)[Abstract:] #text(fill: black)[The busy beaver value BB(n) is the maximum number of steps made by any n-state, 2-symbol deterministic halting Turing machine starting on blank tape. The busy beaver function $n arrow.r.bar "BB"(n)$ is uncomputable and, from below, only 4 of its values, BB(1) ... BB(4), are known to date. This leads one to ask: from above, what is the smallest BB value that encodes a major mathematical challenge? #box[Knowing BB(4,888) has been shown by Yedidia and Aaronson \[28\] to] <par1> #box[be at least as hard as solving Goldbach's conjecture, with a subsequent] <par2> #box[improvement, as yet unpublished, to BB(27) \[4,1\].] <par3> We prove that know -ing BB(15) is at least as hard as solving the following Collatz-related conjecture by Erdős, open since 1979 \[9\]: for all n > 8 there is at least one digit 2 in the base 3 representation of $2^n$. We do so by constructing an explicit 15-state, 2-symbol Turing machine that halts if and only if the conjecture is false. This 2-symbol Turing machine simulates a conceptually simpler 5-state, 4-symbol machine which we construct first. This makes, to date, BB(15) the smallest busy beaver value that is related to a natural open problem in mathematics, bringing to light one of the many challenges underlying the quest of knowing busy beaver values.]
  ]
  ]

]