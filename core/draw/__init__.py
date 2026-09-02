#__init__.py

from OpenGL import GL, GLU
from . import draw

def init():
    draw.init(GL,GLU)