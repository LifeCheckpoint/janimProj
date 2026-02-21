#set page(margin: (x: 1cm, y: 1cm), width: 15cm, height: auto)

#set par(justify: true)
#set text(font: "Georgia", size: 11pt)
#show link: set text(fill: rgb("#1a0dab"))

#block(fill: white, outset: 1em)[

  // Gray navigation bar
  #rect(fill: luma(238), width: 100%, inset: 10pt, stroke: none)[
    #set text(size: 9.5pt)
    #align(center)[
      « #link("https://example.com")[The 8000th Busy Beaver number eludes ZF set theory: new paper by Adam Yedidia and me]
    ]
  ]

  // Title row
  #v(4pt)
  #grid(
    columns: (1fr, auto),
    align: (left + bottom, right + bottom),
    text(size: 22pt, weight: "bold", fill: black)[Three announcements],
    link("https://example.com")[My Quora session »],
  )

  #v(8pt)

  // (-3) paragraph
  #text(fill: black)[(-3)] #text(fill: red, weight: "bold")[Bonus Announcement of May 30:] #text(fill: black)[As a joint effort by Yuri Matiyasevich, Stefan O'Rear, and myself, and using the Not-Quite-Laconic language that Stefan adapted from Adam Yedidia's Laconic, #box[we now have a #link("https://example.com")[744-state]] <par1> #box[#link("https://example.com")[TM] that halts iff there's a counterexample to the Riemann Hypothesis.] <par2>]

  // (-2) paragraph
  #text(fill: black)[(-2)] #text(fill: red, weight: "bold")[Today's Bonus Announcement:] #text(fill: black)[Stefan O'Rear says that hisTuring machine to search for contradictions in ZFC is now down to 1919 states. #h(3pt) If verified, this is an important milestone: our upper bound on the number of Busy Beaver values that are knowable in standard mathematics is now *less* than the number of years since the birth of Christ (indeed, even since the generally-accepted dates for the writing of the Gospels).]

  #text(fill: black)[Stefan also says that his Not-Quite-Laconic system has yielded a1008-state Turing machine to search for counterexamples to the Riemann Hypothesis, improving on our 5372 states.]

]