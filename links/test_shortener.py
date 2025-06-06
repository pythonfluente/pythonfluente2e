from pytest import mark

from shortener import parse_htaccess, choose


HTACCESS_1 = """
ErrorDocument 404 /404.html

# main resources
RedirectTemp /book	https://www.oreilly.com/.../9781492056348/
RedirectTemp /home	https://www.fluentpython.com/  # extra content site

# duplicate targets
RedirectTemp /1-20	https://www.fluentpython.com/
RedirectTemp /ora	https://www.oreilly.com/.../9781492056348/

"""

PARSED_HTACCESS_1 = [
        ('book', 'https://www.oreilly.com/.../9781492056348/'),
        ('home', 'https://www.fluentpython.com/'),
        ('1-20', 'https://www.fluentpython.com/'),
        ('ora', 'https://www.oreilly.com/.../9781492056348/'),
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


# def test_load_redirects():
#     expected = {
#         'home': 'https://www.fluentpython.com/',
#         'ora': 'https://www.oreilly.com/.../9781492056348/'
#     }
#     redirects, _ = load_redirects(PARSED_HTACCESS_1)
#     assert redirects == expected
