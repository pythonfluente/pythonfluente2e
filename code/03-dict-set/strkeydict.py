"""StrKeyDict always converts non-string keys to `str`

Test for initializer: keys are converted to `str`.

    >>> d = StrKeyDict([(2, 'two'), ('4', 'four')])
    >>> sorted(d.keys())
    ['2', '4']

Tests for item retrieval using `d[key]` notation::

    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

Tests for item retrieval using `d.get(key)` notation::

    >>> d.get('2')
    'two'
    >>> d.get(4)
    'four'
    >>> d.get(1, 'N/A')
    'N/A'

Tests for the `in` operator::

    >>> 2 in d
    True
    >>> 1 in d
    False

Test for item assignment using non-string key::

    >>> d[0] = 'zero'
    >>> d['0']
    'zero'

Tests for update using a `dict` or a sequence of pairs::

    >>> d.update({6:'six', '8':'eight'})
    >>> list(d.keys())
    ['2', '4', '0', '6', '8']
    >>> d.update([(10, 'ten'), ('12', 'twelve')])
    >>> list(d.keys())
    ['2', '4', '0', '6', '8', '10', '12']
    >>> d.update([1, 3, 5])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: ...iterable...

"""
# tag::STRKEYDICT[]

import collections


class StrKeyDict(collections.UserDict):  # <1>

    def __missing__(self, key):  # <2>
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data  # <3>

    def __setitem__(self, key, item):
        self.data[str(key)] = item   # <4>
# end::STRKEYDICT[]
