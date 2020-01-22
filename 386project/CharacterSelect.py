WHITE = (255,255,255)
BROWN = (255, 228, 196)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,224)
import pygame
from pygame.locals import *
from Game2 import Game
import Menu
class CharacterSelect:
    def __init__(self):
        self._place = 0
        self._mission = pygame.image.load("mission.png").convert()
        self._condition = pygame.image.load("condition.png").convert()
        self._lastnote = pygame.image.load("lastnote.png").convert()
        self._control = pygame.image.load("control.png").convert()
        pygame.mixer.music.load("mars.ogg")
        pygame.mixer.music.play(-1)
        self._items = [self._mission,self._condition,self._lastnote,self._control]
        
        self._clock = pygame.time.Clock()
        self._last = pygame.time.get_ticks()
        self._game = False
        self._menu = False
    def control(self,keys):
        now = pygame.time.get_ticks()
        if now - self._last > 200:
            self._last = now
        if keys[K_z]:
            if self._place >= len(self._items)-1:
                self._game = True
            else:
                self._place+=1
        elif keys[K_x]:
            if self._place == 0:
                self._menu = True
            else:
                self._place -=1
    def update(self,screen):
        self._clock.tick(5)
        screen.blit(self._items[self._place],(0,0))
    def newControl(self,keys):
        if self._game or self._menu:
            return True
        else:
            return False
    def nextControl(self):
        if self._game:
            return Game()
        elif self._menu:
            return Menu.Menu()
