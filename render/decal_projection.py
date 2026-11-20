"""弹孔贴花投影的纯数学辅助函数。

这些函数只负责几何/排序/采样的数值计算，不持有任何渲染器状态，
便于在 CPU 侧做单元测试。
"""

import math


def _clamp(value, low, high):
    """把 value 限制到 [low, high]。"""
    if value < low:
        return low
    if value > high:
        return high
    return value


def _as_extent(value):
    """把标量或三元组统一成 (x, y, z) 扩展量。"""
    if isinstance(value, (int, float)):
        value = (value, value, value)
    return tuple(value)


def projection_bounds(center, size, normal_extent):
    """投影盒。

    投影盒在切线平面（X/Z）上按 ``size`` 扩展，沿表面法线（Y）按
    ``normal_extent`` 扩展。斜面缺块正是因为法线方向没有扩展，这里把
    两部分分开处理，返回 ``(xmin, ymin, zmin, xmax, ymax, zmax)``。
    """
    cx, cy, cz = center
    sx, sy, sz = _as_extent(size)
    nx, ny, nz = _as_extent(normal_extent)
    # 法线方向的扩展量与切线方向叠加，避免斜面上投影盒穿出表面。
    return (
        cx - sx, cy - ny, cz - sz,
        cx + sx, cy + ny, cz + sz,
    )


def decal_depth_bias(base, slope):
    """深度偏移。

    贴花需要独立于不透明物体的深度偏移；偏移随表面斜率增大，避免
    掠射角处与墙面发生 z-fighting。
    """
    return float(base) * float(slope)


def skinned_decal_position(position, bone_offset):
    """蒙皮贴花位置。

    贴花位置随骨骼变换一起移动，否则角色动画时贴花会停留在静态位置。
    """
    return tuple(p + o for p, o in zip(position, bone_offset))


def angle_fade(dot_value, threshold):
    """角度淡出。

    先用 clamp 把点积限制到 ``[threshold, 1]``，再做归一化淡出：
    背面点积为负时不会透出黑斑，正面也不会超过 1。
    """
    threshold = _clamp(float(threshold), 0.0, 1.0)
    if threshold >= 1.0:
        return 1.0 if dot_value >= 1.0 else 0.0
    d = _clamp(float(dot_value), threshold, 1.0)
    return (d - threshold) / (1.0 - threshold)


def decal_sort_key(layer, distance):
    """贴花排序。

    先按层（同一面墙上的血迹属于同一层），层内按距离由远到近绘制，
    即距离取负。
    """
    return (layer, -distance)


def camera_decal_key(camera_id):
    """多相机缓冲键。

    每个相机（分屏/左右眼）使用独立缓冲，避免共享时数量不一致。
    """
    return camera_id


def atlas_uv(uv, border):
    """atlas 边界。

    把 UV 夹在 ``[border, 1 - border]``，采样不会越过 atlas 子图边界
    而取到相邻图案。
    """
    u, v = uv
    low = float(border)
    high = 1.0 - low
    if high < low:
        low = high = 0.5
    return (_clamp(float(u), low, high), _clamp(float(v), low, high))


def decal_ready(loaded, total):
    """贴花就绪。

    只有全部资源加载完成才允许提交绘制，避免异步生成期间闪烁。
    """
    return int(loaded) >= max(int(total), 0)


def tangent_space_normal(normal, tangent):
    """切线空间法线。

    把世界空间法线投影到切线方向（点积），着色时用切线空间方向，
    避免光照方向相反。
    """
    return float(sum(n * t for n, t in zip(normal, tangent)))


def fade_out(remaining, max_size):
    """淡出。

    超出性能档上限的贴花按剩余额度淡出回收，而不是直接消失。
    """
    max_size = float(max_size)
    if max_size <= 0.0:
        return 0.0
    return _clamp(float(remaining) / max_size, 0.0, 1.0)


def decal_lifetime(age, max_age):
    """生命周期。"""
    return float(age) < float(max_age)


def depth_offset(depth, bias):
    """深度偏移值。

    贴花在深度缓冲中向相机方向前移一个独立偏移量。
    """
    return float(depth) - float(bias)


def projected_area(size, angle_cos):
    """投影面积。

    面积随入射角余弦衰减；余弦钳制到 ``[0, 1]``，背面不产生负面积。
    """
    return float(size) * _clamp(float(angle_cos), 0.0, 1.0)


def clip_rect(rect, bounds):
    """矩形裁剪。

    ``rect`` 与 ``bounds`` 均为 ``(x, y, w, h)``，返回交集；不相交时
    返回零尺寸矩形。
    """
    rx, ry, rw, rh = rect
    bx, by, bw, bh = bounds
    x0 = max(rx, bx)
    y0 = max(ry, by)
    x1 = min(rx + rw, bx + bw)
    y1 = min(ry + rh, by + bh)
    return (x0, y0, max(0, x1 - x0), max(0, y1 - y0))


def decal_id(seed, index):
    """贴花 id。"""
    return f"{seed}:{index}"
