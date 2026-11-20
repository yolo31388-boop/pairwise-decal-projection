import pytest
from render import decal_projection as mod

CASES = [
    ("bounds", 'm.projection_bounds((0, 0, 0), 2, 1) == (-2, -1, -2, 2, 1, 2)'),
    ("bias", 'm.decal_depth_bias(0.01, 2) == approx(0.02)'),
    ("skinned", 'm.skinned_decal_position((1, 2), (2, 3)) == (3, 5)'),
    ("fade", 'm.angle_fade(0.8, 0.2) == approx(0.75)'),
    ("sort", 'm.decal_sort_key(2, 5) == (2, -5)'),
    ("camkey", 'm.camera_decal_key("L") == "L"'),
    ("atlas", 'm.atlas_uv((0.05, 0.95), 0.1) == approx((0.1, 0.9))'),
    ("ready", 'm.decal_ready(3, 3) is True'),
    ("tangent", 'm.tangent_space_normal((0, 1, 0), (1, 0, 0)) == 0'),
    ("fout", 'm.fade_out(2, 4) == approx(0.5)'),
    ("life", 'm.decal_lifetime(1, 2) is True'),
    ("depth", 'm.depth_offset(5, 1) == approx(4.0)'),
    ("area", 'm.projected_area(4, 0.5) == approx(2.0)'),
    ("clip", 'm.clip_rect((0, 0, 10, 10), (2, 2, 5, 5)) == (2, 2, 5, 5)'),
    ("id", 'm.decal_id(3, 2) == "3:2"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
