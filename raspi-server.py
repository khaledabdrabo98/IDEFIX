from src.cam.image_analysis import PiCam
from src.tcpcom.tcpcom import TCPServer
from time import sleep

tcp_ip = "192.168.1.151"
tcp_port = 5432
tcp_reply = "Message received!"


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        print("Server:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("Server:-- Connected to " + msg)
        server.sendMessage("Hello, client!")
        talkWhileConnected()
    elif state == "MESSAGE":
        print("Server:-- Message received: ", msg)
        server.sendMessage(tcp_reply)


def talkWhileConnected():
    if isConnected:
        cam = PiCam().capture()
    while isConnected:
        # transfer real coords captured by cam
        print("Server:-- Sending coord: [x1, y1]..")
        server.sendMessage("Coord test")
        sleep(2)
    print("Done")


def main():
    global server
    server = TCPServer(tcp_port, stateChanged=onStateChanged)


if __name__ == '__main__':
    main()
