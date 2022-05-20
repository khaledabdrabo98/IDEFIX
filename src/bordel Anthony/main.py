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
      
    print(len(localclient.nodes))
    #node = client.nodes[0]
    print(localclient.nodes[0])
    print(localclient.nodes[1])

    #crea robot 1 et avance
    firstRobot = Robot(localclient,0)
    print("1er robot avance")
    """firstRobot.avancer()
    time.sleep(3)
    firstRobot.stopper()"""
    
    #crea robot 2 et avance
    secondRobot = Robot(localclient,1)
    """print("2e robot avance")
    secondRobot.avancer()
    time.sleep(3)
    secondRobot.stopper()"""

    #les cinq avancent en meme temps
    thridRobot = Robot(localclient,2)
    fourthRobot = Robot(localclient,3)
    fifthRobot = Robot(localclient,4)
    print("2e robot avance")
    secondRobot.avancer()
    print("1er robot avance")
    firstRobot.avancer()
    thridRobot.avancer()
    fourthRobot.avancer()
    fifthRobot.avancer()
    time.sleep(3)
    secondRobot.stopper()
    firstRobot.stopper()
    thridRobot.stopper()
    fourthRobot.stopper()
    fifthRobot.stopper()