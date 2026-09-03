class Surface:

    def __init__(self, system, size=(1, 1), alpha=False, screen=False):
        print("SURFACE INIT:", size, "SCREEN:", screen)
        if size == (1600, 900):
            import traceback
            traceback.print_stack()
        self.system = system
        self.size = size
        self.alpha = alpha
        self.screen = screen

        self.texture = None
        self.framebuffer = 0 if screen else None
        self.mask = None

        if not screen:
            self.system.backend.draw.create_surface(self)

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_size(self):
        return self.size

    def get_rect(self, center=None,centerx=None,centery=None, topleft=None, topright=None, 
                 left=None,right=None,top=None, topy=None,bottom=None, bottomleft=None, bottomright=None,
                 width=None,height=None):
        rect = self.system.backend.pygame.Rect(0, 0, *self.size)

        if center is not None:
            rect.center = center
        elif centerx is not None:
            rect.centerx = centerx    
        elif width is not None:
            rect.width = width
        elif height is not None:
            rect.height = height
        elif centery is not None:
        
            rect.centery = centery   
        elif topleft is not None:
            rect.topleft = topleft
        elif topright is not None:
            rect.topright = topright
        elif top is not None:
            rect.top = top
        elif topy is not None:
            rect.topy = topy
        elif left is not None:
            rect.left = left
        elif right is not None:
            rect.right = right
        elif bottom is not None:
            rect.bottom = bottom
        elif bottomleft is not None:
            rect.bottomleft = bottomleft
        elif bottomright is not None:
            rect.bottomright = bottomright

        return rect

    def fill(self, color, rect=None, alpha=None):
        if isinstance(rect, int) or isinstance(rect, float):
            alpha = rect
            rect = None

        self.system.backend.draw.surface_fill(self, color, rect, alpha)

    def set_alpha(self, alpha):
        self.alpha = alpha

    def blit(self, surface, rect):
        if not hasattr(rect, "x"):
            rect = surface.get_rect(topleft=rect)

        opengl = self.system.backend.draw.opengl

        previous = opengl.glGetIntegerv(opengl.GL_FRAMEBUFFER_BINDING)

        opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, self.framebuffer)

        self.system.backend.draw.blit(surface, rect)

        opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, previous)

    @classmethod
    def from_pygame(cls, system, pygame_surface):
        surface = cls(
            system,
            pygame_surface.get_size(),
            pygame_surface.get_alpha() is not None
        )

        surface.pygame_surface = pygame_surface.copy()

        system.backend.draw.upload_surface(surface, pygame_surface)

        surface.mask = system.backend.draw.create_mask(surface)

        return surface