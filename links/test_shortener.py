from pytest import mark

from shortener import parse_htaccess, choose, load_redirects
from shortener import gen_short, gen_unused_short, shorten_one, ShortenResult


SAMPLE_HTACCESS = """
ErrorDocument 404 /404.html

# main resources
RedirectTemp /book	https://www.oreilly.com/.../9781492056348/
RedirectTemp /home	https://www.fluentpython.com/  # extra content site

# duplicate targets
RedirectTemp /1-20	https://www.fluentpython.com/
RedirectTemp /ora	https://www.oreilly.com/.../9781492056348/
RedirectTemp /2-10	http://example.com/
RedirectTemp /10-2	http://example.com/

# shortened
RedirectTemp /22    http://firstshortened.co
"""

FROZEN_TIME = '2025-06-07 01:02:03'

UPDATED_SAMPLE_HTACCESS = SAMPLE_HTACCESS + f"""
# appended: {FROZEN_TIME}
RedirectTemp /23 https://new.site/
RedirectTemp /24 https://other.new.site/
"""


PARSED_SAMPLE_HTACCESS = [
    ('book', 'https://www.oreilly.com/.../9781492056348/'),
    ('home', 'https://www.fluentpython.com/'),
    ('1-20', 'https://www.fluentpython.com/'),
    ('ora', 'https://www.oreilly.com/.../9781492056348/'),
    ('2-10', 'http://example.com/'),
    ('10-2', 'http://example.com/'),
    ('22', 'http://firstshortened.co')
]

# straightforward mapping of .htaccess; some targets may be duplicated.
SAMPLE_REDIRECTS = {
    'home': 'https://www.fluentpython.com/',
    '1-20': 'https://www.fluentpython.com/',
    '2-10': 'http://example.com/',
    '10-2': 'http://example.com/',
    'book': 'https://www.oreilly.com/.../9781492056348/',
    'ora': 'https://www.oreilly.com/.../9781492056348/',
    '22': 'http://firstshortened.co',
}

# the value must be shortest path for that target in the .htaccess
SAMPLE_TARGETS = {
    'https://www.fluentpython.com/': 'home',
    'https://www.oreilly.com/.../9781492056348/': 'ora',
    'http://example.com/': '2-10',
    'http://firstshortened.co': '22',
}



def test_parse_htaccess():
    res = list(parse_htaccess(SAMPLE_HTACCESS))
    assert res == PARSED_SAMPLE_HTACCESS


@mark.parametrize(
    'a,b,expected',
    [
        ('a', 'b', 'a'),
        ('b', 'a', 'a'),
        ('aa', 'a', 'a'),
        ('a-a', 'aaa', 'aaa'),
        ('2-10', '10-2', '2-10'),
        ('p-1', '1-1', 'p-1'),
    ],
)
def test_choose(a, b, expected):
    res = choose(a, b)
    assert res == expected


def test_load_redirects():
   redirects, _ = load_redirects(PARSED_SAMPLE_HTACCESS)
   assert redirects == SAMPLE_REDIRECTS


def test_load_redirect_targets():
    _, targets = load_redirects(PARSED_SAMPLE_HTACCESS)
    assert targets == SAMPLE_TARGETS


@mark.parametrize(
    'target,path,new',
    [
        ('https://www.fluentpython.com/', 'home', False),
        ('https://new.site/', '23', True),
    ],
)
def test_shorten(target, path, new):
    expected = ShortenResult(target, path, new)
    redirects = dict(SAMPLE_REDIRECTS)
    targets = dict(SAMPLE_TARGETS)
    result = shorten_one(target, gen_unused_short(redirects), redirects, targets)
    assert result == expected
    updated = redirects.keys() - SAMPLE_REDIRECTS.keys()
    if new:
        assert len(updated) == 1
        new_path = updated.pop()
        assert new_path == path
        assert redirects == SAMPLE_REDIRECTS | {new_path: target}
        assert targets == SAMPLE_TARGETS | {target: new_path}
    else:
        assert len(updated) == 0
        assert redirects == SAMPLE_REDIRECTS
        assert targets == SAMPLE_TARGETS


def test_update_htaccess():
    pass


def test_gen_short():
    expected = '222 223 224 225 226 227 228 229 22a 22b'.split()
    gen = gen_short(3)
    res = [next(gen) for _ in range(10)]
    assert res == expected


def test_gen_unused_short():
    redirects = {'22': 'u1', '23': 'u2', '25': 'u4'}
    gen = gen_unused_short(redirects)
    assert next(gen) == '24'
    assert next(gen) == '26'
