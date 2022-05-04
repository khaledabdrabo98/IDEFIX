from src.tcpcom.tcpcom import TCPClient
import json

class Client:
    def __init__(self, ipaddress, port):
        super().__init__()
        self.ipaddress = ipaddress
        self.port = port
        self.isConnected = False

    def onStateChanged(self, state, msg):
        if state == "CONNECTING":
            print("Client:-- Waiting for connection...")
        elif state == "CONNECTED":
            print("Client:-- Connected to Raspberry Pi server!")
        elif state == "DISCONNECTED":
            print("Client:-- Connection lost.")
            self.isConnected = False
        elif state == "MESSAGE":
            print("Client:-- Received data: ", msg)
            if msg == "CONFIG OK":
                print("Client:-- Configuration accepted, begin coord reception")
            elif msg == "CONFIG NOT OK":
                print("Client:-- Configuration not accepted, please change config format and retry.")
            else:
                print("Client:-- Received data: ", msg)

    def run(self):
        tcpclient = TCPClient(self.ipaddress, self.port, stateChanged=self.onStateChanged)
        response_connection = tcpclient.connect()
        if response_connection:
            self.isConnected = True
            # init and send config
            config = {}
            config['nbrobots'] = 4
            tcpclient.sendMessage("Hello")
            tcpclient.sendMessage(json.dumps(config))
            print(config)
            print(json.dumps(config))
            print("Sending configuration...")
        else:
            print("Client:-- Connection failed, please check the server is UP.")
