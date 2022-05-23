import IA
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
    localclient = ClientAsync(debug=0)
    print(localclient.process_waiting_messages())
    program = """"""
    async def prog():
            with await localclient.lock() as node:
                print("in init")
                print(node)
                print(len(localclient.nodes))
                error = await node.compile(program)
                if error is not None:
                    print(f"Compilation error: {error['error_msg']}")
                else:
                    error = await node.run()
                    if error is not None:
                        print(f"Error {error['error_code']}")
            print("done")
            
    localclient.run_async_program(prog)

    print("after init")
    print(len(localclient.nodes))
    NBROBOT = len(localclient.nodes)
    start_time = time.time()
    if(NBROBOT >0):
        cptCreatedRobot = 0
        temp = Robot(localclient,cptCreatedRobot)
        RobotList= [temp]
        while(cptCreatedRobot < NBROBOT-1):
            cptCreatedRobot+=1
            newRob = Robot(localclient,cptCreatedRobot)
            RobotList.append(newRob)

    for rob in RobotList:
        rob.tournerGauche()

        mytime = time.time()
        print(mytime - start_time)


    time.sleep(2)
    triche = RobotList
            

    for rob2 in triche:
        rob2.stopper()

        mytime = time.time()
        print(mytime - start_time)
