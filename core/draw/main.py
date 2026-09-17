import pygame,sys,numpy
from helper import sine
from random import randint
from renderer import Renderer
from shader import Shader
from geometry.geometry import Geometry
from texture import Texture

pygame.init()
pygame.font.init()

def normalized_color(color):
    return tuple(channel / 255.0 for channel in color)

win = pygame.Window(title="Assweepay",size=(960,540),position=pygame.WINDOWPOS_UNDEFINED,fullscreen=False,opengl=True,resizable=True)
win.set_icon(pygame.image.load("../ball.png"))
clock  = pygame.time.Clock()
renderer = Renderer(win)
Geometry.init(renderer)
renderer.update_viewport()

rw, rh = renderer.resolution

chairvirt = Geometry.rect(
    rw * 0.5,
    rh * 0.5,
    6,
    20,
    normalized_color((255,0,0,255))
)
chairhorz = Geometry.rect(
    rw * 0.5,
    rh * 0.5,
    20,
    6,
    normalized_color((255,0,0,255))
)

shader2 = Shader("shaders/plane.glsl","shaders/f.glsl")
cube1 = Geometry.cube(
    -0.2,
    -0.2,
    0.0,
    2.0,
    normalized_color((0, 0, 255, 255)),
    shader2
)
shader3 = Shader("shaders/plane.glsl","shaders/f.glsl")
ground = Geometry.plane(
    0.0,
    -1.0,
    0.0,
    100.0,
    100.0,
    normalized_color((0,200,0,255)),
    shader3
)

textureshader = Shader("shaders/texturev.glsl","shaders/texturef.glsl")

fps = clock.get_fps()

font = pygame.font.Font("../Roboto-Bold.ttf", 20)

surface = font.render(
    f"FPS: {fps:.0f}",
    True,
    (255, 255, 255)
)
texture = Texture(surface)

text = Geometry.texture(
    100,
    50,
    surface.get_width(),
    surface.get_height(),
    texture,
    textureshader
)

cube1.y = ground.y + cube1.size / 2
objects2d = []
objects2d.append(chairvirt)
objects2d.append(chairhorz)


objects3d = []
objects3d.append(cube1)
objects3d.append(ground)


def rectangle_factory(renderer, count):

    rw, rh = renderer.resolution

    shader = Shader("shaders/v.glsl","shaders/rectpulse.glsl")

    for i in range(count):
        rect = Geometry.rect(
            randint(20, rw - 20),
            randint(20, rh - 20),
            20,
            20,
            shader=shader
        )

        rect.color = (
            randint(0, 255) / 255.0,
            randint(0, 255) / 255.0,
            randint(0, 255) / 255.0,
            1.0
        )
        objects2d.append(rect)

def camera_controls():

    keys = pygame.key.get_pressed()

    yaw = numpy.radians(renderer.camera.yaw)
    pitch = numpy.radians(renderer.camera.pitch)

    forward = numpy.array([
        numpy.sin(yaw) * numpy.cos(pitch),
        0.0,
        -numpy.cos(yaw) * numpy.cos(pitch)
    ])

    right = numpy.array([
        numpy.cos(yaw),
        0.0,
        numpy.sin(yaw)
    ])

    if keys[pygame.K_w]:
        renderer.camera.position += forward * 0.1
    elif keys[pygame.K_s]:
        renderer.camera.position -= forward * 0.1

    if keys[pygame.K_a]:
        renderer.camera.position -= right * 0.1
    elif keys[pygame.K_d]:
        renderer.camera.position += right * 0.1

    if keys[pygame.K_LSHIFT]:
        renderer.camera.position[1] -= 0.1
    elif keys[pygame.K_SPACE]:
        renderer.camera.position[1] += 0.1


    renderer.camera.position[1] = max(
        ground.y + 1.0,
        renderer.camera.position[1]
    )

def spawn_rectangles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        rectangle_factory(renderer, 1)
    elif keys[pygame.K_2]:
        if len(objects2d) > 2:
            objects2d.pop(-1)

sensitivity = 0.1
paused = False

pygame.mouse.set_relative_mode(not paused)
pygame.mouse.set_visible(paused)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("The graphics card is finished cooking")
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWRESIZED:
            renderer.update_viewport()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

                pygame.mouse.set_relative_mode(not paused)
                pygame.mouse.set_visible(paused)

        if event.type == pygame.MOUSEMOTION and not paused:
            dx, dy = event.rel

            renderer.camera.yaw += dx * sensitivity
            renderer.camera.pitch += dy * sensitivity

    print("x: ", int(renderer.camera.position[0])," y: ", int(renderer.camera.position[1])," z: ", int(renderer.camera.position[2]))
    
    if not paused:
        camera_controls()
    spawn_rectangles()
    Geometry.update(objects2d)
    Geometry.update(objects3d)

    fps = clock.get_fps()

    surface = font.render(
        f"FPS: {fps:.0f}",
        True,
        (255, 255, 255)
    )

    texture.update(surface)

    current_time = pygame.time.get_ticks() / 1000.0
    renderer.clear(color=normalized_color((100,100,240,255)))
    for object in objects3d:
        renderer.render(object,current_time)
    for object in objects2d:
        renderer.render(object, current_time)

    renderer.render(text,current_time)
    
    win.flip()
    clock.tick(60)