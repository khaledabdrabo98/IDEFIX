from src.cam.image_analysis import PiCam
from src.tcpcom.tcpcom import TCPServer
from time import sleep
from random import randint
from threading import Thread

tcp_ip = "192.168.1.151"
tcp_port = 5432
tcp_reply = "Message received!"


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        isConnected = False
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
    # if isConnected:
    #     thread = Thread(target=PiCam().capture())
    #     thread.start()
    #     thread.join()
    while isConnected:
        # transfer real coords captured by cam
        x = randint(0, 1280)
        y = randint(0, 720)
        message = "[" + str(x) + ", " + str(y) + "]"
        print("Server:-- Sending coord: ", message)
        server.sendMessage("Coord: " + message)
        sleep(2)
    print("Done")


def main():
    global server
    server = TCPServer(tcp_port, stateChanged=onStateChanged)


if __name__ == '__main__':
    main()
