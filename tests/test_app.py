import pytest

def test_success():
    assert 4 == 4

def test_fail():
    assert 3 == 4

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
