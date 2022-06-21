import src.IA
import src.config
from src.Robot import Robot
from http import client
from tdmclient import ClientAsync, aw
import time


class TestCoord:
    localclient = ClientAsync(debug=0)
    temp = Robot(localclient, 0)
    temp.coord_list[0].x = 0
    temp.coord_list[0].y = 0
    cat = IA.Cat(temp)
    cat.objectif.x = 10
    cat.objectif.y = 10
    cat.calcul_angle_vers_objectif()

    time.sleep(3)
    cat.robotControled.stopper()
