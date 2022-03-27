from src.cam.image_analysis import PiCam
from src.tcpcom.tcpcom import TCPServer

IP_PORT = 631


class Server:
    def __init__(self):
        super().__init__()
        self.tcpserver = TCPServer(IP_PORT, stateChanged=self.onStateChanged)

    def onStateChanged(self, state, msg):
        if state == "LISTENING":
            print("Server:-- Listening...")
        elif state == "CONNECTED":
            print("Server:-- Connected to", msg)
        elif state == "MESSAGE":
            print("Server:-- Message received:", msg)
            if msg == "go":
                self.tcpserver.sendMessage("[DATA]")


if __name__ == '__main__':
    data = PiCam().capture()
    Server().__init__()
