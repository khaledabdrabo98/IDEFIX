from asyncio import sleep
import src.Robot
import src.config
from src.Coord import Coord
import numpy as np
import math
import time


class IA:

    robotControled = 0
    lastSupplied = 0
    sleep_required = 0
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

    def move(self):
        actual_time = time.time()
        if ((actual_time - self.sleep_required) >= (self.lastSupplied)):
            print(actual_time)
            angle = int(self.calcul_angle_vers_objectif())
            if (angle>45 ):
                self.robotControled.tournerGaucheHard((angle*config.DURATION_VERYHARD)/360)
                self.sleep_required = (((angle*config.DURATION_VERYHARD)/360)/1000) +0.5
            elif (angle>0):
                self.robotControled.tournerGaucheSoft((angle*config.DURATION_SOFT)/360)
                self.sleep_required = (((angle*config.DURATION_SOFT)/360)/1000) +0.5

            elif (angle <-45):
                angle = -angle
                self.robotControled.tournerDroiteHard((angle*config.DURATION_VERYHARD)/360)
                self.sleep_required = (((angle*config.DURATION_VERYHARD)/360)/1000) +0.5
            elif (angle <0):
                angle = -angle
                self.robotControled.tournerDroiteSoft((angle*config.DURATION_SOFT)/360)
                self.sleep_required = (((angle*config.DURATION_SOFT)/360)/1000) +0.5
            else: #angle = 0
                self.robotControled.avancer()
                self.sleep_required = 0
            self.lastSupplied = time.time()
            print("j'attend " +str(self.sleep_required)+"sec")






    

class Mouse(IA):
    def __init__(self, robotLinked, ext2):
        super().__init__(robotLinked)
        self.mouseExtraVar = ext2

