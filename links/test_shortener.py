from pytest import mark

from shortener import parse_htaccess, choose, load_redirects
from shortener import gen_short, gen_unused_short


PARSED_SAMPLE_HTACCESS = [
    ('book', 'https://www.oreilly.com/.../9781492056348/'),
    ('home', 'https://www.fluentpython.com/'),
    ('1-20', 'https://www.fluentpython.com/'),
    ('ora', 'https://www.oreilly.com/.../9781492056348/'),
    ('2-10', 'http://example.com/'),
    ('10-2', 'http://example.com/'),
]


def test_parse_htaccess(shared_datadir):
    with open(shared_datadir / 'sample.htaccess') as fp:
        text = fp.read()
    res = list(parse_htaccess(text))
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
    expected = {
        'home': 'https://www.fluentpython.com/',
        '1-20': 'https://www.fluentpython.com/',
        '2-10': 'http://example.com/',
        '10-2': 'http://example.com/',
        'book': 'https://www.oreilly.com/.../9781492056348/',
        'ora': 'https://www.oreilly.com/.../9781492056348/',
    }
    redirects, _ = load_redirects(PARSED_SAMPLE_HTACCESS)
    assert redirects == expected


def test_load_redirect_targets():
    expected = {
        'https://www.fluentpython.com/': 'home',
        'https://www.oreilly.com/.../9781492056348/': 'ora',
        'http://example.com/': '2-10',
    }
    _, targets = load_redirects(PARSED_SAMPLE_HTACCESS)
    assert targets == expected


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
