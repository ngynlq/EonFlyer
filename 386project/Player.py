import pygame
from pygame.locals import *
import pygame
from pattern import translatePos
from Bullet import Bullet
TOPBOUND = 0
LEFTBOUND = 30
RIGHTBOUND = 740
BOTTOMBOUND = 690
LOWSPEED = 3
HIGHSPEED = 7
class Player:
    def __init__(self,charImg,BulletInfo):
        super().__init__()
        self.image = charImg
        self.rect = charImg.get_rect()
        self.rect.center = (500,500)
        self.radius = 2
        self._alive = True
        self._fireTick = 0 #spacing.
        self._power = 0 #character power
        self._bullet = BulletInfo
        self._life = 3
        self._bomb = 2
        self._immune = False
        self._respawn = False
        self._speed = 3
        self._waitProduce = []
        self._last = pygame.time.get_ticks()
        self._cooldown = []
        self._bombing = False
        self._respawnTime = 0
        for i in self._bullet:
            self._waitProduce.append(i.createTime(self._power))
        for i in self._waitProduce:
            self._cooldown.append(next(i))
    def damageValue(self):
        if self._power < 50:
            return 5
        elif self._power < 100:
            return 6
        elif self._power <150:
            return 7
        elif self._power <175:
            return 8
        elif self._power == 200:
            return 10
    def doneBombing(self):
        self._bombing = False
        self._immune = False
    def getImmune(self):
        return self._immune
    def isBombing(self):
        return self._bombing
    def canBomb(self):
        if not self._bombing and self._bomb >0 and not self._respawn:
            self._bombing = True
            self._immune = True
            return True
        else:
            return False
    def useBomb(self):
        self._bomb -=1        
    def getBomb(self):
        return self._bomb
    def getLife(self):
        return self._life
    def getAlive(self):
        return self._alive
    def getRespawn(self):
        return self._respawn
    def addPower(self,power):
        self._power += power
        if self._power  > 200:
            self._power = 200
    def fireBullets(self,keys):
        bullets = [] # new group of bulelts
        now = pygame.time.get_ticks()
        for info in self._bullet:
            index = self._bullet.index(info)
            if now - self._last >= self._cooldown[index]:
                self._last = pygame.time.get_ticks()
                self._cooldown[index] = next(self._waitProduce[index])
                
                bulletAngles = next(info.rotate(keys,self._power))
                bulletPos = next(info.produce(keys,self._power))
                if len(bulletAngles) == len(bulletPos):#absolute control over points
                    for angle,pos in zip(bulletAngles,bulletPos):
                        newPos = translatePos(self.rect.center,pos)
                        bullets.append(Bullet(info.bulletImg,newPos,angle,info.paths,info.wait,None,None,None,None,self.damageValue()))
                elif len(bulletAngles) > len(bulletPos):
                    for pos in bulletPos:
                        newPos = translatePos(self.rect.center,pos)
                        angles = next(info.rotate(keys,self._power))
                        for ang in angles:
                            bullets.append(Bullet(info.bulletImg,newPos,ang,info.paths,info.wait,None,None,None,None,self.damageValue()))
                else:                       
                    for angle in bulletAngles:
                        bulletPos = next(info.produce(keys,self._power))
                        for pos in bulletPos:
                            newPos = translatePos(self.rect.center,pos)
                            bullets.append(Bullet(info.bulletImg,newPos,angle,info.paths,info.wait,None,None,None,None,self.damageValue()))
        return bullets
    def canFire(self): # controls spacing of bullet intervals.
        if not self._respawn:
            return True
        else:
            return False
    def getImmune(self):
        return self._immune
    def playerDeath(self):
        self._life -=1
        self._bomb = 2
        self.rect.center = (300,660)
        self._respawn = True
        self._respawnTime = pygame.time.get_ticks()
        if self._life < 0:
            self._alive = False
    def doneRespawn(self):
        if self._respawn:
            now = pygame.time.get_ticks()
            if now - self._respawnTime > 2000:
                self._respawn = False
    def updateMovement(self,keys):
        if keys[K_LSHIFT]:
            self._speed = LOWSPEED
        elif not keys[K_LSHIFT]:
            self._speed = HIGHSPEED
        if keys[K_UP]:
            if TOPBOUND > self.rect.midtop[1]-self._speed:
                pass
            else:
                self.rect.centery -=self._speed
        if keys[K_LEFT]:
            if LEFTBOUND > self.rect.midleft[0]-self._speed:
                pass
            else:
                self.rect.centerx -= self._speed
        if keys[K_RIGHT]:
            if RIGHTBOUND < self.rect.midright[0] + self._speed:
                pass
            else:
                self.rect.centerx += self._speed
        if keys[K_DOWN]:
            if BOTTOMBOUND < self.rect.midbottom[1] + self._speed:
                pass
            else:
                self.rect.centery += self._speed
            
    def getImg(self):
        return self.image
    def getRect(self):
        return self.rect
    def getPos(self):
        return self.rect.center
    def slow(self):
        if self._speed == LOWSPEED:
            return True
        else:
            return False
    def getPower(self):
        return self._power

        
