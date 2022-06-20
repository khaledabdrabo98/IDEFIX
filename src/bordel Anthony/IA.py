import Robot
import Coord

class IA:
    robotControled = 0
    lastSupplied = 0
    def __init__(self, robotLinked):
        self.robotControled = robotLinked

class Cat(IA):
    objectif = Coord()
    objectif.x = 100
    objectif.y = 100
    def __init__(self, robotLinked):
        super().__init__(robotLinked)

    def calcul_angle_vers_objectif():
        #TODO


    

class Mouse(IA):
    def __init__(self, robotLinked, ext2):
        super().__init__(robotLinked)
        self.mouseExtraVar = ext2

