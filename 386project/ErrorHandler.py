WHITE = (255,255,255)
WHITE = (255,255,255)
BROWN = (255, 228, 196)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,224)
import pygame
class ErrorHandler:
    def __init__(self,text):
        self._errortxt = text+" Press any key to exit"
    def update(self,screen):
        basicFont = pygame.font.SysFont(None, 48)  
        screen.fill(WHITE)
        error = basicFont.render(self._errortxt,True,BLACK)
        errorRect = error.get_rect()
        errorRect.centerx = screen.get_rect().centerx
        errorRect.centery = screen.get_rect().centery
        screen.blit(error,errorRect)
    def control(self,keys):
        pass
    def newControl(self,keys):
        if keys:
            return True
        else:
            return False
    def nextControl(self):
        return False
