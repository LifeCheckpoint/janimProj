"""
临时脏标记 patch，用于优化 detect_changes_of_all 的性能。
通过 monkey-patch Component.mark_refresh 自动收集脏 item，
使 detect_changes_of_all 只检查脏 item 和首次 track 的 item。

用法：
    from dirty_patch import install_dirty_patch, uninstall_dirty_patch
    # 在 construct() 开头
    install_dirty_patch()
    # 在 construct() 末尾（可选）
    uninstall_dirty_patch()
"""

from janim.components.component import Component
from janim.anims.timeline import Timeline

_dirty_items: set = set()
_orig_mark_refresh = Component.mark_refresh
_orig_detect = Timeline.detect_changes_of_all


def _patched_mark_refresh(self, func, *, recurse_up=False, recurse_down=False):
    ret = _orig_mark_refresh(self, func, recurse_up=recurse_up, recurse_down=recurse_down)
    if self.bind is not None:
        _dirty_items.add(self.bind.at_item)
    return ret


def _patched_detect(self):
    for item, appr in self.item_appearances.items():
        if appr.stack.prev_display is None or item in _dirty_items:
            appr.stack.detect_change(item, self.current_time)
    _dirty_items.clear()


def install_dirty_patch():
    Component.mark_refresh = _patched_mark_refresh
    Timeline.detect_changes_of_all = _patched_detect


def uninstall_dirty_patch():
    Component.mark_refresh = _orig_mark_refresh
    Timeline.detect_changes_of_all = _orig_detect
