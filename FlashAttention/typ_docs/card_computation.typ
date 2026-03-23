#import "preamble.typ": conf
#show: conf

#let c = rgb("#FDF6E3")

#set text(fill: c, size: 9pt)

#table(
  columns: (1.9fr, 2fr, 1fr, 1.2fr, 1.2fr, 1.2fr, 1.2fr, 1.2fr, 1.2fr, 1.2fr),
  align: (left, right, right, right, right, right, right, right, right, right),
  inset: (x: 6pt, y: 4pt),
  stroke: none,

  table.hline(y: 0, stroke: 1.2pt + c),
  table.hline(y: 1, stroke: 0.6pt + c),
  table.hline(y: 7, stroke: 1.2pt + c),

  strong[型号], strong[FP64], strong[FP32], strong[TF32], strong[BF16],
  strong[FP16], strong[FP8], strong[INT8], strong[FP4], strong[INT4],

  strong[A100 80GB], [9.7（19.5 TC）], [19.5], [156 / 312\*], [312 / 624\*],
  [312 / 624\*], [—], [624 / 1248\*], [—], [—],

  strong[H100 SXM], [34（67 TC）], [67], [494.5 / 989\*], [989.5 / 1979\*],
  [989.5 / 1979\*], [1979 / 3958\*], [1979 / 3958\*], [—], [—],

  strong[H200 SXM], [34（67 TC）], [67], [494.5 / 989\*], [989.5 / 1979\*],
  [989.5 / 1979\*], [1979 / 3958\*], [1979 / 3958\*], [—], [—],

  strong[L4], [—], [30.3], [60 / 120\*], [121 / 242\*],
  [121 / 242\*], [242.5 / 485\*], [242.5 / 485\*], [—], [—],

  strong[L40S], [—], [91.6], [183 / 366\*], [362.05 / 733\*],
  [362.05 / 733\*], [733 / 1466\*], [733 / 1466\*], [—], [733 / 1466\*†],

  strong[HGX B200/8], [37], [75], [1125 / 2250\*], [2250 / 4500\*],
  [2250 / 4500\*], [4500 / 9000\*], [4500 / 9000\*], [9000 / 18000\*], [—],
)

#v(6pt)
#set text(size: 8pt)

注：\* 表示稀疏性能；† 表示特定条件下的 INT4 数据。