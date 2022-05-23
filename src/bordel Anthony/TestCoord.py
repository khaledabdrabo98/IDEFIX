import IA
from Robot import Robot
from http import client
from tdmclient import ClientAsync, aw
import time

class TestCoord:
    localclient = ClientAsync(debug=0)
    temp = Robot(localclient, 0)
    temp.updateCoord(0, 10)
    temp.updateCoord(-10, 11)
