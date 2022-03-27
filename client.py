from src.tcpcom.tcpcom import TCPClient
from time import sleep

IP_ADDRESS = "192.168.1.67"
IP_PORT = 65432


class Client:
    def __init__(self):
        super().__init__()
        self.isConnected = False

    def onStateChanged(self, state, msg):
        if state == "CONNECTING":
            print("Client:-- Waiting for connection...")
        elif state == "CONNECTED":
            print("Client:-- Connection established.")
        elif state == "DISCONNECTED":
            print("Client:-- Connection lost.")
            self.isConnected = False
        elif state == "MESSAGE":
            print("Client:-- Received data: ", msg)

    def run(self):
        tcpclient = TCPClient(IP_ADDRESS, IP_PORT, stateChanged=self.onStateChanged)
        response_connection = tcpclient.connect()
        if response_connection:
            self.isConnected = True
            while self.isConnected:
                print("Client:-- Sending command: go...")
                tcpclient.sendMessage("go")
                sleep(2)
            print("Done")
        else:
            print("Client:-- Connection failed, please check the server is UP.")


if __name__ == '__main__':
    Client().run()
