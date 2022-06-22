from http import client
from tdmclient import ClientAsync, aw
import numpy as np
import math
from src.Coord import Coord


class Robot:
    program =""""""
    mynode = 0
    clientRef = 0
    rayon = 0
    coord_list = []
    angle = 0
    behaviour = "cat"

    def __init__(self, client, nodeN):
        self.clientRef = client
        self.mynode = nodeN
        coord1 = Coord()
        coord2 = Coord()
        self.coord_list.append(coord1)
        self.coord_list.append(coord2)
        print(len(self.clientRef.nodes))
        

    async def prog(self):
            with await self.clientRef.nodes[self.mynode].lock() as node:
                #print(node)
                #print(self.mynode)
                #print(len(self.clientRef.nodes))
                error = await node.compile(self.program)
                if error is not None:
                    print(f"Compilation error: {error['error_msg']}")
                else:
                    error = await node.run()
                    if error is not None:
                        print(f"Error {error['error_code']}")
            print("done")

    def avancer(self):
        self.program = """
        motor.left.target=200
motor.right.target=200"""
        self.clientRef.run_async_program(self.prog)

    def stopper(self):
        self.program = """
        motor.left.target=0
motor.right.target=0"""
        self.clientRef.run_async_program(self.prog)

    def tournerDroiteSoft(self,duration):
        self.program = """
        timer.period[0] = """ + str(int(duration)) + """
motor.left.target = 200
motor.right.target = 100

onevent timer0
    motor.right.target = 200
    timer.period[0] = 0"""
        self.clientRef.run_async_program(self.prog)

    def tournerGaucheSoft(self,duration):
        self.program = """
timer.period[0] = """ + str(int(duration)) + """
motor.right.target = 200
 motor.left.target = 100

onevent timer0
    motor.left.target = 200
    timer.period[0] = 0
"""
        self.clientRef.run_async_program(self.prog)

    def tournerDroiteHard(self,duration):
        self.program = """
        timer.period[0] = """ + str(int(duration)) + """
motor.left.target = 500
motor.right.target = -500


onevent timer0
    motor.right.target = 200
    motor.left.target = 200
    timer.period[0] = 0"""
        self.clientRef.run_async_program(self.prog)

    def tournerGaucheHard(self,duration):
        print(duration)
        print(int(duration))
        self.program = """
timer.period[0] = """ + str(int(duration)) + """
motor.right.target = 500
motor.left.target = -500

onevent timer0
    motor.left.target = 200
    motor.right.target = 200
    timer.period[0] = 0
"""
        self.clientRef.run_async_program(self.prog)

    def accelerer(self, x):
        if x <= 200:
            self.program = """motor.left.target="""+x+""""motor.right.target="""+x
            self.clientRef.run_async_program(self.prog)

    def ralentir(self):
        self.program = """
        motor.left.target=100
        motor.right.target=100"""
        self.clientRef.run_async_program(self.prog)

    def updateRayon(self, r):
        self.rayon = r

    def updateCoord(self, x, y):
        self.coord_list[1].x = self.coord_list[0].x
        self.coord_list[1].y = self.coord_list[0].y
        self.coord_list[0].x = x
        self.coord_list[0].y = y
        self.calculOrientation()

    def calculOrientation(self):
        vecteurReference = []
        vecteurReference.append(6)
        vecteurReference.append(0)
        vecteurRobot = []
        vecteurRobot.append(self.coord_list[0].x - self.coord_list[1].x)
        vecteurRobot.append(self.coord_list[0].y - self.coord_list[1].y)
        #print("X vecteur Robot : ", vecteurRobot[0])
        #print("y vecteur Robot : ", vecteurRobot[1])
        produitScalaire = np.dot(vecteurReference, vecteurRobot)
        #print("Produit scalaire : ", produitScalaire)
        a = np.array((self.coord_list[0].x, self.coord_list[0].y))
        b = np.array((self.coord_list[1].x, self.coord_list[1].y))
        distanceVecteurRobot = np.linalg.norm(b - a)
        #print("Distance du vecteur : ", distanceVecteurRobot)
        cosAngle = (1.0*produitScalaire)/(1.0*(distanceVecteurRobot*6))
        #print("Cosinus : ", cosAngle)
        if self.coord_list[1].y > self.coord_list[0].y:
            self.angle = - math.degrees(np.arccos(cosAngle))
        else:
            self.angle = math.degrees(np.arccos(cosAngle))
        #print(self.angle)

