import src.IA
from src.Robot import Robot
from tdmclient import ClientAsync, aw
import time
from src.com.receiver import Receiver
from src.com.tcpcom.tcpcom import TCPServer
import json
from src.utils import centre_shape

# RASPBERRY_PI_IP_ADDRESS = "172.20.10.13" #khaled
RASPBERRY_PI_IP_ADDRESS = "192.168.1.67"
RASPBERRY_PI_IP_PORT = 5005

configSent = False
coordReceiver = Receiver(RASPBERRY_PI_IP_ADDRESS, RASPBERRY_PI_IP_PORT, False)


def onStateChanged(state, msg):
    global isConnected
    if state == "LISTENING":
        print("PC:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("PC:-- Connected to Raspberry Pi")
        print("PC:-- Sending configuration...")
        global configSent
        configSent = True
        # init and send config
        configInit = {'nbrobots': src.config.NB_ROBOTS, 'colors': src.config.LED_COLORS,
                      'nbchats': src.config.NB_CHATS, 'nbsouris': src.config.NB_SOURIS}
        global configSender
        configSender.sendMessage(json.dumps(configInit))

        global coordReceiver
        # coordReceiver = Receiver(RASPBERRY_PI_IP_ADDRESS, RASPBERRY_PI_IP_PORT, False)
        coordReceiver.run()
        configSender.terminate()


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

    global configSender  # , coordReceiver#, configSent
    # configSent = False

    configSender = TCPServer(RASPBERRY_PI_IP_PORT, stateChanged=onStateChanged)

    print("je passe ici")

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
        if rob.behaviour == "cat":
            cat = src.IA.Cat(rob)
            IACatList.append(cat)
            print("create 1 cat")
        elif rob.behaviour == "mouse":
            mouse = src.IA.Mouse(rob)
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

    while not configSent:  # attente de la finalisation de la config
        time.sleep(1)
        print("j'attend la config 1sec")
    print("sortie de boucle")

    flux = coordReceiver.getCoordFlux()
    while flux == []:  # attente des premières coord
        time.sleep(1)
        flux = coordReceiver.getCoordFlux()

    time.sleep(1)  # securite pour la detection coord

    while (time.time() - start_time) < 25:
        time.sleep(1)
        actual_time = time.time()
        if (actual_time - IACatList[0].sleep_required) >= (IACatList[0].lastSupplied):
            # tout ce parsing permet de lire la position du 1er carré vert detecté (supposé être le robot)
            flux = str(coordReceiver.getCoordFlux())
            print("mon flux" + str(flux))
            if flux != "{\"red\": null, \"green\": null}":
                coord = [0, 0, 0, 0]
                while flux[0] != ':':  # remove red name
                    flux = flux[1:]
                flux = flux[1:]  # remove red's ':'
                while flux[0] != ':':  # remove red data and green name
                    flux = flux[1:]
                flux = flux[1:]  # remove green's ':'
                flux = flux[1:]  # remove ' '
                flux = flux[1:]  # remove '''
                print(flux)
                for i in range(4):
                    coord[i] = 0
                    while (flux[0] == '0' or flux[0] == '1' or flux[0] == '2' or flux[0] == '3' or flux[0] == '4' or
                           flux[0] == '5' or flux[0] == '6' or flux[0] == '7' or flux[0] == '8' or flux[0] == '9'):
                        coord[i] *= 10
                        coord[i] += int(flux[0])
                        flux = flux[1:]
                    print(coord[i])
                    flux = flux[1:]  # remove the ','

                """all_coords = flux.split(";")
                print(all_coords)
                coord = all_coords[0].split(",")
                print (coord)"""
                center = centre_shape(int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))
                IACatList[0].robotControled.updateCoord(center[0], center[1])
                IACatList[0].robotControled.updateRayon(coord[2] - coord[0])  # w-x

        for cat in IACatList:
            cat.objectif.x == 1000
            cat.objectif.y == -200
            cat.robotControled.ralentir()
            # cat.move()
            # cat.robotControled.updateCoord(cat.robotControled.coord_list[0].x * 2,
            # cat.robotControled.coord_list[0].y * 2)
            # mytime = time.time()
            # print(mytime - start_time)

    # time.sleep(3)
    triche = RobotList

    for rob2 in triche:
        rob2.stopper()

        mytime = time.time()
        print(mytime - start_time)
