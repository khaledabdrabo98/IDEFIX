from http import client
import time
from tdmclient import ClientAsync, aw


class Robot :
    program =""""""
    mynode = 0
    clientRef = 0
    def __init__(self,client,nodeN):
        self.clientRef = client
        self.mynode = nodeN
        print(len(self.clientRef.nodes))
        

    async def prog(self):
            with await self.clientRef.nodes[self.mynode].lock() as node:
                print(node)
                print(self.mynode)
                print(len(self.clientRef.nodes))
                error = await node.compile(self.program)
                if error is not None:
                    print(f"Compilation error: {error['error_msg']}")
                else:
                    error = await node.run()
                    if error is not None:
                        print(f"Error {error['error_code']}")
            print("done")

    def avancer(self):
        self.program="""
        motor.left.target=200
motor.right.target=200"""
        self.clientRef.run_async_program(self.prog)

    def stopper(self):
        self.program="""
        motor.left.target=0
motor.right.target=0"""
        self.clientRef.run_async_program(self.prog)
        
        


    
"""
    def __init__(self,x,y,orientation,statut,role,protocoleIA,couleur):
        client = ClientAsync()
        node = client.aw(client.wait_for_node())
        if (x <= max) :
            self.coordX = x
        if (y <= max) :
            self.coordY = y
        if (orientation < 359) :
            self.orientation = orientation
        self.statut = statut
        self.role = role
        self.protocoleIA = protocoleIA
        self.couleur = couleur
    """	



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
        