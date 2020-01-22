'''
fields = [field1,field2,field,etc...] a list of fields or shapes where bullets
start to spawn at.
sprites = [[bullet,bullet2],[bullet1],[bullet2]]
pathsX and Y = [[bullet1path,bullet2path],[bullet1path,path2]] sizes of sprites and paths
must match.
randoms = [[True,False],[bullet1path,bulletpath2]]
waits = [[1,0],[0,0] ]
num = [[None,156],[100,450]]

shouldnot be a list for each onr.
'''

#pretty much im passing function names of generators and then having the
#class create the generators from the names.
class BulletInfo:
    def __init__(self,bulletType,paths,rotate,createTime,wait,posProduce,patternTrack=None,tracktime = None,trackPath=None,trackSpeed=None,trackArgs =[],kill=False):
        self.bulletImg = bulletType
        self.paths = paths #movement x,y
        self.createTime = createTime
        self.rotate = rotate #img rotation.
        self.wait = wait
        self.trackTime = tracktime
        self.trackPath = trackPath
        self.trackSpeed = trackSpeed
        self.kill = kill
        self.produce = posProduce
        self.trackArgs =trackArgs
        self.trackPattern = patternTrack
