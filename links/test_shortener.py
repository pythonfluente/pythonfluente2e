from pytest import mark

from shortener import parse_htaccess, choose, load_redirects


HTACCESS_1 = """
ErrorDocument 404 /404.html

# main resources
RedirectTemp /book	https://www.oreilly.com/.../9781492056348/
RedirectTemp /home	https://www.fluentpython.com/  # extra content site

# duplicate targets
RedirectTemp /1-20	https://www.fluentpython.com/
RedirectTemp /ora	https://www.oreilly.com/.../9781492056348/
RedirectTemp /2-10	http://example.com/
RedirectTemp /10-2	http://example.com/
"""

PARSED_HTACCESS_1 = [
        ('book', 'https://www.oreilly.com/.../9781492056348/'),
        ('home', 'https://www.fluentpython.com/'),
        ('1-20', 'https://www.fluentpython.com/'),
        ('ora', 'https://www.oreilly.com/.../9781492056348/'),
        ('2-10', 'http://example.com/'),
        ('10-2', 'http://example.com/'),
    ]

def test_parse_htaccess():
    res = list(parse_htaccess(HTACCESS_1))
    assert res == PARSED_HTACCESS_1

@mark.parametrize('a,b,expected', [
    ('a', 'b', 'a'),
    ('b', 'a', 'a'),
    ('aa', 'a', 'a'),
    ('a-a', 'aaa', 'aaa'),
    ('2-10', '10-2', '2-10'),
    ('p-1', '1-1', 'p-1'),
])
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
    redirects, _ = load_redirects(PARSED_HTACCESS_1)
    assert redirects == expected


def test_load_redirect_targets():
    expected = {
        'https://www.fluentpython.com/' : 'home',
        'https://www.oreilly.com/.../9781492056348/' : 'ora',
        'http://example.com/' : '2-10',
    }
    _, targets = load_redirects(PARSED_HTACCESS_1)
    assert targets == expected