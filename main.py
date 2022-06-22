import src.IA
from src.Robot import Robot
from tdmclient import ClientAsync, aw
import time
from src.com.receiver import Receiver
from src.com.tcpcom.tcpcom import TCPServer
import json
from src.utils import centre_shape

#RASPBERRY_PI_IP_ADDRESS = "172.20.10.13" #khaled
RASPBERRY_PI_IP_ADDRESS = "192.168.1.67"
RASPBERRY_PI_IP_PORT = 5005


def onStateChanged(state, msg):
    global isConnected
    if state == "LISTENING":
        print("PC:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("PC:-- Connected to Raspberry Pi")
        print("PC:-- Sending configuration...")
        # init and send config
        configInit = {'nbrobots': src.config.NB_ROBOTS, 'colors': src.config.LED_COLORS,
                      'nbchats': src.config.NB_CHATS, 'nbsouris': src.config.NB_SOURIS}
        configSender.sendMessage(json.dumps(configInit))
        coordReceiver = Receiver(RASPBERRY_PI_IP_ADDRESS, RASPBERRY_PI_IP_PORT, False)
        coordReceiver.run()
        configSender.terminate()
        configSent = True


"""firstRobot = IA.Robot()
secondRobot = IA.Robot()

from IA import *
thridRobot = Robot()

robotList = []
robotList.append(firstRobot)
robotList.append(secondRobot)"""

if __name__ == '__main__':
    start_time = time.time()
    previous_request = 0

    global configSender, coordReceiver, configSent
    configSent = False
    configSender = TCPServer(RASPBERRY_PI_IP_PORT, stateChanged=onStateChanged)

    # INIT -> fake program to start the link and to know how many robots are connected
    localclient = ClientAsync(debug=0)
    print(localclient.process_waiting_messages())
    program = """"""


    async def prog():
        with await localclient.lock() as node:
            print("init")
            # print(node)
            # print(len(localclient.nodes))
            error = await node.compile(program)
            if error is not None:
                print(f"Compilation error: {error['error_msg']}")
            else:
                error = await node.run()
                if error is not None:
                    print(f"Error {error['error_code']}")
        print("done")


    localclient.run_async_program(prog)
    previous_request = time.time()
    # END INIT

    # print("after init")
    # print(len(localclient.nodes))

    # Listing des Robots
    NBROBOT = len(localclient.nodes)
    start_time = time.time()
    previous_request = 0
    RobotList = []
    if NBROBOT > 0:
        cptCreatedRobot = 0
        firstRobot = Robot(localclient, cptCreatedRobot)
        RobotList.append(firstRobot)
        while cptCreatedRobot < (NBROBOT - 1):
            cptCreatedRobot += 1
            nextRob = Robot(localclient, cptCreatedRobot)
            RobotList.append(nextRob)

    # Association Robot -> coord from cam + chat souris ?

    # attribution des robots aux IA souhaitées
    IACatList = []
    IAMouseList = []
    for rob in RobotList:
        if (rob.behaviour == "cat"):
            cat = IA.Cat(rob)
            IACatList.append(cat)
        elif (rob.behaviour == "mouse"):
            mouse = IA.Mouse(rob)
            IAMouseList.append(mouse)

    '''
    while(True): #boucle d'actualisation
        #receiveCoordFromCam()
        #applyThemToRobotCoord()
        if (previous_request - start_time > config.TRANSPILATION_TIME):
        for rob in RobotList:
            #if (canSend): #timebased
                #doDecision&anction()"""
    '''

    while configSent and (time.time() - start_time < 10):

        flux = coordReceiver.getCoordFlux()['green']
        if new_coord is not None:
            all_coords = flux.split(";")
            coord = all_coords[0].split(",")
            center = centre_shape(coord[0], coord[1], coord[2], coord[3])
            IACatList[0].updateCoord(center[0], center[1])
            IACatList[0].updateRayon(coord[2] - coord[0])  # w-x

        for cat in IACatList:
            cat.move()
            cat.objectif.x += 10
            cat.objectif.y += 3
            cat.robotControled.updateCoord(cat.robotControled.coord_list[0].x * 2,
                                           cat.robotControled.coord_list[0].y * 2)
            # mytime = time.time()
            # print(mytime - start_time)

    # time.sleep(3)
    triche = RobotList

    for rob2 in triche:
        rob2.stopper()

        mytime = time.time()
        print(mytime - start_time)
