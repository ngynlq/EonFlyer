BOUND = -1
class SpatialHash:
    def __init__(self,cellwidth,cellheight,offsetx,offsety):
        self.dict = {}
        self.offsetx = offsetx
        self.offsety = offsety
        self.yBoxes = int(690 / cellheight)
        self.xBoxes = int(710 / cellwidth)
        for i in range(self.yBoxes):
            for j in range(self.xBoxes):
                self.dict[(i,j)] = []
        self.cellheight = cellheight
        self.cellwidth = cellwidth
        self.dict[BOUND] = []
    def _hash(self,point):
        x = int((point[0]-self.offsetx)/self.cellwidth)
        y = int((point[1]+self.offsety)/self.cellheight)
        if (point[0]-self.offsetx) < 0:
            x = -1
        elif (point[1] + self.offsety) <0:
            y = -1
        return x,y
    def addRect(self,item):
        box = item.getRect()
        minpt, maxpt = self._hash(box.bottomleft), self._hash(box.topright)
        for i in range(minpt[0],maxpt[0]+1):
            for j in range(maxpt[1],minpt[1]+1):
                if (i,j) in self.dict:
                    self.dict[(i,j)].append(item)
                elif item not in self.dict[BOUND]:#only add to the outofbounds once
                    self.dict[BOUND].append(item)
    def remove(self,item):
        box = item.getRect()
        minpt, maxpt = self._hash(box.bottomleft), self._hash(box.topright)
        for i in range(minpt[0],maxpt[0]+1):
            for j in range(maxpt[1],minpt[1]+1):
                if (i,j) in self.dict:
                    if item in self.dict[(i,j)]:
                        self.dict[(i,j)].remove(item)
                elif item in self.dict[BOUND]:
                    self.dict[BOUND].remove(item)
    def outOfBounds(self):
        temp = []
        for i in self.dict[BOUND]:
            x = list(set(self.getKey(i)))
            if x == [BOUND]:
                temp.append(i)
        return temp
    def getKey(self,item):
        box = item.getRect()
        temp = []
        minpt, maxpt = self._hash(box.bottomleft), self._hash(box.topright)
        for i in range(minpt[0],maxpt[0]+1):
            for j in range(maxpt[1],minpt[1]+1):
                if (i,j) in self.dict:
                    temp.append((i,j))
                elif item in self.dict[BOUND]:
                    temp.append(BOUND)
        return temp
    def update(self,item):
        box = item.getRect()
    def retrieve(self,item):
        box = item.getRect()
        temp = []
        minpt, maxpt = self._hash(box.bottomleft), self._hash(box.topright)
        for i in range(minpt[0],maxpt[0]+1):
            for j in range(maxpt[1],minpt[1]+1):
                if (i,j) in self.dict:
                    temp.append((i,j))
                elif item in self.dict[BOUND]:
                    temp.append(BOUND)
        items = []
        for key in temp:
            x = self.dict[key]
            for i in x:
                if i not in items:
                    items.append(i)
        return items
    def clear(self):
        for i in range(self.xBoxes):
            for j in range(self.yBoxes):
                self.dict[(i,j)] = []
        self.dict[BOUND] = []

        

            
                    
        
        
