from Bullet import Bullet
from Spawner import Spawner
from Player import Player
from ErrorHandler import ErrorHandler
from pygame.locals import *
from BulletInfo import BulletInfo
from BonusBox import BonusBox
from pattern import *
from SpatialHash import SpatialHash
from StageBoss import StageBoss
from PhaseInfo import PhaseInfo
TOPBOUND = 0
LEFTBOUND = 30
RIGHTBOUND = 740
BOTTOMBOUND = 690
WHITE = (255,255,255)
BROWN = (255, 228, 196)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (56,56,56)
import pygame
class Game:
    def __init__(self):
        pygame.mixer.music.load('map.ogg')
        pygame.mixer.music.play(-1)
        self._playerFire = pygame.mixer.Sound("Rain.ogg")
        self._playerFire.set_volume(.1)
        self._playerDie = pygame.mixer.Sound("Explosion.ogg")
        self._bombingSound = pygame.mixer.Sound("Kiira.ogg")
        self._attackFire = pygame.mixer.Sound("Rain2.ogg")
        self._attackFire.set_volume(.1)
        self._bombingSound.set_volume(.01)
        self._deadSpawnerSound = pygame.mixer.Sound("DeathNew.ogg")
        self._deadSpawnerSound.set_volume(.2)
        self._hitBulletSound = pygame.mixer.Sound("Telecom.ogg")
        self._hitBulletSound.set_volume(.2)
        self._itemSound = pygame.mixer.Sound("Collect_Point_00.ogg")
        self._itemSound.set_volume(.5)
        self._error = False #error checker.
        self._clear = False #check if the Game cleared
        self._stageSpawners = {} #a dictionary of spawners for each stage {tick:spawners}
        self._activeSpawners = []
        self._activeBullets = []
        self._hitBullets = []
        self._deadSpawners = []
        self._scorePoint = []
        self._activePlayerBullets = []
        self._powerPoint = []
        self._clock = pygame.time.Clock()
        self._score = 0 # score tracking
        self._graze = 0
        #bunch of control variables.
        
        self._pause = False #player has paused the game.
        self._resume = True #default choice Yes/Return to Game
        self._confirm = False #player has hit enter.
        self._scoreScreen = False
        self._moveOn = True #tell the game to load a stage.
        self._boss = False
        self._bossTick = 60 #60
        self._bossSpawn = False
        self._time = 0
        self._currentBoss = []
        self._gameOver = False
        #load the images.
        self._waitTime = 0
        
        self._gameItems = SpatialHash(71,69,30,0)
        self._scoreScreenImg = pygame.image.load("end.png").convert()
        self._rightBound = pygame.image.load("rightBound.png").convert()
        self._leftBound = pygame.image.load("leftBound.png").convert()
        self._bottomBound = pygame.image.load("bottomBound.png").convert()
        self._background = pygame.image.load("background.png").convert()
        self._lifeimg = pygame.image.load("life.png").convert()
        self._lifeimg.set_colorkey(BLACK)
        self._playerimg = pygame.image.load("player.png").convert()
        self._playerimg.set_colorkey(BLACK)
        self._bombimg = pygame.image.load("bomb.png").convert()
        self._bombimg.set_colorkey(BLACK)
        self._playerBullet = pygame.image.load("playerbullet.png").convert()
        self._playerBullet.set_colorkey(BLACK)
        temp = BulletInfo(self._playerBullet,ConstantStraightPath,PlayerPrimAngle,PlayerWait,zeroWait,PlayerPos)
        self._player = Player(self._playerimg,[temp]) #temp
        self._powerImg = pygame.image.load("power.png").convert()
        self._scoreImg = pygame.image.load("score.png").convert()
        self._bossImg = pygame.image.load("Boss.png").convert()
        self._bossImg.set_colorkey(BLACK)
        self._bombTime = 0
        self._hitImg = pygame.image.load("explosion.png").convert()
        self._hitImg.set_colorkey(BLACK)
        self._spawnerdeathImg = pygame.image.load("explosion.png").convert()
        self._spawnerdeathImg.set_colorkey(BLACK)
        self._spawner = pygame.image.load("spawner.png").convert()
        self._spawner.set_colorkey(WHITE)
        self._bullet2 = pygame.image.load("bullet2.png").convert()
        self._bullet2.set_colorkey(BLACK)
        firstPhase = PhaseInfo(2000,[Spawner(None,None,(400,200),SpawnerMovement(0,0),zeroWait,
                                        [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,20,0,360,10,50),ContinualFire(300),BulletWait,SpawnerPos)]
                                            ,1,[((10,0),10)],[((-10,0),10)],False)],
                               SpawnerMovement(0,0),NoWait())
        thirdPhase = PhaseInfo(2000,[Spawner(None,None,(350,200),SpawnerMovement(0,0),zeroWait,
                                          [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,4,0,360,10,50),ContinualFire(500),BulletWait,SpawnerPos)]
                                          ,1,[((10,0),10)],[((-10,0),10)],False),
                                  Spawner(None,None,(400,200),SpawnerMovement(0,0),zeroWait,
                                          [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,10,0,360,20,50),ContinualFire(700),BulletWait,SpawnerPos)]
                                          ,1,[((10,0),10)],[((-10,0),10)],False),
                                  Spawner(None,None,(450,200),SpawnerMovement(0,0),zeroWait,
                                          [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,4,0,360,50,50),ContinualFire(600),BulletWait,SpawnerPos)]
                                          ,1,[((10,0),None)],[((-10,0),10)],False),
                                  Spawner(None,None,(400,150),SpawnerMovement(0,0),zeroWait,
                                          [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,20,0,360,50,50),ContinualFire(500),BulletWait,SpawnerPos)]
                                          ,1,[((10,0),None)],[((-10,0),10)],False),
                                  Spawner(None,None,(400,250),SpawnerMovement(0,0),zeroWait,
                                          [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,20,0,360,50,50),ContinualFire(800),BulletWait,SpawnerPos)]
                                          ,1,[((10,0),None)],[((-10,0),10)],False)],
                               SpawnerMovement(0,0),NoWait())
        secondPhase = PhaseInfo(2000,[Spawner(None,None,(400,200),SpawnerMovement(0,0),zeroWait,
                                       [BulletInfo(self._bullet2,SlowStraight,ArcAngle(1,30,0,360,20,None),ContinualFire(300),BulletWait,SpawnerPos)]
                                       ,1,[((10,0),10)],[((-10,0),10)],False)],
                                    SpawnerMovement(0,0),NoWait())
        self._currentBoss = StageBoss(self._bossImg,(400,200),[firstPhase,secondPhase,thirdPhase])

        
        self._stageSpawners[3] = [Spawner(self._spawner,20,(350,0),SpawnerMovement(0,-100),zeroWait,
                                           [BulletInfo(self._bullet2,straightPath,ArcAngle(1,20,0,360,0,None),fixedFire(1,3),BulletWait,SpawnerPos)]
                                               ,1,[((10,0),5)],[((-10,0),5)],False)]
        self._stageSpawners[5] = [Spawner(self._spawner,10,(200,30),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,3),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,20),5)],False),
                                Spawner(self._spawner,10,(500,30),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,3),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False)]
                                                                                         
        self._stageSpawners[6] =[Spawner(self._spawner,10,(200,20),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,4),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(500,20),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,4),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(200,18),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,4),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(500,18),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,4),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[7] =[Spawner(self._spawner,10,(200,10),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,5),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(500,10),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,5),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,20,(350,0),SpawnerMovement(0,-100),zeroWait,
                                           [BulletInfo(self._bullet2,straightPath,ArcAngle(1,20,0,360,0,None),fixedFire(1,5),BulletWait,SpawnerPos)]
                                               ,1,[((10,0),5)],[((-10,0),5)],False)]
        self._stageSpawners[8] =[Spawner(self._spawner,10,(200,5),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                            [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,5),BulletWait,SpawnerPos,
                                False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                  ,1,[((10,0),5)],[((-10,0),5)],False),
                        Spawner(self._spawner,10,(500,5),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                            [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,5),BulletWait,SpawnerPos,
                                False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                  ,1,[((10,0),5)],[((-10,0),5)],False)]
        self._stageSpawners[9] =[Spawner(self._spawner,10,(200,9),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                            [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,6),BulletWait,SpawnerPos,
                                False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                  ,1,[((10,0),5)],[((-10,0),5)],False),
                        Spawner(self._spawner,10,(500,9),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                            [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,6),BulletWait,SpawnerPos,
                                False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                  ,1,[((10,0),5)],[((-10,0),5)],False)]
        self._stageSpawners[10] = [Spawner(self._spawner,10,(350,0),SpawnerMovement(0,-100),zeroWait,
                                           [BulletInfo(self._bullet2,straightPath,ArcAngle(1,20,0,360,0,None),fixedFire(1,5),BulletWait,SpawnerPos)]
                                               ,1,[((10,0),5)],[((-10,0),5)],False)]
        self._stageSpawners[11] =[Spawner(self._spawner,10,(200,20),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(500,20),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(200,18),SpawnerMoveTwoDirections((0,-200),(-100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(500,18),SpawnerMoveTwoDirections((0,-200),(100,0)),TwoSpeedSwap,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        
        self._stageSpawners[17] =[Spawner(self._spawner,10,(0,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(-40,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-80,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-120,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(760,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),

                                Spawner(self._spawner,10,(800,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(840,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(880,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[21] =[Spawner(self._spawner,10,(0,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(-40,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-80,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-120,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(760,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),

                                Spawner(self._spawner,10,(800,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(840,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(880,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[24] =[Spawner(self._spawner,10,(0,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(-40,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-80,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-120,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(760,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),

                                Spawner(self._spawner,10,(800,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(840,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(880,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[30] =[Spawner(self._spawner,10,(0,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(-40,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-80,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(-120,100),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(760,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),

                                Spawner(self._spawner,10,(800,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(840,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(880,150),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[31] =[Spawner(self._spawner,10,(0,50),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 Spawner(self._spawner,10,(-40,50),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),10)],False),
                                Spawner(self._spawner,10,(-80,50),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),10)],False),
                                Spawner(self._spawner,10,(-120,50),SpawnerMovement(100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),10)],False),
                                Spawner(self._spawner,10,(760,200),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),10)],False),

                                Spawner(self._spawner,10,(800,200),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(840,200),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                Spawner(self._spawner,10,(880,200),SpawnerMovement(-100,0),zeroWait,
                                    [BulletInfo(self._bullet2,straightPath,ArcAngle(1,5,210,240,0,None),fixedFire(1,7),BulletWait,SpawnerPos,
                                        False,None,trackArcAngle,trackWait,[1,4,0,180,0,None])]
                                          ,1,[((10,0),5)],[((-10,0),5)],False),
                                 ]
        self._stageSpawners[40] = [Spawner(self._spawner,350,(350,0),SpawnerMulti([(0,-200),(0,0),(-100,0)]),slowSecondSwap,
                                   [BulletInfo(self._bullet2,SlowStraight,SpacedAngles(1,8,20,360,20,1,20),slowfixedFire(1,50,10000),BulletWait,SpawnerPos)]
                                       ,1,[((10,0),50)],[((-10,0),50)],False)]
        self.readScore()
        self._playerTick = 0
    def readScore(self):
        f = open("score.txt", "r")
        x = f.readline()
        temp = x.split()
        self._highScore= int(temp[0])
        self._oldHighScore = self._highScore
        f.close()      
    def control(self,keys):
        if self._pause: # pause controls
            if keys[K_UP] or keys[K_DOWN]:
                self._resume = not self._resume
            elif keys[K_z]:
                self._confirm = True
                if self._resume:
                    self._pause = False
                    elapsed = pygame.time.get_ticks() - self._pauseTime
                    for i in self._activeSpawners:
                        i.offsetTime(elapsed)
                    for i in self._activeBullets:
                        i.offsetTime(elapsed)
        elif self._scoreScreen: #might be more to this such as array stepping
            now = pygame.time.get_ticks()
            if now - self._wait > 400:
                if keys[K_z]:
                    self._resume = True
        elif self._gameOver:
            if keys[K_z]:
                self._resume = True
        elif not self._clear:
            self._player.updateMovement(keys)            
            if keys[K_ESCAPE]:
                self._pause = True
                self._confirm = False
                self._pauseTime = pygame.time.get_ticks()        
            if keys[K_z]:
                if self._player.canFire(): #player shoots
                    self._playerFire.play()
                    x = self._player.fireBullets(keys)
                    self._activePlayerBullets += x
                    for i in x:
                        self._gameItems.addRect(i)
            if keys[K_x]:
                if self._player.canBomb():
                    self._player.useBomb()
                    self._bombTime = pygame.time.get_ticks()
    def newControl(self,keys):
        if self._error:
            return True
        elif not self._resume and self._pause and self._confirm:
            return True
        elif self._scoreScreen and self._resume:
            return True
        elif self._gameOver and self._resume:
            return True
        else:
            return False
    def nextControl(self):
        import Menu
        if self._error: # some error within the read. should techinically make a text string to tell since it would make more sense
            return ErrorHandler("Error in Text Parsing")
        elif self._gameOver: #GAME OVER!
            return Menu.Menu()
        elif self._scoreScreen:
            return Menu.Menu()
        elif self._pause:
            return Menu.Menu()
    def readStages(self):
        try:
            with open('stages.txt','r') as f:
                read_data = f.read()
        except:
            self._error = True
    def update(self,screen):
        if self._error:#error? don't do anything.
            pass
        elif self._pause:
            self.drawPause(screen)
        else:
            if self._scoreScreen :#stuff for the winning game
                self.drawEndOfGame(screen)
            elif self._gameOver:
                self.drawGameOver(screen)
            else:
                self._timedelta = self._clock.tick(60)
                self._timedelta /= 1000
                self._time +=self._timedelta
                
                self.stageAction()
                self.drawObjects(screen)
                self.drawUI(screen) # just the entire UI

    def drawEndOfGame(self,screen):
        screen.blit(self._scoreScreenImg,(0,0))
        basicFont = pygame.font.SysFont("century", 40)
        playerlifetotal = 100000 * self._player.getLife()
        playerbombtotal = 50000 * self._player.getBomb()
        grazetotal = 10 * self._graze
        final = self._score + playerlifetotal+playerbombtotal + grazetotal
        playerlifetext = basicFont.render(str(playerlifetotal),True,BLACK)
        playerbombtext = basicFont.render(str(playerbombtotal),True,BLACK)
        grazetext = basicFont.render(str(grazetotal),True,BLACK)
        score = basicFont.render(str(self._score),True,BLACK)
        finaltext = basicFont.render(str(final),True,BLACK)
        
        playerrect = playerlifetext.get_rect()
        playerbomb = playerbombtext.get_rect()
        grazerect = grazetext.get_rect()
        scorerect = score.get_rect()
        finalrect = finaltext.get_rect()

        playerrect.midleft = (575,174)
        playerbomb.midleft = (575,245)
        grazerect.midleft = (575,318)
        scorerect.midleft = (575,375)
        finalrect.midleft = (575,484)

        screen.blit(playerlifetext,playerrect)
        screen.blit(playerbombtext,playerbomb)
        screen.blit(grazetext,grazerect)
        screen.blit(score,scorerect)
        screen.blit(finaltext,finalrect)


        if self._highScore > self._oldHighScore:
            newhighscore = basicFont.render("NEW HIGH SCORE!",True,BLACK)
            screen.blit(newhighscore,(139,586))
    def drawUI(self,screen): #basic drawing for the next stage
        basicFont = pygame.font.SysFont("century", 40)

        powerpt = basicFont.render(str(self._player.getPower()),True,BLACK)

        screen.blit(powerpt,(800,319))

        screen.blit(self._rightBound,(740,0))
        screen.blit(self._leftBound,(0,0))
        screen.blit(self._bottomBound,(30,690))
        num = self._clock.get_fps()
        temp = int(num)
        fps = basicFont.render("FPS:"+str(temp),True,BLACK)
        screen.blit(fps,(755,708))
        
        highscorevalue = basicFont.render(str(self._highScore),True,BLACK)
        if self._highScore == 0:
            placesneeded = 6
        else:
            zeroes = int(math.log(self._highScore,10))
            placesneeded = 6 - zeroes
        if placesneeded > 0:
            highscorevalue = ("0"*placesneeded)+str(self._highScore)
        highscore = basicFont.render(highscorevalue,True,BLACK)
        screen.blit(highscore,(810,86))
            
        if self._score == 0:
            placesneeded = 6
        else:
            zeroes = int(math.log(self._score,10))
            placesneeded = 6 - zeroes
            
        if placesneeded > 0:
            highscorevalue = ("0"*placesneeded)+str(self._score)
        highscore = basicFont.render(highscorevalue,True,BLACK)
        screen.blit(highscore,(810,196))
        graze = basicFont.render(str(self._graze),True,BLACK)
        grazerect = graze.get_rect()
        grazerect.center = (895,680)
        screen.blit(graze,grazerect)
        for i in range(self._player.getLife()):
            screen.blit(self._lifeimg,(840+(25*i),333))
        for i in range(self._player.getBomb()):
            screen.blit(self._bombimg,(840+(30*i),444))
        if self._player.getPower() == 200:
            x= "MAX"
        else:
            x= str(self._player.getPower())
        power = basicFont.render(x,True,BLACK)
        powerrect = graze.get_rect()
        powerrect.center = (885,575)
        screen.blit(power,powerrect)
    def drawPause(self,screen):
        self._clock.tick(10)
        screen.blit(self._background,(30,0))
        screen.fill(WHITE)
        centerx = screen.get_rect().centerx
        centery = screen.get_rect().centery
        basicFont = pygame.font.SysFont(None, 48)
        yes = basicFont.render("Yes",True,BLACK)
        no = basicFont.render("No",True,BLACK)
        yesRect = yes.get_rect()
        yesRect.center = (centerx,centery-100)
        noRect = no.get_rect()
        noRect.center =(centerx,centery)
        if self._resume:
            pygame.draw.rect(screen,BLUE,yesRect)
        else:
            pygame.draw.rect(screen,BLUE,noRect)
        screen.blit(yes,yesRect)
        screen.blit(no,noRect)
    def drawObjects(self,screen):
        screen.fill(BLACK)
        screen.blit(self._background,(30,0))
        if self._player.isBombing():
            now = pygame.time.get_ticks()
            elapsed = now - self._bombTime
            if elapsed < 2000:
                screen.fill(WHITE)
                self._bombingSound.play()
            elapsed = now - self._bombTime
            if 0 < elapsed <2500:
                score = len(self._activeBullets) * 10
                for i in self._activeBullets:
                    self._gameItems.remove(i)
                self._activeBullets = []

                temp = self._activeSpawners[:]
                for i in temp:
                    if i.getHP() is not None:
                        i.damage(1)
                        if i.getHP() < 0:
                            self._activeSpawners.remove(i)
                            self._deadSpawners.append(i.getPos())
                            self._gameItems.remove(i)
                if self._bossSpawn:
                    self._currentBoss.bombDamage(5)
                self.addScore(score)
            elif elapsed >3500:
                self._bombingSound.stop()
                self._player.doneBombing()
                screen.blit(self._background,(30,0))
                
        if self._bossSpawn and self._currentBoss.alive():
            screen.blit(self._currentBoss.getImage(),self._currentBoss.getRect())
            
        
        for spawner in self._activeSpawners:
            if spawner.getImage() is not None:
                screen.blit(spawner.getImage(),spawner.getRect())

        for i in self._activePlayerBullets:
            screen.blit(i.getImage(),i.getRect())

        for point in self._scorePoint: #extra points
            screen.blit(self._scoreImg,point.getRect())

        for power in self._powerPoint:#power ups
            screen.blit(self._powerImg,power.getRect())
        if self._player.getRespawn():
            now = pygame.time.get_ticks()
            if not now % 5 == 0:
                screen.blit(self._player.getImg(),self._player.getRect())
        else:
            screen.blit(self._player.getImg(),self._player.getRect())

        if self._player.slow():
            pygame.draw.circle(screen,RED,self._player.getPos(),5)
        
        for i in self._activeBullets:
            screen.blit(i.getImage(),i.getRect())
             
        for i in self._hitBullets:
            temp = self._hitImg.get_rect()
            temp.center = i
            screen.blit(self._hitImg,temp)
        
        for i in self._deadSpawners:
            temp = self._spawnerdeathImg.get_rect()
            temp.center = i
            screen.blit(self._spawnerdeathImg,temp)

        if self._bossSpawn:
            per = int(710 * self._currentBoss.getHPPercent())
            hp = pygame.Rect((30,0),(per,20))
            pygame.draw.rect(screen,GREEN,hp)
            for i in range(self._currentBoss.RemainingPhases()):
                pygame.draw.circle(screen,GREEN,(35+(10*i),30),5)
    def writeHighScore(self):
        playerlifetotal = 100000 * self._player.getLife()
        playerbombtotal = 50000 * self._player.getBomb()
        grazetotal = 10 * self._graze
        final = self._score + playerlifetotal+playerbombtotal + grazetotal
        if final > self._oldHighScore:

            f = open("score.txt","w")
            f.write(str(final))
            f.close()
    def drawGameOver(self,screen):
        screen.fill(BLACK)
        basicFont = pygame.font.SysFont("century", 40)
        gameovertext = basicFont.render("GAMEOVER",True,WHITE)
        gameoverrect = gameovertext.get_rect()
        gameoverrect.center = screen.get_rect().center
        screen.blit(gameovertext,gameoverrect)
        confirm = basicFont.render("Press Confirm to return to Menu",True,WHITE)
        confirmrect = confirm.get_rect()
        confirmrect.center = (screen.get_rect().centerx,screen.get_rect().centery+200)
        screen.blit(confirm,confirmrect)
    def stageAction(self):
        self._deadSpawners = []
        self._hitBullets = []
        
        time = int(self._time)        
        if time == self._bossTick and not self._bossSpawn:#init boss spawning & set false in the draw.
            pygame.mixer.music.load('bossMain.ogg')
            pygame.mixer.music.play(-1)
            self._bossSpawn = True
            for i in self._activeBullets:
                self._gameItems.remove(i)
            self._activeBullets = []
            for i in self._activeSpawners:
                self._gameItems.remove(i)
            self._activeSpawners = []
            self._activeSpawners += self._currentBoss.produceSpawners()
            self._gameItems.addRect(self._currentBoss)
        elif self._bossSpawn: #boss actions. will use spawner,activebullets          
                if self._currentBoss.alive():
                    if self._currentBoss.nextPhase():
                        points = len(self._activeBullets) *10
                        self.addScore(points)
                        for i in self._activeBullets:
                            self._gameItems.remove(i)
                        self._activeBullets = []
                        self._activeSpawners = []                      
                        self._activeSpawners+= self._currentBoss.produceSpawners()
                else:
                    self.writeHighScore()
                    self._gameItems.clear()
                    self._activePlayerBullets = []
                    pygame.mixer.music.load("Chippytoon.ogg")
                    pygame.mixer.music.play(-1)
                    self._activeBullets = []
                    self._activeSpawners = []
                    self._scoreScreen = True
                    self._bossSpawn = False
                    self._resume = False
                    self._wait = pygame.time.get_ticks()
        elif time != self._bossTick:#normal stages
            if time in self._stageSpawners:
                item = self._stageSpawners[time]
                addTime = pygame.time.get_ticks()
                for i in item:
                    i.setLast(addTime)
                self._activeSpawners += item
                x = self._stageSpawners[time]
                for i in x:
                    self._gameItems.addRect(i)
                del self._stageSpawners[time]
                
        #handles all movement for scores,spawners and bullets
        for bullet in self._activePlayerBullets:
            self._gameItems.remove(bullet)
            bullet.update()
            self._gameItems.addRect(bullet)
        for power in self._powerPoint:
            self._gameItems.remove(power)
            power.update()
            self._gameItems.addRect(power)
        for score in self._scorePoint:
            self._gameItems.remove(score)
            score.update()
            self._gameItems.addRect(score)
            
        for bullet in self._activeBullets:
            self._gameItems.remove(bullet)
            bullet.update(self._player.getPos())
            self._gameItems.addRect(bullet)
        #hit collision for spawners.
        for spawner in self._activeSpawners[:]:
            x = []
            for i in self._gameItems.retrieve(spawner):
                if i in self._activePlayerBullets:
                    x.append(i)     
            for i in x:
                if pygame.sprite.collide_circle(spawner,i) and spawner.getHP() != None:
                    spawner.damage(i.getDamage())
                    self._activePlayerBullets.remove(i)
                    self._gameItems.remove(i)
                    self._hitBullets.append(i.getPos())
                    
                    if not spawner.alive():
                        self._deadSpawnerSound.play()
                        self._deadSpawners.append(spawner.getPos())
                        self.addScore(10)
                        score = spawner.getScore()
                        for pos,value in score:
                            scorept = BonusBox(self._scoreImg,pos,value)
                            self._scorePoint.append(scorept)
                            self._gameItems.addRect(scorept)
                            
                        power = spawner.getPower()  
                        for pos,value in power:
                            powerpt = BonusBox(self._powerImg,pos,value)
                            self._powerPoint.append(powerpt)
                            self._gameItems.addRect(powerpt)
                        break
            if spawner.getComplete():
                self._activeSpawners.remove(spawner)
                self._gameItems.remove(spawner)    
        if self._bossSpawn and self._currentBoss.getHP() > 0:
            self._currentBoss.update()
            x = []
            for i in self._gameItems.retrieve(self._currentBoss):
                if i in self._activePlayerBullets:
                    x.append(i)
            for i in x:
                if pygame.sprite.collide_circle(self._currentBoss,i):
                    self._hitBulletSound.play()
                    self._activePlayerBullets.remove(i)
                    self._gameItems.remove(i)
                    self._hitBullets.append(i.getPos())
                    self._currentBoss.damage(i.getDamage())
                    
        for spawner in self._activeSpawners:
            self._gameItems.remove(spawner)
            spawner.update()
            
            x = spawner.produceBullets(self._player.getPos())
            self._gameItems.addRect(spawner)

            if  x != []:
                self._attackFire.play()
                #self._activeSpawnerFire.append(spawner.getPos())
                self._activeBullets += x
                for bullet in x:
                    self._gameItems.addRect(bullet)

                    
        #Player Hit Detection  
        items = self._gameItems.retrieve(self._player)
        for i in items[:]:
            if i in self._activePlayerBullets:
                items.remove(i)
        score = self._scorePoint[:]
        power = self._powerPoint[:]
        self._player.doneRespawn()
        for i in items:

            if i in self._activeSpawners:
                if i.getHP() == None:
                    continue
            if i in self._activeSpawners or i in self._activeBullets:
                if pygame.sprite.collide_rect(self._player,i):
                    self._graze +=1
                    self.addScore(1)
            if i in self._activeSpawners or i in self._activeBullets or i == self._currentBoss:
                if not self._player.getImmune():
                    deadPlayer = False
                    if i == self._currentBoss:
                        if pygame.sprite.collide_rect(i,self._player):
                            deadPlayer = True
                    elif pygame.sprite.collide_circle(self._player,i):
                        deadPlayer = True
                        
                    if deadPlayer:
                        for x in self._activeBullets:
                            self._gameItems.remove(x)
                        self._activeBullets = []
                        for x in self._activePlayerBullets:
                            self._gameItems.remove(x)
                        self._activePlayerBullets = []
                        self._player.playerDeath()
                        self._playerDie.play()
                        if not self._player.getAlive():
                            self._gameOver = True
                            self._resume = False
                            pygame.mixer.music.load("Icy Game Over.ogg")
                            pygame.mixer.music.play()
                        break
            if pygame.sprite.collide_rect(i,self._player):
                if i in power:
                    if self._player.getPower() == 200:
                        self.addScore(i.getValue())
                    else:
                        self._player.addPower(i.getValue())
                    self._itemSound.play()
                    self._powerPoint.remove(i)
                elif i in score:
                    self._itemSound.play()
                    self.addScore(i.getValue())
                    self._scorePoint.remove(i)
                self._gameItems.remove(i)
                


                    
        outBounds = self._gameItems.outOfBounds()
        for i in outBounds[:]:
            if i in self._activeSpawners or i == self._currentBoss:
                outBounds.remove(i)
        playerbullet = self._activePlayerBullets[:]
        enemybullet = self._activeBullets[:]
        score = self._scorePoint[:]
        power = self._powerPoint[:]
        for item in outBounds:
            if item in playerbullet:
                self._activePlayerBullets.remove(item)
            elif item in enemybullet:
                self._activeBullets.remove(item)
            elif item in score:
                self._scorePoint.remove(item)
            elif item in power:
                self._powerPoint.remove(item)
            self._gameItems.remove(item)
            
    def addScore(self,value):
        self._score +=value
        if self._score > self._highScore:
            self._highScore = self._score
            
