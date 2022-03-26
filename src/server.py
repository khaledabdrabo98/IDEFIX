from cam.image_analysis import PiCam
from .tcpcom.tcpcom import TCPServer

IP_PORT = 22000


class Server:
    def __init__(self):
        super.__init__()
        self.tcpserver = TCPServer(IP_PORT, stateChanged=self.onStateChanged())

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
    cam = PiCam()
    data = cam.capture()
    Server().__init__()
