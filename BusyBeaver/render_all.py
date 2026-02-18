"""
并行渲染 BusyBeaver 文件夹中的所有动画，至多同时运行 2 个任务。
用法: 在 BusyBeaver 目录下运行 python render_all.py
"""
import subprocess, concurrent.futures, time
from pathlib import Path

CWD = Path(__file__).parent

TASKS = [
    ("s1_NestedSequence.py", "s1_2"),
    ("s1_NestedSequence.py", "s1_3"),
    ("s1_NestedSequence.py", "s1_4"),
    ("s1_NestedSequence.py", "s1_5"),
    ("s2_TuringMachineAndHalt.py", "s2_1"),
    ("s2_TuringMachineAndHalt.py", "s2_2"),
    ("s2_TuringMachineAndHalt.py", "s2_3"),
    ("s2_TuringMachineAndHalt.py", "s2_4"),
    ("s2_TuringMachineAndHalt.py", "s2_5"),
    ("s3_BusyBeaver.py", "s3_1"),
    ("s3_BusyBeaver.py", "s3_2"),
    ("s3_BusyBeaver.py", "s3_3"),
    ("s3_BusyBeaver.py", "s3_4"),
    ("s3_BusyBeaver.py", "s3_5"),
]

def render(task):
    file, scene = task
    print(f"[开始] {file} {scene}")
    t0 = time.time()
    r = subprocess.run(
        ["uv", "run", "janim", "write", file, scene],
        capture_output=True, text=True, cwd=CWD,
    )
    elapsed = time.time() - t0
    status = "成功" if r.returncode == 0 else "失败"
    print(f"[{status}] {file} {scene} ({elapsed:.1f}s)")
    if r.returncode != 0:
        print(r.stderr[-500:] if len(r.stderr) > 500 else r.stderr)
    return (file, scene, r.returncode)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(render, TASKS))
    failed = [f"{f} {s}" for f, s, rc in results if rc != 0]
    print(f"\n全部完成: {len(results) - len(failed)}/{len(results)} 成功")
    if failed:
        print("失败任务:", *failed, sep="\n  ")
