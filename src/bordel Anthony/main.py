import IA
import config
from Robot import Robot
from http import client
from tdmclient import ClientAsync, aw
import time


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

    # INIT -> fake program to start the link and to know how many robots are connected
    localclient = ClientAsync(debug=0)
    print(localclient.process_waiting_messages())
    program = """"""
    async def prog():
            with await localclient.lock() as node:
                print("init")
                #print(node)
                #print(len(localclient.nodes))
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
    #END INIT

    #print("after init")
    #print(len(localclient.nodes))

    # Listing des Robots
    NBROBOT = len(localclient.nodes)
    start_time = time.time()
    previous_request = 0
    RobotList=[]
    if(NBROBOT >0):
        cptCreatedRobot = 0
        firstRobot = Robot(localclient,cptCreatedRobot)
        RobotList.append(firstRobot)
        while(cptCreatedRobot < NBROBOT-1):
            cptCreatedRobot+=1
            nextRob = Robot(localclient,cptCreatedRobot)
            RobotList.append(nextRob)

    #Association Robot -> coord from cam + chat souris ?

    #attribution des robots aux IA souhaitées
    IACatList = []
    IAMouseList = []
    for rob in RobotList:
        if(rob.behaviour == "cat"):
            IACatList.append(rob)
        elif(rob.behaviour == "mouse"):
            IAMouseList.append(rob)



    while(True): #boucle d'actualisation
        #receiveCoordFromCam()
        #applyThemToRobotCoord()
        if (previous_request - start_time > config.TRANSPILATION_TIME):
        for rob in RobotList:
            if (canSend): #timebased
                #doDecision&anction()"""


    
    for rob in RobotList:
        rob.tournerDroiteHard(2000)

        mytime = time.time()
        print(mytime - start_time)


    time.sleep(3)
    triche = RobotList
            

    for rob2 in triche:
        rob2.stopper()

        mytime = time.time()
        print(mytime - start_time)
