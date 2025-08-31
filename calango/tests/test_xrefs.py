import pytest
from calango.xrefs import Target, Kind
from bs4 import BeautifulSoup

@pytest.mark.parametrize('ident, expected', [
    ('ch_data_model', Kind.CHAPTER),
    ('data_model_emulating_sec', Kind.SECTION)
])
def test_kind(ident, expected):
    target = Target(ident)
    assert target.kind == expected

@pytest.mark.parametrize('ident, expected', [
    ('ch_data_model', (1, 1)),
    ('ch_seq_methods', (2, 12)),
    ('ch_descriptors', (3, 23)),
    ('data_model_emulating_sec', (1, 1))
])
def test_volume_and_chapter(ident, expected):
    target = Target(ident)
    assert target.volume, target.chapter == expected

def test_unknown_kind():
    with pytest.raises(ValueError) as excinfo:
        Target('something')

    assert "Kind of 'something' is unknown" in str(excinfo.value)

def test_get_section_title():
    html = '''<h3 id="typeddict_sec"><a class="link" href="#typeddict_sec">15.3. TypedDict</a></h3>'''
    root = BeautifulSoup(html, 'html.parser')
    target = Target('typeddict_sec')
    assert target.get_section_title(root) == '15.3. TypedDict'
