from .tcpcom.tcpcom import TCPClient
import time

IP_ADDRESS = "192.168.1.67"
IP_PORT = 22000


class Client:
    def __init__(self):
        super.__init__()
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
            print("Client:-- Received data:", msg)

    def run(self):
        tcpclient = TCPClient(IP_ADDRESS, IP_PORT, stateChanged=self.onStateChanged())
        response_connection = tcpclient.connect()
        if response_connection:
            self.isConnected = True
            while self.isConnected:
                print("Client:-- Sending command: go...")
                tcpclient.sendMessage("go")
                time.sleep(2)
            print("Done")
        else:
            print("Client:-- Connection failed")


if __name__ == '__main__':
    client = Client()
    client.run()
