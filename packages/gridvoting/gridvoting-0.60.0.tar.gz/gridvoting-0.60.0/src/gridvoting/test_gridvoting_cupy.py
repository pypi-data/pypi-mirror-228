import pytest

def test_module():
    import gridvoting
    assert (not gridvoting.use_cupy) == (gridvoting.xp is gridvoting.np)
    print("use_cupy is ",gridvoting.use_cupy)
