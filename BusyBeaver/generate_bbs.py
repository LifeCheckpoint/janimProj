from pathlib import Path

def simulate_bb(name, rules):
    tape, pos, state, history = {}, 0, 'A', []
    while state != 'H':
        val = tape.get(pos, 0)
        history.append((dict(tape), pos)) # 记录当前带子和指针位置
        (write, move, next_state) = rules[(state, val)]
        tape[pos] = write
        pos += 1 if move == 'R' else -1
        state = next_state
    history.append((dict(tape), pos)) # 记录停机状态
    
    # 计算纸带边界以对齐输出
    all_indices = [i for h in history for i in h[0].keys()] + [h[1] for h in history]
    min_i, max_i = min(all_indices), max(all_indices)
    
    path = Path("resources/bbs_track") / f"{name}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)

    content = ""
    for t, p in history:
        line = "".join(str(t.get(i, 0)) for i in range(min_i, max_i + 1))
        content += line + "\n"
    path.write_text(content)

# 定义规则表 (状态, 读入) -> (写入, 移动, 下一状态)
machines = {
    "BB1": {('A', 0): (1, 'R', 'H')},
    "BB2": {('A', 0): (1, 'R', 'B'), ('A', 1): (1, 'L', 'B'),
            ('B', 0): (1, 'L', 'A'), ('B', 1): (1, 'R', 'H')},
    "BB3": {('A', 0): (1, 'R', 'B'), ('A', 1): (1, 'R', 'H'),
            ('B', 0): (1, 'L', 'B'), ('B', 1): (0, 'R', 'C'),
            ('C', 0): (1, 'L', 'C'), ('C', 1): (1, 'L', 'A')},
    "BB4": {('A', 0): (1, 'R', 'B'), ('A', 1): (1, 'L', 'B'),
            ('B', 0): (1, 'L', 'A'), ('B', 1): (0, 'L', 'C'),
            ('C', 0): (1, 'R', 'H'), ('C', 1): (1, 'L', 'D'),
            ('D', 0): (1, 'R', 'D'), ('D', 1): (0, 'R', 'A')}
}

for name, rules in machines.items():
    simulate_bb(name, rules)
    print(f"已生成 {name}.txt")