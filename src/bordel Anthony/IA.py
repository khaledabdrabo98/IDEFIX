import Robot
from Coord import Coord
import numpy as np
import math

class IA:

    robotControled = 0
    lastSupplied = 0
    def __init__(self, robotLinked):
        self.robotControled = robotLinked


class Cat(IA):

    objectif = Coord()
    objectif.x = 10
    objectif.y = 10

    def __init__(self, robotLinked):
        super().__init__(robotLinked)

    def calcul_angle_vers_objectif(self):

        vecteurReference = []
        vecteurReference.append(6)
        vecteurReference.append(0)
        vecteurRobot = []
        angleObjectif = 0
        vecteurRobot.append(self.objectif.x - self.robotControled.coord_list[0].x)
        vecteurRobot.append(self.objectif.y - self.robotControled.coord_list[0].y)
        produitScalaire = np.dot(vecteurReference, vecteurRobot)
        a = np.array((self.objectif.x, self.objectif.y))
        b = np.array((self.robotControled.coord_list[0].x, self.robotControled.coord_list[0].y))
        distanceVecteurRobot = np.linalg.norm(b - a)
        cosAngle = (1.0 * produitScalaire) / (1.0 * (distanceVecteurRobot * 6))

        if self.robotControled.coord_list[0].y > self.objectif.y:
            angleObjectif = - math.degrees(np.arccos(cosAngle))
        else:
            angleObjectif = math.degrees(np.arccos(cosAngle))

        print("angle objectif ",angleObjectif)

        angleRobot = self.robotControled.angle
        print("angle robot ", angleRobot)

        print(angleObjectif - angleRobot)
        return angleObjectif - angleRobot


    

class Mouse(IA):
    def __init__(self, robotLinked, ext2):
        super().__init__(robotLinked)
        self.mouseExtraVar = ext2

