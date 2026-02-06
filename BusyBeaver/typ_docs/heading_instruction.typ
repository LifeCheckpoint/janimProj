#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import fletcher.shapes: diamond

#diagram(
	node-stroke: white,
	node((0,0), [#box[读取状态] <reading>], corner-radius: 2pt, extrude: (0, 3)),
	edge("-|>", stroke: white),
	node((0,1), [#box[写入数据] <writing>], shape: diamond),
	edge("d,r,u", "-|>", [0/1], label-pos: 0.5, stroke: white),
  node((1,1), [#box[改变状态] <state_changing>]),
  edge("u", "-|>", stroke: white),
  node((1,0), [#box[移动一格] <moving>]),
  edge("l", "-|>", stroke: white),
)