#!/usr/bin/env jython
# NOTE: Jython is still Python 2.7 in late2020

"""
In the Jython registry file there is this line:

python.security.respectJavaAccessibility = true

Set this to false and Jython provides access to non-public
fields, methods, and constructors of Java objects.
"""
from __future__ import print_function

import Confidential

message = Confidential('top secret text')
for name in dir(message):
    attr = getattr(message, name)
    if not callable(attr):  # non-methods only
        print(name + '\t=', attr)
