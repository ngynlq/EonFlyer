import pygame
from pattern import translatePos
TOPBOUND = 0
LEFTBOUND = 30
RIGHTBOUND = 740
BOTTOMBOUND = 727
class Bullet:
    def __init__(self,sur,pos,angle,paths,wait,trackTime = None,trackDecide=None,trackSpeed = None,player=None,power = 0):
        self.image = sur
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = self.rect.w/2
        self._angle = angle #angle is only needed to build the generator
        self._path = paths(angle)
        self._wait = wait() #update cooldown.
        self._power = power #only for player.
        self._last = pygame.time.get_ticks()
        self._CD = next(self._wait)
        self._endPoint = next(self._path)
        self._OldPoint = pos
        self._xInc = self._endPoint[0]/60
        self._yInc = self._endPoint[1]/60
        self._tick = 0
        self._trackTime = trackTime
        self._trackPath = trackDecide
        self._trackSpeed = trackSpeed
        self._start = self._last
        self._builtTrack = False
        if self._trackTime != None:
            if self._start > self._trackTime:
                self._path = self._trackPath(self.rect.center,player)
                self._wait = self._trackSpeed()
                self._builtTrack = True            
    def getPos(self):
        return self.rect.center
    def offsetTime(self,elapsed):
        self._last += elapsed
    def update(self,pos=None):
        x = int(self._xInc * self._tick)
        y = int(self._yInc * self._tick)
        self._tick +=1
        self.rect.center = translatePos(self._OldPoint,(x,y))
        if self._tick == 60:
            now = pygame.time.get_ticks()
            if self._trackTime != None:
                if now - self._start > self._trackTime and not self._builtTrack:
                    self._path = self._trackPath(self.rect.center,pos)
                    self._wait = self._trackSpeed()
                    self._builtTrack = True

            if now - self._last > self._CD:
                self._CD = next(self._wait)
                self._last = pygame.time.get_ticks()
                self._endPoint = next(self._path)                
            self._OldPoint = self.rect.center
            self._xInc = self._endPoint[0]/60
            self._yInc = self._endPoint[1]/60
            self._tick = 0
    def getRect(self):
        return self.rect
    def getDamage(self):
        return self._power
    def getImage(self):
        return self.image
