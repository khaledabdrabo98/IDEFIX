from IA import Cat
from Robot import Robot
from http import client
from tdmclient import ClientAsync, aw
import time

class TestCoord:
    localclient = ClientAsync(debug=0)
    temp = Robot(localclient, 0)
    temp.updateCoord(0, 1)
    cat = Cat(temp)
    cat.calcul_angle_vers_objectif()
