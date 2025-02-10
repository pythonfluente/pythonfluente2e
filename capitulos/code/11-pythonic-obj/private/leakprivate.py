#!/usr/bin/env jython
# NOTE: Jython is still Python 2.7 in late2020

from __future__ import print_function

from java.lang.reflect import Modifier
import Confidential

message = Confidential('top secret text')
fields = Confidential.getDeclaredFields()
for field in fields:
    # list private fields only
    if Modifier.isPrivate(field.getModifiers()):
        field.setAccessible(True) # break the lock
        print('field:', field)
        print('\t', field.getName(), '=', field.get(message))
