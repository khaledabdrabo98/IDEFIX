import Robot
import Coord

class IA:
    robotControled = 0
    lastSupplied = 0
    def __init__(self, robotLinked):
        self.robotControled = robotLinked

class Cat(IA):
    objectifList = []
    def __init__(self, robotLinked, ext):
        super().__init__(robotLinked)
        objectif = Coord()
        objectif.x = 100
        objectif.y = 100
        self.objectifList.append(objectif)
        self.catExtraVar = ext

    

class Mouse(IA):
    def __init__(self, robotLinked, ext2):
        super().__init__(robotLinked)
        self.mouseExtraVar = ext2

