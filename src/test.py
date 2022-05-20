from http import client
import time
from tdmclient import ClientAsync, aw


class Robot :
    program =""""""
    node = 0
    client = 0
    def __init__(self):
        self.client = ClientAsync(debug=0)
        print(len(self.client.nodes))
        

    async def prog(self):
            with await self.client.lock() as node:
                print(node)
                print(len(self.client.nodes))
                
                
                
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
        self.client.run_async_program(self.prog)

    def stopper(self):
        self.program="""
        motor.left.target=0
motor.right.target=0"""
        self.client.run_async_program(self.prog)
        
        


    
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
    print(len(localclient.nodes))
    #node = client.nodes[0]
    firstRobot = Robot()
    firstRobot.avancer()
    #time.sleep(3)
    
    secondRobot = Robot()
    secondRobot.avancer()
    time.sleep(3)
    secondRobot.stopper()
    firstRobot.stopper()    