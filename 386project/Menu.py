import pygame
from pygame.locals import *

WHITE = (255,255,255)
BROWN = (255, 228, 196)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,224)
class Menu:
    def __init__(self):
        self._Focus = 0
        self._clock = pygame.time.Clock()
        pygame.mixer.music.load('Mercury.ogg')
        pygame.mixer.music.play(-1)
        self._background = pygame.image.load("Menu.png")
        self._background.convert()
        self._last = pygame.time.get_ticks()
    def control(self,keys):
        now = pygame.time.get_ticks()
        if now - self._last > 300:
            self._last = now
            if keys[K_UP]:
                if self._Focus == 0:
                    self._Focus = 1
                else:
                    self._Focus -= 1
            elif keys[K_DOWN]:
                if self._Focus == 1:
                    self._Focus = 0
                else:
                    self._Focus += 1
    def update(self,screen):
        self._clock.tick(10)
        basicFont = pygame.font.SysFont(None, 48)
        centerx = screen.get_rect().centerx
        centery = screen.get_rect().centery
        
        screen.blit(self._background,(0,0))
        play = basicFont.render("Play",True,BLACK)
        quitGame = basicFont.render("Quit Game",True,BLACK)
                
        playRect = play.get_rect()
        playRect.center = (750,439)
        
        quitGameRect = quitGame.get_rect()
        quitGameRect.center = (750,639)
        choices = [playRect,quitGameRect]
        
        pygame.draw.rect(screen,BLUE,choices[self._Focus])
        screen.blit(play,playRect)
        screen.blit(quitGame,quitGameRect)
    def newControl(self,keys):
        if keys[K_z]:
            return True
        else:
            return False
    def nextControl(self):
        import CharacterSelect        
        if self._Focus == 0:
            pygame.mixer.music.stop()
            return CharacterSelect.CharacterSelect()
        elif self._Focus == 1:
            return False
            

    
