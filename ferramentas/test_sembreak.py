import pytest

from sembreak import sembreak

@pytest.mark.parametrize("given,expected", [
    ('aaa bbb.', 'aaa bbb.'),
    ('aaa bbb. Ccc', 'aaa bbb.\nCcc'),
    ('aaa bbb.  Ccc', 'aaa bbb.\nCcc'),
    ('aaa bbb. ccc', 'aaa bbb. ccc'),
])
def test_sembreak(given:str, expected:str):
    res = sembreak(given)
    assert res == expected
