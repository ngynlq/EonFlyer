from pattern import *
import pygame
class BonusBox:
    def __init__(self,sur,pos,value):
        self.image = sur
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self._value = value
        self._path = straightPath(270)
        self._wait = PointDrop()
        self._CD = next(self._wait)
        self._last = pygame.time.get_ticks()
        self._tick = 0
        self._endPoint = next(self._path)
        self._OldPoint = pos
        self._xInc = self._endPoint[0]/60
        self._yInc = self._endPoint[1]/60
    def update(self):
        x = int(self._xInc * self._tick)
        y = int(self._yInc * self._tick)
        self._tick +=1
        self.rect.center = translatePos(self._OldPoint,(x,y))
        if self._tick ==60:
            now = pygame.time.get_ticks()
            if now - self._last > self._CD:
                self._CD = next(self._wait)
                self._last = pygame.time.get_ticks()
                self._endPoint = next(self._path)
            self._OldPoint = self.rect.center
            self._xInc = self._endPoint[0]/60
            self._yInc = self._endPoint[1]/60
            self._tick = 0
    def getImage(self):
        return self.image
    def getRect(self):
        return self.rect
    def getValue(self):
        return self._value
            
        
