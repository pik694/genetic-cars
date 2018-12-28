"""
Module providing car methods
Works with pybox2d
"""


import sys
from os import path

TRIANGLE_GENES = 7
TRIANGLES = 5

MAX_DURATION = 60
MAX_SAME_POSITION = 125

sys.path.append(path.abspath('../pybox2d'))
