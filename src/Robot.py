from http import client
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