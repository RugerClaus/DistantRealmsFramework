# draw.draw.py

opengl = None
glu = None


def init(gl, glutils):
    global opengl, glu

    opengl = gl
    glu = glutils