import math

def projection_bounds(center, size, normal_extent):
    """投影盒。"""
    raise NotImplementedError("TODO: projection_bounds")

def decal_depth_bias(base, slope):
    """深度偏移。"""
    raise NotImplementedError("TODO: decal_depth_bias")

def skinned_decal_position(position, bone_offset):
    """蒙皮贴花位置。"""
    raise NotImplementedError("TODO: skinned_decal_position")

def angle_fade(dot_value, threshold):
    """角度淡出。"""
    raise NotImplementedError("TODO: angle_fade")

def decal_sort_key(layer, distance):
    """贴花排序。"""
    raise NotImplementedError("TODO: decal_sort_key")

def camera_decal_key(camera_id):
    """多相机缓冲键。"""
    raise NotImplementedError("TODO: camera_decal_key")

def atlas_uv(uv, border):
    """atlas 边界。"""
    raise NotImplementedError("TODO: atlas_uv")

def decal_ready(loaded, total):
    """贴花就绪。"""
    raise NotImplementedError("TODO: decal_ready")

def tangent_space_normal(normal, tangent):
    """切线空间法线。"""
    raise NotImplementedError("TODO: tangent_space_normal")

def fade_out(remaining, max_size):
    """淡出。"""
    raise NotImplementedError("TODO: fade_out")

def decal_lifetime(age, max_age):
    """生命周期。"""
    raise NotImplementedError("TODO: decal_lifetime")

def depth_offset(depth, bias):
    """深度偏移值。"""
    raise NotImplementedError("TODO: depth_offset")

def projected_area(size, angle_cos):
    """投影面积。"""
    raise NotImplementedError("TODO: projected_area")

def clip_rect(rect, bounds):
    """矩形裁剪。"""
    raise NotImplementedError("TODO: clip_rect")

def decal_id(seed, index):
    """贴花 id。"""
    raise NotImplementedError("TODO: decal_id")
