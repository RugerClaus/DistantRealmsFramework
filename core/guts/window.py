import pygame
from systemlogging import log_error
from helper import get_colors,asset
from config import config

class Window:
    def __init__(self,system):
        pygame.init()
        self.system = system
        self.default_width = 1600
        self.default_height = 900
        self.color = (255,0,0)
        self.width = None
        self.height = None
        self.fps = 60
        self.fullscreen = False
        self.set_mode(self.width,self.height)
        self.Rect = pygame.Rect
        
        

    def mask(self,surface):
        return pygame.mask.from_surface(surface)

    def set_mode(self,width=None,height=None,mode=None):
        self.screen = pygame.display.set_mode((width if width is not None else self.default_width,height if height is not None else self.default_height),pygame.RESIZABLE)
        
        pygame.display.set_caption(f"{config['TITLE']} {config['VERSION']}")
        icon = self.load_image(asset("linux_icon"))
        pygame.display.set_icon(icon)
        
    def transform_scale(self, original_surface, new_surface_width, new_surface_height):
        return pygame.transform.scale(original_surface, (new_surface_width, new_surface_height))

    def transform_smoothscale(self,original,newW,newH):
        return pygame.transform.smoothscale(original,(newW,newH))
    
    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.fullscreen = True
            self.set_mode()
        else:
            self.fullscreen = False
            self.set_mode()

    def get_width(self):
        return self.screen.get_width()
    
    def get_height(self):
        return self.screen.get_height()

    def get_size(self):
        return self.screen.get_size()

    def default_fill(self):
        self.screen.fill(self.color)

    def fill(self, color,alpha=None):
        if isinstance(color, str):
            color = get_colors(color.lower())
        elif isinstance(color, tuple) and len(color) == 3:
            color = color
            alpha = alpha if alpha is not None else 255
            color = (*color, alpha)
        elif isinstance(color, tuple) and len(color) == 4:
            color = color
        else:
            raise ValueError("fill() only supports RGB or RGBA tuples or color strings")
        self.screen.fill(color)

    def draw_overlay(self, color, alpha):
        overlay = self.make_surface(self.get_width(), self.get_height(), alpha=True)
        overlay.fill((*color, alpha))
        return overlay
    
    def draw_line(self,surface,point_a,point_b,color,width=None):
        if isinstance(color,tuple):
            pygame.draw.line(surface,color,point_a,point_b)
            if width is not None:
                pygame.draw.line(surface,color,point_a,point_b,width)
        else:
            log_error("color must be a tuple")

    def draw_polygon(self,surface,color,points):
        pygame.draw.polygon(surface,color,points)

    def draw_circle(self,surface,color,center,radius,object=None):
        if not isinstance(surface,pygame.Surface):
            log_error(f"surface must be a Surface",object)
        elif not isinstance(color,tuple) or len(color) != 3:
            log_error(f"color must be a tuple: (r,g,b); found: value: {str(color)} type: {str(type(color))}",object)
        elif not isinstance(center,tuple) or len(center) != 2:
            log_error(f"center must be a tuple: (x,y); found: value: {str(center)} type: {str(type(center))}",object)
        elif not isinstance(radius,float):
            log_error(f"radius must be a floating point number (decimal); found: value: {str(radius)} type: {str(type(radius))}",object)
        else:
            pygame.draw.circle(surface,color,center,radius)

    def draw_rect(self, surface, color, rect, width=0, border_radius=None, object=None):
        if not isinstance(surface, pygame.Surface):
            log_error(f"surface must be a Surface", object)
            return
        elif not isinstance(color,tuple):
            log_error("color must be a tuple",object)

        elif not isinstance(rect,pygame.Rect):
            log_error("rect must be a pygame.Rect") # this will change once I create my own solution for rects
            
        if border_radius:
            pygame.draw.rect(surface, color, rect, width, border_radius)
        else:
            pygame.draw.rect(surface, color, rect, width)

    def make_rect(self, data):
        x, y, w, h = data
        return pygame.Rect(x, y, w, h)
            
    def load_image(self,file_like):
        img = pygame.image.load(file_like)
        img = img.convert_alpha()
        img = img.copy()
        return img

    def blit(self,surface,destination,area=None):
        if area is not None:
            x, y, w, h = area
            area = pygame.Rect(x, y, w, h)

        self.screen.blit(surface, destination, area)

    def get_screen(self):
        return self.screen
    
    def make_surface(self, width, height, alpha=False):

        flags = pygame.SRCALPHA if alpha else 0
        return pygame.Surface((width, height), flags)

    def update(self):
        pygame.display.flip()

    def get_fps(self): #temporary while i refactor to prevent breakage
        return self.system.time.get_fps()
    
    def get_info(self):
        return f"""{pygame.display.Info()}\n,PYGAMEDRIVER: \n{pygame.display.get_driver()}
                ,\n PYGAMENUMDISPLAYS: {pygame.display.get_num_displays()}
        """
    
    def quit(self):
        return pygame.quit()