#!/usr/bin/env python

from distutils.core import setup

long_description = """
Get mac address, correct and return in required format
DOES NOT CHECK THE INPUT MAC ADDRESS FORMAT, just delete invalid characters and check len = 12
:param mac: mac address
:param delimiter: separator character
:param chunk: the number of characters before the separator output, mast be in [1, 2, 3, 4, 6]. 0 or None for output without delimiter
:param capital: lowercase or uppercase return output str. default lowercase
:return: mac address in required format

example:
print(mac_4mater('ab.bg.55.55.55.53', delimiter='.', chunk=4, capital=False))
ValueError: Invalid mac address ab.bg.55.55.55.53

print(mac_4mater('ab.bc.55.55.55.53', delimiter='.', chunk=4))
abbc.5555.5553

print(mac_4mater('ab.bc55.55.55bbbbbbbbbbbbbb.53', delimiter=':', chunk=4, capital=False))
ValueError: Invalid mac address ab.bc55.55.55bbbbbbbbbbbbbb.53

print(mac_4mater('ABrrrrrrrrrrrr.bc.55.55.55.53', delimiter='-', chunk=2, capital=True))
AB-BC-55-55-55-53

print(mac_4mater('AB.bc.55.55.55.53', delimiter=':', chunk=2, capital=True))
AB:BC:55:55:55:53
"""

setup(

name='mac-4mater',
version='1.0',
py_modules=['mac_4mater'],
author='myxx921',
author_email='myxx921@gmail.com',
url='https://github.com/myxx921/mac_4mater',
description='convert mac to required format',
long_description=long_description
)