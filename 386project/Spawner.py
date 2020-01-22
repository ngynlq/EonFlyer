import Bullet
from BulletInfo import BulletInfo
from pattern import translatePos,trackPath
import pygame
#this class is factory that creates more bullets
import Bullet
TOPBOUND = 0
LEFTBOUND = 30
RIGHTBOUND = 740
BOTTOMBOUND = 710
class Spawner:
    def __init__(self,sprite,HP,pos,paths,travelCD,BulletInfo,difficulty,score,power,kill):
        super().__init__()
        self.image = sprite#hit collision stuff
        if self.image is not None:    
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.radius = self.rect.w /2
        else:
            self.rect = pygame.Rect((0,0),(0,0))
            self.rect.center = pos
            self.radius = 0

        self._HP = HP
        self._bulletGen = []#bullet creator
        self.createGen(BulletInfo)
        
        self._bulletsOn = []
        self._kill = kill
        self._diff = difficulty
        self._visible = self.isVisible(self.rect)
        self._complete = False
        self._score = score #int list
        self._power = power

        self._paths = paths#self movement
        self._travelCDGen = travelCD()
        self._moveCD = next(self._travelCDGen)
        self._last = 0
        self._endPoint = next(self._paths)
        self._xInc = self._endPoint[0]/60
        self._yInc = self._endPoint[1]/60
        self._tick = 0
        self._oldPoint = self.rect.center
    def setLast(self,last):
        self._last = last
    def offsetTime(self,elapsed):
        self._last += elapsed
    def setComplete(self,i):
        self._complete = i
    def getHP(self):
        return self._HP
    def getPower(self):
        temp = []
        for pos,value in self._power:
            temp.append((translatePos(self.rect.center,pos),value))
        return temp
    def getScore(self):
        temp = []
        for pos,value in self._score:
            temp.append((translatePos(self.rect.center,pos),value))
        return temp
    def getPos(self):
        return self.rect.center
    def createGen(self,Infos):
        for BulletInfos in Infos:
            temp = {}
            temp['img'] = BulletInfos.bulletImg
            temp['rotate'] = BulletInfos.rotate#yields arcangle generators. can sent an unbuilt or built gen
            temp['posProduce'] = BulletInfos.produce()
            temp['createTime'] = BulletInfos.createTime#add
            temp['createCD'] = next(temp['createTime'])
            temp['path'] = BulletInfos.paths #one path for all,let the bullet construct its path and wait time.
            temp['waitTime'] = BulletInfos.wait
            temp['trackTime'] = BulletInfos.trackTime
            temp['trackPath'] = BulletInfos.trackPath
            temp['trackSpeed'] = BulletInfos.trackSpeed
            temp['selfdestruct'] = BulletInfos.kill
            temp['continualTrack'] = BulletInfos.trackPattern
            temp['addTrackArgs'] = BulletInfos.trackArgs
            temp['built'] = False
            self._bulletGen.append(temp)
        time = pygame.time.get_ticks()
        for i in self._bulletGen:
            i['time'] = time
    def getRect(self):
        return self.rect
    def produceBullets(self,player):
        temp = [] # new group of bulelts
        if self.fullyVisible():
            now = pygame.time.get_ticks()
            for info in self._bulletGen:
                if info['createCD'] is not None:
                    if now - info['time'] > info['createCD']:
                        setOfBullets = []
                        if info['continualTrack'] is not None:
                            if info['continualTrack']:
                                info['rotate'] = info['trackPath'](self.rect.center,player,info['addTrackArgs'])
                            elif not info['continualTrack'] and not info['built']:
                                info['rotate'] = info['trackPath'](self.rect.center,player,info['addTrackArgs'])
                                info['built'] = True
                        bulletAngles = next(info['rotate'])
                        bulletPos = next(info['posProduce'])
                        if len(bulletAngles) == len(bulletPos):#absolute control over points
                            for angle,pos in zip(bulletangles,bulletPos):
                                newPos = translatePos(self.rect.center,pos)
                                setOfBullets.append(Bullet.Bullet(info['img'],newPos,angle,info['path'],info['waitTime'],info['trackTime'],info['trackPath'],info['trackSpeed'],player))
                        elif len(bulletAngles) > len(bulletPos):
                            for pos in bulletPos:
                                newPos = translatePos(self.rect.center,pos)
                                Angles = next(info['rotate'])
                                for angle in Angles:
                                    setOfBullets.append(Bullet.Bullet(info['img'],newPos,angle,info['path'],info['waitTime'],info['trackTime'],info['trackPath'],info['trackSpeed'],player))
                        else:                       
                            for angle in bulletAngles:
                                bulletPos = next(info['posProduce'])
                                for pos in bulletPos:
                                    newPos = translatePos(self.rect.center,pos)
                                    setOfBullets.append(Bullet.Bullet(info['img'],newPos,angle,info['path'],info['waitTime'],info['trackTime'],info['trackPath'],info['trackSpeed'],player))
                        if info['selfdestruct']:
                            self._bulletsOn += setOfBullets
                        info['time'] = now
                        info['createCD'] = next(info['createTime'])
                        temp +=setOfBullets
                
        return temp
    def getImage(self):
        return self.image
    def damage(self,damage):
        if self._HP != None:
            if self.isVisible(self.rect):
                self._HP -= damage
                if self._HP <= 0:
                    self._complete = True
    def update(self):
            x = int(self._xInc * self._tick)
            y = int(self._yInc * self._tick)
            self._tick +=1
            temp = self.isVisible(self.rect)
            self.rect.center = translatePos(self._oldPoint,(x,y))
            if temp and not self.isVisible(self.rect):
                self._complete = True
            if self._tick == 60:
                now = pygame.time.get_ticks()
                if now - self._last > self._moveCD:
                    self._moveCD = next(self._travelCDGen)
                    self._last = pygame.time.get_ticks()
                    self._endPoint = next(self._paths)
                self._oldPoint = self.rect.center
                self._xInc = self._endPoint[0]/60
                self._yInc = self._endPoint[1]/60
                self._tick = 0
    def alive(self):
        if self._HP > 0:
            return True
        else:
            return False
    def fullyVisible(self):
        if TOPBOUND > self.rect.midtop[1]:
            return False
        elif BOTTOMBOUND < self.rect.midbottom[1]:
            return False
        elif LEFTBOUND > self.rect.midleft[0]:
            return False
        elif RIGHTBOUND < self.rect.midright[0]:
            return False
        else:
            return True        
    def isVisible(self,projectile):
        if TOPBOUND > projectile.midbottom[1]:
            return False
        elif BOTTOMBOUND < projectile.midtop[1]:
            return False
        elif LEFTBOUND > projectile.midright[0]:
            return False
        elif RIGHTBOUND < projectile.midleft[0]:
            return False
        else:
            return True
    def getComplete(self):
        return self._complete
