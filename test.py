import pygame
from OpenGL import GL

pygame.init()

window = pygame.Window(
    title="OpenGL Test",
    size=(800, 600),
    opengl=True
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    GL.glClearColor(1.0, 0.0, 0.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    window.flip()