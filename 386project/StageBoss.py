#the stage boss class is mainly composed of a spawner and a track
#the tracker just keeps knowledge of the number of phases
from pattern import translatePos
import pygame
class StageBoss:
    def __init__(self,img,pos,phases):
        super().__init__()
        self._PhaseInfo = phases
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self._ori = pos
        self.radius = self.rect.w
        self._phases = len(self._PhaseInfo)
        self._currentPhase = 0
        self._PhaseHP = self._PhaseInfo[self._currentPhase].hp
        self._currentHP = self._PhaseInfo[self._currentPhase].hp
        self._last = pygame.time.get_ticks()
        self._travelGen = self._PhaseInfo[self._currentPhase].movementcd
        self._CD = next(self._travelGen)
        self._path = self._PhaseInfo[self._currentPhase].movement
        self._endPoint = next(self._path)
        self._OldPoint = pos
        self._xInc = self._endPoint[0]/60
        self._yInc = self._endPoint[1]/60
        self._tick = 0
        self._immune = False
    def bombDamage(self,damage):
        if not self._immune:
            self.damage(damage)
    def RemainingPhases(self):
        return self._phases - self._currentPhase -1
    def getHPPercent(self):
        return self._currentHP/self._PhaseHP
    def produceSpawners(self):
        return self._PhaseInfo[self._currentPhase].spawners
    def getPos(self):
        return self.rect.center
    def update(self):
        x = int(self._xInc * self._tick)
        y = int(self._yInc * self._tick)
        self._tick +=1
        self.rect.center = translatePos(self._OldPoint,(x,y))
        if self._tick == 60:
            now = pygame.time.get_ticks()
            if now - self._last > self._CD:
                self._CD = next(self._PhaseInfo[self._currentPhase].movementcd)
                self._last = pygame.time.get_ticks()
                self._endPoint = next(self._path)                
            self._OldPoint = self.rect.center
            self._xInc = self._endPoint[0]/60
            self._yInc = self._endPoint[1]/60
            self._tick = 0
    def nextPhase(self):
        if self._currentHP == 0 and self._currentPhase < self._phases:
            self._currentPhase +=1
            self._currentHP = self._PhaseInfo[self._currentPhase].hp
            self._last = pygame.time.get_ticks()
            self._travelGen = self._PhaseInfo[self._currentPhase].movementcd
            self._CD = next(self._travelGen)
            self._path = self._PhaseInfo[self._currentPhase].movement
            self._endPoint = next(self._path)
            self._OldPoint = self._ori
            self._xInc = self._endPoint[0]/60
            self._yInc = self._endPoint[1]/60
            self._PhaseHP = self._PhaseInfo[self._currentPhase].hp
            self._tick = 0
            return True
        else:
            return False
    def alive(self):
        if self._currentPhase+1 == self._phases and self._currentHP == 0:
            return False
        else:
            return True
    def damage(self,damage):
        self._currentHP -= damage
        if self._currentHP <= 0:
            self._currentHP = 0
    def getHP(self):
        return self._currentHP
    def getImage(self):
        return self.image
    def getRect(self):
        return self.rect
    def getBlitPos(self):
        return self.rect.topleft
