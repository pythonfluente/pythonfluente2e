"""
# tag::FUNC_DESCRIPTOR_DEMO[]

    >>> word = Text('forward')
    >>> word  # <1>
    Text('forward')
    >>> word.reverse()  # <2>
    Text('drawrof')
    >>> Text.reverse(Text('backward'))  # <3>
    Text('drawkcab')
    >>> type(Text.reverse), type(word.reverse)  # <4>
    (<class 'function'>, <class 'method'>)
    >>> [Text.reverse(x) for x in ['abc', (1, 2), Text('stressed')]]  # <5>
    ['cba', (2, 1), Text('desserts')]
    >>> Text.reverse.__get__(word)  # <6>
    <bound method Text.reverse of Text('forward')>
    >>> Text.reverse.__get__(None, Text)  # <7>
    <function Text.reverse at 0x...>
    >>> word.reverse  # <8>
    <bound method Text.reverse of Text('forward')>
    >>> word.reverse.__self__  # <9>
    Text('forward')
    >>> word.reverse.__func__ is Text.reverse  # <10>
    True

# end::FUNC_DESCRIPTOR_DEMO[]
"""

# tag::FUNC_DESCRIPTOR_EX[]
import collections


class Text(collections.UserString):

    def __repr__(self):
        return f'Text({self.data!r})'

    def reverse(self):
        return self[::-1]

# end::FUNC_DESCRIPTOR_EX[]
