import pygame

from helper import get_colors,log_error,asset
from config import config
from core.guts.time import Time

class Window:
    def __init__(self):
        pygame.init()
        self.default_width = 1200
        self.default_height = 800
        self.color = (255,0,0)
        self.width = self.default_width
        self.height = self.default_height
        self.fps = 60
        self.time = Time()
        self.get_current_time = self.time.get_current_time
        self.fullscreen = False
        self.set_screen()
        self.Rect = pygame.Rect
        

    def mask(self,surface):
        return pygame.mask.from_surface(surface)

    def set_screen(self,width=None,height=None):
        if width is None and height is None:
            self.screen = pygame.display.set_mode((self.width,self.height),pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
        elif width is not None and height is None:
            self.screen = pygame.display.set_mode((width,self.height),pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
        elif width is None and height is not None:
            self.screen = pygame.display.set_mode((self.width,height),pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
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
            self.set_screen()
        else:
            self.fullscreen = False
            self.set_screen()

    def get_width(self):
        return self.screen.get_width()
    
    def get_height(self):
        return self.screen.get_height()
    
    def scale(self,target_width,target_height):
        self.screen = pygame.display.set_mode((target_width,target_height),pygame.RESIZABLE)

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
        return self.time.get_fps()
    
    def quit(self):
        return pygame.quit()