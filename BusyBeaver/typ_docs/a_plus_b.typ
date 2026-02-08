#import "@preview/lovelace:0.3.0": *

#pseudocode-list(
  booktabs: true,
  title: smallcaps[Turing Machine Unary Addition],
  booktabs-stroke: white,
)[
  + *Input:* $a$ 个 $1$, 分隔符 $0$，$b$ 个 $1$.
  + *Initial:* 读写头在最左侧 $1$.
  + $space$
  + \/\/ Phase 1: 跳过第一组 $1$
  + *while* tape[head] == 1 *do*
    + *move right* (State A)
  + *end*
  + $space$
  + \/\/ Phase 2: 跨过分隔符，检查第二组
  + *move right* (State B)
  + *if* tape[head] == 1 *then*
    + *write* 0, *move left*
    + *write* 1, *move right*
    + *goto* Phase 1
  + *else*
    + *halt* #h(1em)\/\/ 停机
  + *end*
]