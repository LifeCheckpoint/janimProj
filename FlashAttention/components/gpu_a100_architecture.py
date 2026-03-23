from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from janim.imports import *  # type: ignore

from .colors import FAColor

GroupAny = Group[Any]


@dataclass(frozen=True)
class A100DepthConfig:
    basic_depth: int = 50

    center_spine: float = 10 + basic_depth

    top_bar_label: float = 11 + basic_depth
    top_bar_body: float = 12 + basic_depth

    nvlink_label: float = 13 + basic_depth
    nvlink_body: float = 14 + basic_depth
    hub_label: float = 15 + basic_depth
    hub_body: float = 16 + basic_depth

    l2_label: float = 17 + basic_depth
    l2_split: float = 18 + basic_depth
    l2_base: float = 19 + basic_depth

    gpc_label: float = 20 + basic_depth
    tpc_label: float = 21 + basic_depth
    tpc_sm: float = 22 + basic_depth
    tpc_bus: float = 23 + basic_depth
    tpc_compute: float = 24 + basic_depth
    tpc_cell: float = 25 + basic_depth
    gpc_row_link: float = 26 + basic_depth
    gpc_bar: float = 27 + basic_depth
    gpc_shell: float = 28 + basic_depth

    side_link: float = 29 + basic_depth
    memory_ctrl_text: float = 30 + basic_depth
    memory_ctrl_body: float = 31 + basic_depth
    hbm_text: float = 32 + basic_depth
    hbm_body: float = 33 + basic_depth

    chip_border: float = 34 + basic_depth
    die_bg: float = 35 + basic_depth


A100_DEPTH = A100DepthConfig()


@dataclass
class A100TPCCellPart:
    item: GroupAny
    cell: Rect
    sm_strip: Rect
    compute: Rect
    bus: Rect
    tpc_label: TypstText | None
    sm_label: TypstText | None


@dataclass
class A100GPCBlockPart:
    item: GroupAny
    shell: Rect
    gpc_bar: Rect
    gpc_label: TypstText
    cells: GroupAny
    cell_parts: list[A100TPCCellPart]
    row_links: GroupAny


@dataclass
class A100MemoryControllerSegmentPart:
    item: GroupAny
    body: Rect
    label: TypstText


@dataclass
class A100MemoryControllerColumnPart:
    item: GroupAny
    segments_group: GroupAny
    segment_parts: list[A100MemoryControllerSegmentPart]


@dataclass
class A100HBMBlockPart:
    item: GroupAny
    body: Rect
    label: TypstText


@dataclass
class A100HBMColumnPart:
    item: GroupAny
    blocks_group: GroupAny
    block_parts: list[A100HBMBlockPart]


@dataclass
class A100BarPart:
    item: GroupAny
    body: Rect
    label: TypstText


@dataclass
class A100NVLinkPart:
    item: GroupAny
    body: Rect
    label: TypstText


@dataclass
class A100L2Part:
    item: GroupAny
    base: Rect
    split: Rect
    labels: list[TypstText]


@dataclass
class A100ComputeCorePart:
    item: GroupAny
    top_row: GroupAny
    top_gpc_parts: list[A100GPCBlockPart]
    l2_part: A100L2Part
    bottom_row: GroupAny
    bottom_gpc_parts: list[A100GPCBlockPart]


@dataclass
class A100IOPart:
    item: GroupAny
    hub_part: A100BarPart
    nvlink_row: GroupAny
    nvlink_parts: list[A100NVLinkPart]


@dataclass
class A100TopBarsPart:
    item: GroupAny
    pci_part: A100BarPart
    giga_part: A100BarPart


@dataclass
class GPUA100ArchitecturePart:
    item: GroupAny

    die_bg: Rect
    chip_border: Rect
    architecture: GroupAny

    top_bars_part: A100TopBarsPart
    compute_core_part: A100ComputeCorePart
    io_part: A100IOPart

    main_stack: GroupAny
    center_spine: Rect

    left_memory_controller: A100MemoryControllerColumnPart
    right_memory_controller: A100MemoryControllerColumnPart
    left_hbm: A100HBMColumnPart
    right_hbm: A100HBMColumnPart
    left_links: GroupAny
    right_links: GroupAny


def _set_depth(item: VItem, depth: float) -> None:
    item.depth.set(depth)


def _make_label(
    text: str,
    scale: float = 0.40,
    color: str = FAColor.a100_label_light,
    rotate: float = 0.0,
    depth: float = A100_DEPTH.gpc_label,
) -> TypstText:
    label = TypstText(text)
    label.points.scale(scale)
    if rotate != 0:
        label.points.rotate(rotate)
    label.astype(VItem).fill.set(color=color, alpha=1.0)
    label.astype(VItem).stroke.set(alpha=0.0)
    _set_depth(label.astype(VItem), depth)
    return label


def _create_tpc_cell(cell_w: float, cell_h: float, show_tags: bool = False) -> A100TPCCellPart:
    cell = Rect(cell_w, cell_h)
    cell.fill.set(color=FAColor.a100_tpc_cell_fill, alpha=1.0)
    cell.stroke.set(color=FAColor.a100_tpc_cell_stroke, alpha=1.0)
    cell.radius.set(0.0035)
    _set_depth(cell, A100_DEPTH.tpc_cell)

    sm_strip = Rect(cell_w * 0.86, cell_h * 0.28)
    sm_strip.fill.set(color=FAColor.a100_tpc_sm_fill, alpha=1.0)
    sm_strip.stroke.set(alpha=0.0)
    sm_strip.points.move_to(cell.points.box.center + UP * (cell_h * 0.20))
    _set_depth(sm_strip, A100_DEPTH.tpc_sm)

    compute = Rect(cell_w * 0.86, cell_h * 0.50)
    compute.fill.set(color=FAColor.a100_tpc_compute_fill, alpha=1.0)
    compute.stroke.set(alpha=0.0)
    compute.points.move_to(cell.points.box.center + DOWN * (cell_h * 0.10))
    _set_depth(compute, A100_DEPTH.tpc_compute)

    bus = Rect(cell_w * 0.86, cell_h * 0.07)
    bus.fill.set(color=FAColor.a100_tpc_bus_fill, alpha=1.0)
    bus.stroke.set(alpha=0.0)
    bus.points.move_to(cell.points.box.center + UP * (cell_h * 0.01))
    _set_depth(bus, A100_DEPTH.tpc_bus)

    tpc_txt: TypstText | None = None
    sm_txt: TypstText | None = None
    item = Group(cell, compute, bus, sm_strip)

    if show_tags:
        tpc_txt = _make_label(
            "TPC",
            scale=0.34,
            color=FAColor.a100_label_dim,
            depth=A100_DEPTH.tpc_label,
        )
        sm_txt = _make_label(
            "SM",
            scale=0.34,
            color=FAColor.a100_label_dim,
            depth=A100_DEPTH.tpc_label,
        )
        tpc_txt.points.move_to(cell.points.box.bottom + UP * (cell_h * 0.11))
        sm_txt.points.move_to(sm_strip)
        item.add(tpc_txt, sm_txt)

    return A100TPCCellPart(
        item=cast(Group, item),
        cell=cell,
        sm_strip=sm_strip,
        compute=compute,
        bus=bus,
        tpc_label=tpc_txt,
        sm_label=sm_txt,
    )


def _create_gpc_block(
    block_w: float,
    block_h: float,
    tpc_cols: int,
    tpc_rows: int,
    label_position: str = "top",
) -> A100GPCBlockPart:
    shell = Rect(block_w, block_h)
    shell.fill.set(color=FAColor.a100_gpc_shell_fill, alpha=1.0)
    shell.stroke.set(color=FAColor.a100_gpc_shell_stroke, alpha=1.0)
    shell.radius.set(0.0045)
    _set_depth(shell, A100_DEPTH.gpc_shell)

    bar_h = 0.24
    gpc_bar = Rect(block_w - 0.06, bar_h)
    gpc_bar.fill.set(color=FAColor.a100_gpc_bar_fill, alpha=1.0)
    gpc_bar.stroke.set(color=FAColor.a100_gpc_bar_stroke, alpha=1.0)
    gpc_bar.radius.set(0.004)
    _set_depth(gpc_bar, A100_DEPTH.gpc_bar)

    gpc_txt = _make_label(
        "GPC",
        scale=0.52,
        color=FAColor.a100_label_mid,
        depth=A100_DEPTH.gpc_label,
    )
    if label_position == "bottom":
        gpc_bar.points.move_to(shell.points.box.bottom + UP * (bar_h / 2 + 0.03))
        gpc_txt.points.next_to(gpc_bar, LEFT, buff=0.05)
    else:
        gpc_bar.points.move_to(shell.points.box.top + DOWN * (bar_h / 2 + 0.03))
        gpc_txt.points.next_to(gpc_bar, LEFT, buff=0.05)

    inner_w = block_w - 0.10
    inner_h = block_h - bar_h - 0.14
    col_gap = 0.015
    row_gap = 0.03
    cell_w = (inner_w - (tpc_cols - 1) * col_gap) / tpc_cols
    cell_h = (inner_h - (tpc_rows - 1) * row_gap) / tpc_rows

    cell_parts = [
        _create_tpc_cell(
            cell_w,
            cell_h,
            show_tags=(r in (0, tpc_rows - 1) and c in (0, tpc_cols - 1)),
        )
        for r in range(tpc_rows)
        for c in range(tpc_cols)
    ]
    cells = Group.from_iterable(part.item for part in cell_parts)
    cells.points.arrange_in_grid(n_rows=tpc_rows, n_cols=tpc_cols, buff=col_gap)

    if label_position == "bottom":
        cells.points.next_to(gpc_bar, UP, buff=0.04)
    else:
        cells.points.next_to(gpc_bar, DOWN, buff=0.04)

    shell_center_x = shell.points.box.center[0]
    cells.points.shift(RIGHT * (shell_center_x - cells.points.box.center[0]))

    row_link_items = []
    for r in range(1, tpc_rows):
        upper = cells[(r - 1) * tpc_cols].points.box.bottom[1]
        lower = cells[r * tpc_cols].points.box.top[1]
        y = (upper + lower) / 2
        link = Rect(inner_w, 0.02)
        link.fill.set(color=FAColor.a100_gpc_link_fill, alpha=1.0)
        link.stroke.set(alpha=0.0)
        link.points.move_to(RIGHT * shell_center_x + UP * y)
        _set_depth(link, A100_DEPTH.gpc_row_link)
        row_link_items.append(link)

    row_links = Group.from_iterable(row_link_items)
    item = Group(shell, gpc_bar, row_links, cells, gpc_txt)

    return A100GPCBlockPart(
        item=item,
        shell=shell,
        gpc_bar=gpc_bar,
        gpc_label=gpc_txt,
        cells=cells,
        cell_parts=cell_parts,
        row_links=row_links,
    )


def _create_memory_controller_column(width: float, height: float, segments: int = 4) -> A100MemoryControllerColumnPart:
    gap = 0.03
    seg_h = (height - (segments - 1) * gap) / segments
    segment_parts: list[A100MemoryControllerSegmentPart] = []

    for _ in range(segments):
        seg = Rect(width, seg_h)
        seg.fill.set(color=FAColor.a100_mem_ctrl_fill, alpha=1.0)
        seg.stroke.set(color=FAColor.a100_mem_ctrl_stroke, alpha=1.0)
        seg.radius.set(0.0035)
        _set_depth(seg, A100_DEPTH.memory_ctrl_body)

        txt = _make_label(
            "Memory Controller",
            scale=0.52,
            color=FAColor.a100_label_memory_ctrl,
            rotate=PI / 2,
            depth=A100_DEPTH.memory_ctrl_text,
        )
        txt.points.move_to(seg)

        segment_parts.append(
            A100MemoryControllerSegmentPart(
                item=Group(seg, txt),
                body=seg,
                label=txt,
            )
        )

    segments_group = Group.from_iterable(part.item for part in segment_parts)
    segments_group.points.arrange(DOWN, buff=gap)
    item = Group(segments_group)

    return A100MemoryControllerColumnPart(
        item=item,
        segments_group=segments_group,
        segment_parts=segment_parts,
    )


def _create_hbm_column(width: float, height: float) -> A100HBMColumnPart:
    gap = 0.18
    seg_h = (height - gap) / 2
    block_parts: list[A100HBMBlockPart] = []

    for _ in range(2):
        blk = Rect(width, seg_h)
        blk.fill.set(color=FAColor.a100_hbm_fill, alpha=1.0)
        blk.stroke.set(color=FAColor.a100_hbm_stroke, alpha=1.0)
        blk.radius.set(0.004)
        _set_depth(blk, A100_DEPTH.hbm_body)

        txt = _make_label(
            "HBM2",
            scale=0.60,
            color=FAColor.a100_label_light,
            rotate=PI / 2,
            depth=A100_DEPTH.hbm_text,
        )
        txt.points.move_to(blk)

        block_parts.append(
            A100HBMBlockPart(
                item=Group(blk, txt),
                body=blk,
                label=txt,
            )
        )

    blocks_group = Group.from_iterable(part.item for part in block_parts)
    blocks_group.points.arrange(DOWN, buff=gap)
    item = Group(blocks_group)

    return A100HBMColumnPart(
        item=item,
        blocks_group=blocks_group,
        block_parts=block_parts,
    )


def _create_side_links(controller: A100MemoryControllerColumnPart, hbm: A100HBMColumnPart, side: str) -> Group:
    arrows: list[Arrow] = []
    for seg_part in controller.segment_parts:
        y = seg_part.item.points.box.center[1]
        if side == "left":
            x0 = seg_part.item.points.box.left[0] - 0.02
            x1 = hbm.item.points.box.right[0] + 0.02
        else:
            x0 = seg_part.item.points.box.right[0] + 0.02
            x1 = hbm.item.points.box.left[0] - 0.02

        start = RIGHT * x0 + UP * y
        end = RIGHT * x1 + UP * y

        arrow = Arrow(start, end, color=FAColor.a100_side_link)
        arrow.astype(VItem).stroke.set(alpha=0.85)
        _set_depth(arrow, A100_DEPTH.side_link)
        arrows.append(arrow)

    return Group.from_iterable(arrows)


def _create_bar(
    text: str,
    width: float,
    height: float,
    fill: str,
    stroke: str,
    label_color: str,
    body_depth: float,
    label_depth: float,
    label_scale: float = 0.52,
) -> A100BarPart:
    body = Rect(width, height)
    body.fill.set(color=fill, alpha=1.0)
    body.stroke.set(color=stroke, alpha=1.0)
    body.radius.set(0.0045)
    _set_depth(body, body_depth)

    label = _make_label(
        text,
        scale=label_scale,
        color=label_color,
        depth=label_depth,
    )
    label.points.move_to(body)

    return A100BarPart(item=Group(body, label), body=body, label=label)


def create_GPU_A100_architecture(
    width: float = 15.2,
    height: float = 9.6,
    gpc_cols: int = 4,
    tpc_cols: int = 8,
    tpc_rows: int = 4,
    nvlink_count: int = 12,
) -> GPUA100ArchitecturePart:
    """
    创建一个复杂版 A100 架构示意图（近似原图风格）。

    返回 dataclass，包含：
    - 最外层 `item: Group`
    - 各层 Group 本体
    - 各层子物件 dataclass/list/item
    """
    if width <= 6 or height <= 4:
        raise ValueError("width/height 过小，无法构建 A100 架构示意图")
    if gpc_cols < 2:
        raise ValueError("gpc_cols 至少为 2")
    if tpc_cols < 2 or tpc_rows < 2:
        raise ValueError("tpc_cols/tpc_rows 至少为 2")
    if nvlink_count < 2:
        raise ValueError("nvlink_count 至少为 2")

    mem_ctrl_w = 0.56
    hbm_w = 0.62
    side_gap = 0.08

    core_w = width - 2 * (mem_ctrl_w + hbm_w + side_gap * 2)
    if core_w <= 4:
        raise ValueError("当前 width 不足以容纳核心区，请增大 width")

    v_gap = 0.08
    pci_h = 0.46
    giga_h = 0.42
    l2_h = 1.45
    hub_h = 0.48
    nv_h = 0.52

    gpc_h = (height - (pci_h + giga_h + l2_h + hub_h + nv_h) - 6 * v_gap) / 2
    if gpc_h <= 1.2:
        raise ValueError("当前 height 不足以容纳 GPC 区域，请增大 height")

    gpc_gap = 0.06
    gpc_w = (core_w - (gpc_cols - 1) * gpc_gap) / gpc_cols

    top_gpc_parts = [
        _create_gpc_block(gpc_w, gpc_h, tpc_cols=tpc_cols, tpc_rows=tpc_rows, label_position="top")
        for _ in range(gpc_cols)
    ]
    top_row = Group.from_iterable(part.item for part in top_gpc_parts)
    top_row.points.arrange(RIGHT, buff=gpc_gap)

    bottom_gpc_parts = [
        _create_gpc_block(gpc_w, gpc_h, tpc_cols=tpc_cols, tpc_rows=tpc_rows, label_position="bottom")
        for _ in range(gpc_cols)
    ]
    bottom_row = Group.from_iterable(part.item for part in bottom_gpc_parts)
    bottom_row.points.arrange(RIGHT, buff=gpc_gap)

    l2_base = Rect(core_w, l2_h)
    l2_base.fill.set(color=FAColor.a100_l2_fill, alpha=1.0)
    l2_base.stroke.set(color=FAColor.a100_l2_stroke, alpha=1.0)
    l2_base.radius.set(0.005)
    _set_depth(l2_base, A100_DEPTH.l2_base)

    l2_split = Rect(0.08, l2_h)
    l2_split.fill.set(color=FAColor.a100_l2_split_fill, alpha=1.0)
    l2_split.stroke.set(alpha=0.0)
    l2_split.points.move_to(l2_base)
    _set_depth(l2_split, A100_DEPTH.l2_split)

    l2_l = _make_label("L2 Cache", scale=0.95, color=FAColor.a100_label_l2, depth=A100_DEPTH.l2_label)
    l2_r = _make_label("L2 Cache", scale=0.95, color=FAColor.a100_label_l2, depth=A100_DEPTH.l2_label)
    l2_l.points.move_to(l2_base.points.box.center + LEFT * (core_w * 0.25))
    l2_r.points.move_to(l2_base.points.box.center + RIGHT * (core_w * 0.25))

    l2_part = A100L2Part(item=Group(l2_base, l2_split, l2_l, l2_r), base=l2_base, split=l2_split, labels=[l2_l, l2_r])

    compute_core = Group(top_row, l2_part.item, bottom_row)
    compute_core.points.arrange(DOWN, buff=v_gap)
    compute_core_part = A100ComputeCorePart(
        item=compute_core,
        top_row=top_row,
        top_gpc_parts=top_gpc_parts,
        l2_part=l2_part,
        bottom_row=bottom_row,
        bottom_gpc_parts=bottom_gpc_parts,
    )

    hub_part = _create_bar(
        text="High-Speed Hub",
        width=core_w,
        height=hub_h,
        fill=FAColor.a100_hub_fill,
        stroke=FAColor.a100_hub_stroke,
        label_color=FAColor.a100_label_light,
        body_depth=A100_DEPTH.hub_body,
        label_depth=A100_DEPTH.hub_label,
        label_scale=0.60,
    )

    nv_gap = 0.03
    nv_w = (core_w - (nvlink_count - 1) * nv_gap) / nvlink_count
    nvlink_parts = [
        A100NVLinkPart(
            item=Group(
                blk := Rect(nv_w, nv_h),
                txt := _make_label(
                    "NVLink",
                    scale=0.54,
                    color=FAColor.a100_label_nvlink,
                    depth=A100_DEPTH.nvlink_label,
                ),
            ),
            body=blk,
            label=txt,
        )
        for _ in range(nvlink_count)
    ]
    for part in nvlink_parts:
        part.body.fill.set(color=FAColor.a100_nvlink_fill, alpha=1.0)
        part.body.stroke.set(color=FAColor.a100_nvlink_stroke, alpha=1.0)
        part.body.radius.set(0.0035)
        _set_depth(part.body, A100_DEPTH.nvlink_body)
        part.label.points.move_to(part.body)

    nvlink_row = Group.from_iterable(part.item for part in nvlink_parts)
    nvlink_row.points.arrange(RIGHT, buff=nv_gap)

    io_item = Group(hub_part.item, nvlink_row)
    io_item.points.arrange(DOWN, buff=0.04)
    io_part = A100IOPart(item=io_item, hub_part=hub_part, nvlink_row=nvlink_row, nvlink_parts=nvlink_parts)

    main_stack = Group(compute_core_part.item, io_part.item)
    main_stack.points.arrange(DOWN, buff=v_gap)

    left_memory_controller = _create_memory_controller_column(mem_ctrl_w, compute_core_part.item.points.box.height)
    right_memory_controller = _create_memory_controller_column(mem_ctrl_w, compute_core_part.item.points.box.height)

    left_memory_controller.item.points.next_to(compute_core_part.item, LEFT, buff=0.05)
    right_memory_controller.item.points.next_to(compute_core_part.item, RIGHT, buff=0.05)
    left_memory_controller.item.points.align_to(compute_core_part.item, UP)
    right_memory_controller.item.points.align_to(compute_core_part.item, UP)

    left_hbm = _create_hbm_column(hbm_w, compute_core_part.item.points.box.height)
    right_hbm = _create_hbm_column(hbm_w, compute_core_part.item.points.box.height)

    left_hbm.item.points.next_to(left_memory_controller.item, LEFT, buff=0.12)
    right_hbm.item.points.next_to(right_memory_controller.item, RIGHT, buff=0.12)
    left_hbm.item.points.align_to(compute_core_part.item, UP)
    right_hbm.item.points.align_to(compute_core_part.item, UP)

    left_links = _create_side_links(left_memory_controller, left_hbm, side="left")
    right_links = _create_side_links(right_memory_controller, right_hbm, side="right")

    top_bar_w = compute_core_part.item.points.box.width + 2 * mem_ctrl_w + 0.1
    pci_part = _create_bar(
        text="PCI Express 4.0 Host Interface",
        width=top_bar_w,
        height=pci_h,
        fill=FAColor.a100_pci_fill,
        stroke=FAColor.a100_pci_stroke,
        label_color=FAColor.a100_label_light,
        body_depth=A100_DEPTH.top_bar_body,
        label_depth=A100_DEPTH.top_bar_label,
    )
    giga_part = _create_bar(
        text="GigaThread Engine with MIG Control",
        width=top_bar_w,
        height=giga_h,
        fill=FAColor.a100_giga_fill,
        stroke=FAColor.a100_giga_stroke,
        label_color=FAColor.a100_label_giga_dark,
        body_depth=A100_DEPTH.top_bar_body,
        label_depth=A100_DEPTH.top_bar_label,
    )

    top_bars_item = Group(pci_part.item, giga_part.item)
    top_bars_item.points.arrange(DOWN, buff=0.02)
    top_bars_item.points.next_to(compute_core_part.item, UP, buff=v_gap)
    top_bars_part = A100TopBarsPart(item=top_bars_item, pci_part=pci_part, giga_part=giga_part)

    center_spine = Rect(0.06, compute_core_part.item.points.box.height)
    center_spine.fill.set(color=FAColor.a100_center_spine_fill, alpha=1.0)
    center_spine.stroke.set(alpha=0.0)
    center_spine.points.move_to(compute_core_part.item)
    _set_depth(center_spine, A100_DEPTH.center_spine)

    architecture = Group(
        top_bars_part.item,
        main_stack,
        left_memory_controller.item,
        right_memory_controller.item,
        left_hbm.item,
        right_hbm.item,
        left_links,
        right_links,
        center_spine,
    )

    die_bg = Rect(
        architecture.points.box.width + 0.35,
        architecture.points.box.height + 0.35,
    )
    die_bg.fill.set(color=FAColor.a100_die_bg_fill, alpha=1.0)
    die_bg.stroke.set(color=FAColor.a100_die_bg_stroke, alpha=1.0)
    die_bg.radius.set(0.005)
    die_bg.points.move_to(architecture)
    _set_depth(die_bg, A100_DEPTH.die_bg)

    chip_border = Rect(
        architecture.points.box.width + 0.12,
        architecture.points.box.height + 0.12,
    )
    chip_border.fill.set(alpha=0.0)
    chip_border.stroke.set(color=FAColor.a100_chip_border_stroke, alpha=1.0)
    chip_border.radius.set(0.004)
    chip_border.points.move_to(architecture)
    _set_depth(chip_border, A100_DEPTH.chip_border)

    item = Group(die_bg, chip_border, architecture)

    return GPUA100ArchitecturePart(
        item=item,
        die_bg=die_bg,
        chip_border=chip_border,
        architecture=architecture,
        top_bars_part=top_bars_part,
        compute_core_part=compute_core_part,
        io_part=io_part,
        main_stack=main_stack,
        center_spine=center_spine,
        left_memory_controller=left_memory_controller,
        right_memory_controller=right_memory_controller,
        left_hbm=left_hbm,
        right_hbm=right_hbm,
        left_links=left_links,
        right_links=right_links,
    )


@dataclass(frozen=True)
class A100SMDepthConfig:
    basic_depth: int = 10

    sm_tag_label: float = 10 + basic_depth
    sm_tag_body: float = 11 + basic_depth

    tex_label: float = 12 + basic_depth
    tex_body: float = 13 + basic_depth
    l1d_label: float = 14 + basic_depth
    l1d_body: float = 15 + basic_depth

    ldst_label: float = 16 + basic_depth
    ldst_body: float = 17 + basic_depth
    tensor_label: float = 18 + basic_depth
    tensor_body: float = 19 + basic_depth
    compute_label: float = 20 + basic_depth
    compute_cell: float = 21 + basic_depth

    bar_label: float = 22 + basic_depth
    bar_body: float = 23 + basic_depth
    panel_body: float = 24 + basic_depth

    l1i_label: float = 25 + basic_depth
    l1i_body: float = 26 + basic_depth

    frame: float = 27 + basic_depth
    die_bg: float = 28 + basic_depth


A100_SM_DEPTH = A100SMDepthConfig()


@dataclass
class A100SMBarPart:
    item: GroupAny
    body: Rect
    label: TypstText


@dataclass
class A100SMComputeColumnPart:
    item: GroupAny
    cells: GroupAny
    label_text: str


@dataclass
class A100SMSubPartitionPart:
    item: GroupAny
    panel: Rect
    l0_inst: A100SMBarPart
    warp_sched: A100SMBarPart
    dispatch_unit: A100SMBarPart
    register_file: A100SMBarPart
    compute_columns: list[A100SMComputeColumnPart]
    tensor_core: Rect
    tensor_label: TypstText
    ldst_group: GroupAny
    sfu_bar: A100SMBarPart


@dataclass
class GPUA100SMPart:
    item: GroupAny
    die_bg: Rect
    frame: Rect
    sm_tag: A100SMBarPart
    l1_inst: A100SMBarPart
    quadrant_group: GroupAny
    quadrants: list[A100SMSubPartitionPart]
    l1_data_shared: A100SMBarPart
    tex_group: GroupAny
    tex_bars: list[A100SMBarPart]


def _create_sm_bar(
    text: str,
    width: float,
    height: float,
    fill: str,
    stroke: str,
    body_depth: float,
    label_depth: float,
    label_scale: float = 0.72,
    label_color: str = FAColor.a100_label_light,
) -> A100SMBarPart:
    body = Rect(width, height)
    body.fill.set(color=fill, alpha=1.0)
    body.stroke.set(color=stroke, alpha=1.0)
    body.radius.set(0.004)
    _set_depth(body, body_depth)

    label = _make_label(
        text,
        scale=label_scale,
        color=label_color,
        depth=label_depth,
    )
    label.points.move_to(body)

    return A100SMBarPart(item=Group(body, label), body=body, label=label)


def _create_sm_compute_column(
    width: float,
    height: float,
    rows: int,
    fill: str,
    stroke: str,
    text: str,
    cell_depth: float,
    label_depth: float,
    text_scale: float = 0.36,
) -> A100SMComputeColumnPart:
    gap = 0.006
    cell_h = (height - (rows - 1) * gap) / rows

    items = []
    for _ in range(rows):
        cell = Rect(width, cell_h)
        cell.fill.set(color=fill, alpha=1.0)
        cell.stroke.set(color=stroke, alpha=1.0)
        cell.radius.set(0.0025)
        _set_depth(cell, cell_depth)

        label = _make_label(
            text,
            scale=text_scale,
            color=FAColor.a100_label_light,
            depth=label_depth,
        )

        # 自动限高/限宽，避免列内文字互相重叠
        max_w = width * 0.82
        max_h = cell_h * 0.40
        cur_w = max(label.points.box.width, 1e-6)
        cur_h = max(label.points.box.height, 1e-6)

        if cur_w > 1e-5 and cur_h > 1e-5:
            fit_ratio = min(max_w / cur_w, max_h / cur_h)
            label.points.scale(min(1.0, fit_ratio * 0.95))
        else:
            # Typst 尺寸异常时的兜底缩放
            label.points.scale(0.22)

        label.points.move_to(cell.points.box.center + DOWN * (cell_h * 0.02))
        items.append(Group(cell, label))

    cells = Group.from_iterable(items)
    cells.points.arrange(DOWN, buff=gap)

    return A100SMComputeColumnPart(item=cells, cells=cells, label_text=text)


def _create_sm_subpartition(panel_w: float, panel_h: float) -> A100SMSubPartitionPart:
    panel = Rect(panel_w, panel_h)
    panel.fill.set(color=FAColor.a100_sm_panel_fill, alpha=1.0)
    panel.stroke.set(color=FAColor.a100_sm_panel_stroke, alpha=1.0)
    panel.radius.set(0.004)
    _set_depth(panel, A100_SM_DEPTH.panel_body)

    inner_w = panel_w - 0.08
    l0_h = panel_h * 0.13
    warp_h = panel_h * 0.10
    dispatch_h = panel_h * 0.10
    reg_h = panel_h * 0.18
    ldst_h = panel_h * 0.12

    l0_inst = _create_sm_bar(
        "L0 Instruction Cache",
        inner_w,
        l0_h,
        fill=FAColor.a100_sm_l0i_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.bar_body,
        label_depth=A100_SM_DEPTH.bar_label,
        label_scale=0.80,
    )
    warp_sched = _create_sm_bar(
        "Warp Scheduler (32 thread/clk)",
        inner_w,
        warp_h,
        fill=FAColor.a100_sm_warp_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.bar_body,
        label_depth=A100_SM_DEPTH.bar_label,
        label_scale=0.80,
    )
    dispatch_unit = _create_sm_bar(
        "Dispatch Unit (32 thread/clk)",
        inner_w,
        dispatch_h,
        fill=FAColor.a100_sm_dispatch_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.bar_body,
        label_depth=A100_SM_DEPTH.bar_label,
        label_scale=0.70,
    )
    register_file = _create_sm_bar(
        "Register File (16,384 $times$ 32-bit)",
        inner_w,
        reg_h,
        fill=FAColor.a100_sm_register_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.bar_body,
        label_depth=A100_SM_DEPTH.bar_label,
        label_scale=0.80,
    )

    top_stack = Group(l0_inst.item, warp_sched.item, dispatch_unit.item, register_file.item)
    top_stack.points.arrange(DOWN, buff=0.01)

    compute_h = panel_h - 0.12 - top_stack.points.box.height - ldst_h - 0.03
    if compute_h <= 0.45:
        compute_h = 0.45

    ratios = [1.20, 1.20, 1.30, 1.30, 1.40, 2.00]
    gap = 0.008
    unit = (inner_w - gap * (len(ratios) - 1)) / sum(ratios)
    widths = [r * unit for r in ratios]

    col_specs = [
        ("INT32", FAColor.a100_sm_int32_fill),
        ("INT32", FAColor.a100_sm_int32_fill),
        ("FP32", FAColor.a100_sm_fp32_fill),
        ("FP32", FAColor.a100_sm_fp32_fill),
        ("FP64", FAColor.a100_sm_fp64_fill),
    ]
    compute_columns = [
        _create_sm_compute_column(
            width=widths[i],
            height=compute_h,
            rows=6,
            fill=col_specs[i][1],
            stroke=FAColor.a100_sm_panel_stroke,
            text=col_specs[i][0],
            cell_depth=A100_SM_DEPTH.compute_cell,
            label_depth=A100_SM_DEPTH.compute_label,
            text_scale=0.8,
        )
        for i in range(5)
    ]

    tensor_core = Rect(widths[5], compute_h)
    tensor_core.fill.set(color=FAColor.a100_sm_tensor_fill, alpha=1.0)
    tensor_core.stroke.set(color=FAColor.a100_sm_panel_stroke, alpha=1.0)
    tensor_core.radius.set(0.003)
    _set_depth(tensor_core, A100_SM_DEPTH.tensor_body)

    tensor_label = _make_label(
        "TENSOR CORE",
        scale=0.62,
        color=FAColor.a100_label_light,
        depth=A100_SM_DEPTH.tensor_label,
    )
    tensor_label.points.move_to(tensor_core)

    compute_group = Group.from_iterable([part.item for part in compute_columns])
    compute_group.points.arrange(RIGHT, buff=gap)

    tensor_group = Group(tensor_core, tensor_label)
    compute_band = Group(compute_group, tensor_group)
    compute_band.points.arrange(RIGHT, buff=gap)

    ldst_count = 8
    row_gap = 0.008
    sfu_w = inner_w * 0.18
    ldst_total_w = inner_w - sfu_w - row_gap
    ldst_w = (ldst_total_w - row_gap * (ldst_count - 1)) / ldst_count

    ldst_parts = [
        _create_sm_bar(
            "LD/ST",
            ldst_w,
            ldst_h,
            fill=FAColor.a100_sm_ldst_fill,
            stroke=FAColor.a100_sm_panel_stroke,
            body_depth=A100_SM_DEPTH.ldst_body,
            label_depth=A100_SM_DEPTH.ldst_label,
            label_scale=0.50,
        )
        for _ in range(ldst_count)
    ]
    ldst_group = Group.from_iterable(part.item for part in ldst_parts)
    ldst_group.points.arrange(RIGHT, buff=row_gap)

    sfu_bar = _create_sm_bar(
        "SFU",
        sfu_w,
        ldst_h,
        fill=FAColor.a100_sm_sfu_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.ldst_body,
        label_depth=A100_SM_DEPTH.ldst_label,
        label_scale=0.60,
    )
    bottom_row = Group(ldst_group, sfu_bar.item)
    bottom_row.points.arrange(RIGHT, buff=row_gap)

    content = Group(top_stack, compute_band, bottom_row)
    content.points.arrange(DOWN, buff=0.01)
    content.points.align_to(panel, UP).shift(DOWN * 0.05)
    content.points.shift(RIGHT * (panel.points.box.center[0] - content.points.box.center[0]))

    item = Group(panel, content)

    return A100SMSubPartitionPart(
        item=item,
        panel=panel,
        l0_inst=l0_inst,
        warp_sched=warp_sched,
        dispatch_unit=dispatch_unit,
        register_file=register_file,
        compute_columns=compute_columns,
        tensor_core=tensor_core,
        tensor_label=tensor_label,
        ldst_group=ldst_group,
        sfu_bar=sfu_bar,
    )


def create_GPU_A100_SM(
    width: float = 12.8,
    height: float = 12.0,
) -> GPUA100SMPart:
    """
    创建 A100 单个 SM 架构图（仿照官方示意图），返回 dataclass。
    """
    if width <= 6 or height <= 6:
        raise ValueError("width/height 过小，无法构建 A100 SM 架构图")

    die_bg = Rect(width, height)
    die_bg.fill.set(color=FAColor.a100_die_bg_fill, alpha=1.0)
    die_bg.stroke.set(color=FAColor.a100_die_bg_stroke, alpha=1.0)
    die_bg.radius.set(0.006)
    _set_depth(die_bg, A100_SM_DEPTH.die_bg)

    frame = Rect(width - 0.16, height - 0.16)
    frame.fill.set(color=FAColor.a100_sm_shell_fill, alpha=1.0)
    frame.stroke.set(color=FAColor.a100_sm_shell_stroke, alpha=1.0)
    frame.radius.set(0.006)
    frame.points.move_to(die_bg)
    _set_depth(frame, A100_SM_DEPTH.frame)

    content_w = frame.points.box.width - 0.20
    l1i_h = 0.70
    l1d_h = 0.70
    tex_h = 0.85
    quad_gap = 0.12

    quad_area_h = frame.points.box.height - 0.20 - l1i_h - l1d_h - tex_h - 3 * 0.06
    quad_h = (quad_area_h - quad_gap) / 2
    quad_w = (content_w - quad_gap) / 2
    if quad_h <= 1.6:
        raise ValueError("当前 height 太小，不足以容纳 SM 子分区")

    sm_tag = _create_sm_bar(
        text="SM",
        width=1.30,
        height=0.55,
        fill=FAColor.a100_sm_shell_fill,
        stroke=FAColor.a100_sm_shell_stroke,
        body_depth=A100_SM_DEPTH.sm_tag_body,
        label_depth=A100_SM_DEPTH.sm_tag_label,
        label_scale=0.95,
    )

    l1_inst = _create_sm_bar(
        text="L1 Instruction Cache",
        width=content_w,
        height=l1i_h,
        fill=FAColor.a100_sm_l1i_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.l1i_body,
        label_depth=A100_SM_DEPTH.l1i_label,
        label_scale=0.62,
    )

    quadrants = [_create_sm_subpartition(quad_w, quad_h) for _ in range(4)]
    quadrant_group = Group.from_iterable(part.item for part in quadrants)
    quadrant_group.points.arrange_in_grid(n_rows=2, n_cols=2, buff=quad_gap)

    l1_data_shared = _create_sm_bar(
        text="192KB L1 Data Cache / Shared Memory",
        width=content_w,
        height=l1d_h,
        fill=FAColor.a100_sm_l1d_fill,
        stroke=FAColor.a100_sm_panel_stroke,
        body_depth=A100_SM_DEPTH.l1d_body,
        label_depth=A100_SM_DEPTH.l1d_label,
        label_scale=0.90,
    )

    tex_gap = 0.03
    tex_w = (content_w - tex_gap * 3) / 4
    tex_bars = [
        _create_sm_bar(
            text="Tex",
            width=tex_w,
            height=tex_h,
            fill=FAColor.a100_sm_tex_fill,
            stroke=FAColor.a100_sm_panel_stroke,
            body_depth=A100_SM_DEPTH.tex_body,
            label_depth=A100_SM_DEPTH.tex_label,
            label_scale=0.70,
        )
        for _ in range(4)
    ]
    tex_group = Group.from_iterable(part.item for part in tex_bars)
    tex_group.points.arrange(RIGHT, buff=tex_gap)

    body_stack = Group(l1_inst.item, quadrant_group, l1_data_shared.item, tex_group)
    body_stack.points.arrange(DOWN, buff=0.06)
    body_stack.points.move_to(frame)

    sm_tag.item.points.align_to(frame, UL).shift(RIGHT * 0.06 + DOWN * 0.06)

    item = Group(die_bg, frame, body_stack, sm_tag.item)

    return GPUA100SMPart(
        item=item,
        die_bg=die_bg,
        frame=frame,
        sm_tag=sm_tag,
        l1_inst=l1_inst,
        quadrant_group=quadrant_group,
        quadrants=quadrants,
        l1_data_shared=l1_data_shared,
        tex_group=tex_group,
        tex_bars=tex_bars,
    )
