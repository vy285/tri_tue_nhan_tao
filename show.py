import pygame
from math import sqrt
pygame.init()


""" 
    rectbutton : dung de ve cac o tuy chon hanh dong
    co method color_change khi duoc chi vao
"""
class RectButton:
    def __init__(self,left:int,top:int,width:int,height:int,
                     text:str,textcolor:tuple,rectcolor:tuple,
                     screen:pygame,font:pygame) :
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.screen = screen
        self.font = font
        # setup hinh tron voi cac thong tin chieu cao , rong ,vi tri
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.textcolor = textcolor
        self.rectcolor = rectcolor

# khoi tao ve cac rect
    def __call__(self):
        button_text = self.font.render(self.text,True,self.textcolor)
        button_rect = button_text.get_rect()
        button_rect.center = self.rect.center
        pygame.draw.rect(self.screen,self.rectcolor,self.rect)
        self.screen.blit(button_text,button_rect)
    
    #thay doi mau khi duoc chon
    def color_change(self ,  color : tuple):
        self.rectcolor = color

"""
    cirbutton : de chon thuat toan thuc hien
"""
class CirButton:
    def __init__(self, center:tuple, radius:int, text:str, 
                       textcolor:tuple, circolor:tuple,
                       screen:pygame, font:pygame):
        self._radius = radius
        self._center = center
        self._text = text
        self._screen = screen
        self._font = font
        self.textcolor = textcolor
        self.circolor = circolor

    def __call__(self):
        button_text = self._font.render(self._text, True, self.textcolor)
        button_rect = button_text.get_rect()
        
        button_rect.center = self._center
        pygame.draw.circle(self._screen, self.circolor, self._center, self._radius)
        self._screen.blit(button_text, button_rect)

    def color_change(self, color:tuple):
        self.circolor = color


    def distance(self, mouse_pos:tuple)->float:
    
        return sqrt((self._center[0]-mouse_pos[0])**2+(self._center[1]-mouse_pos[1])**2)

