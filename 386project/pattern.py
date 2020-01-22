import math
import random
from pygame.locals import *
#this is the waitime calc, return 0 to produce a bullet.

#path Generator
def translatePos(ori,pos):
    x = ori[0] + pos[0]
    y= ori[1] - pos[1]
    return x,y
def straightPath(angle): #for the bullet/constant speed.
    tick = 300
    deg = math.radians(angle)
    while True:
        x = math.cos(deg) * tick
        y = tick * math.sin(deg)
        yield x,y
        tick = 100
def SlowStraight(angle):
    tick = 200
    deg = math.radians(angle)
    while True:
        x = math.cos(deg) * tick
        y = tick * math.sin(deg)
        yield x,y
        tick = 50
def SpawnerMoveTwoDirections(first,second):
    yield first
    while True:
        yield second
def fixedFire(difficulty,limit):
    count = 0
    total = limit * difficulty
    while True:
        if count > total:
            yield None
        else:
            yield 250
            count +=1
def SpawnerMulti(pos):
    while True:
        for i in pos:
            yield i
def slowSecondSwap():
    yield 500
    while True:
        yield 12000
def slowfixedFire(difficulty,limit,first):
    count = 0
    total = limit * difficulty
    yield first
    while True:
        if count > total:
            yield None
        else:
            yield 500
            count +=1
    
def ConstantStraightPath(angle): #for the bullet/constant speed.
    tick = 500
    deg = math.radians(angle)
    while True:
        x = math.cos(deg) * tick
        y = tick * math.sin(deg)
        yield x,y
def BulletWait():#When to swap to a next speed
    while True:
        yield 4000
def instantTrack():
    while True:
        yield 0
def SpawnerMovement(x,y):
    tick = 0
    while True:
        yield x,y
def NoWait():#spawner production
    tick = 0
    while True:
        yield 200
def ContinualFire(wait):
    while True:
        yield wait
def TwoSpeedSwap():
    while True:
        yield 800
def zeroWait():
    while True:
        yield 200
def trackSwap():#this function tells when to swap to
    while True:
        yield 8000
def trackPath(selfpos,tarpos,add=[]):
    y = selfpos[1] - tarpos[1]
    x = tarpos[0] - selfpos[0]
    angle = math.atan2(y,x)
    deg = math.degrees(angle)
    return straightPath(deg)
def trackWait():
    while True:
        yield 100
def PointDrop():
    while True:
        yield 5
#always assume there is enough room for a  single placement
def SpacedAngles(difficulty,baseBullets,start,end,rotate,spacing,gap):
    clump = (baseBullets * difficulty)
    circum = abs(start-end)
    remaining = circum
    newStart = start
    times = circum / ((clump * spacing) + gap)
    if times == 0:
        times = 1
    while True:
        item = []
        while times > 0:
            for i in range(clump):
                item.append(newStart+(i * spacing))
            newStart += ((spacing * clump) + gap)
            times -= 1
        yield item
        times = circum / ((clump * spacing) + gap)
        newStart+= rotate
    #number of elements in add must be the same as ArcAngle
def trackArcAngle(selfpos,tarpos,add):
    difficulty = add[0]
    base = add[1]
    start = add[2]
    end = add[3]
    rotate = add[4]
    spin = add[5]
    
    dist = abs(end - start) / 2
    y = selfpos[1] - tarpos[1]
    x = tarpos[0] - selfpos[0]
    angle = math.atan2(y,x)

    deg = math.degrees(angle)
    start = deg - dist
    end = deg + dist
    return ArcAngle(difficulty,base,start,end,rotate,spin)
#when using skip make sure the start -end is less than  360/spacing
def delayContinual(delay,continual):
    yield delay
    while True:
        yield continual
def ArcAngle(difficulty,baseBullets,start,end,rotate,spin):
    totalBullets = (baseBullets * difficulty)
    circum = abs(start - end)
    newStart = start
    count = 0
    tick = rotate
    angle = circum / totalBullets
    while True:
        item = []
        for i in range(totalBullets):
            item.append(newStart + (i* angle))
        yield item
        count +=1
        if spin != None:
            if count == spin:
                tick *= -1
                count = rotate
        newStart += tick
def PlayerPrimShoot(keys,power):
    while True:
        if keys[LSHIFT]:
            return [(-2,1),(1,2)]
        else:
            return [(-1,1),(1,1)]
def PlayerPrimAngle(keys,power):
    while True:
        if keys[K_LSHIFT]:
            if power < 50:
                yield [90]
            elif 50<= power <150:
                yield [90,90]
            elif power >= 150:
                yield [90,90,90]
        else:
            if power < 50:
                yield [90]
            elif 50<= power <150:
                yield [60,120]
            elif power >= 150:
                yield [90,120,60]            
def PlayerWait(power):
    while True:   
        yield 100

def PlayerPos(keys,power):
    while True:
        if keys[K_LSHIFT]:
            if power <50:
                yield [(0,1)]
            elif 50<= power <150:
                yield [(30,1),(-30,1)]
            elif power >= 150:
                yield [(30,1),(-30,1),(0,1)]
        else:
            yield [(0,1)]
def SpawnerPos():
    while True:
        yield [(0,0)]

    

    
    



    
