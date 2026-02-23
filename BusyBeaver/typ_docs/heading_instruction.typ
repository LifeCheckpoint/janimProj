#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import fletcher.shapes: diamond

#diagram(
	node-stroke: white,
	node((-0.75,1.5), [图灵机流程], extrude: (0, 3)),
	node((0,0), [#box[读取状态] <reading>], corner-radius: 2pt),
	edge("-|>", stroke: white),
	node((0,1), [#box[写入数据] <writing>], corner-radius: 2pt),
	edge("-|>", [0/1], label-pos: 0.5, stroke: white),
  node((0,2), [#box[改变状态] <state_changing>], corner-radius: 2pt),
  edge("-|>", stroke: white),
  node((0,3), [#box[移动一格] <moving>], corner-radius: 2pt),
)