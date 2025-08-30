import pytest
from calango.xrefs import Target, Kind

def test_recursion_depth():
    with pytest.raises(ValueError) as excinfo:
        _ = Target('something')

    assert "Kind of 'something' is unknown" in str(excinfo.value)