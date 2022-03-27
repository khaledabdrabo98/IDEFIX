from src.cam.image_analysis import PiCam
from src.tcpcom.tcpcom import TCPServer
from time import sleep
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
    global cam

    if isConnected:
        cam = PiCam()
        thread = Thread(target=cam.capture())
        thread.start()
        thread.join()
    while isConnected:
        # transfer real coords captured by cam
        print("Server:-- Sending red LED coord: ", cam.coord_red_led)
        print("Server:-- Sending green LED coord: ", cam.coord_green_led)
        server.sendMessage("Red LED coord: " + cam.coord_red_led + "\nGreen LED coord: " + cam.coord_green_led + "\n")
        sleep(1)


def main():
    global server
    server = TCPServer(tcp_port, stateChanged=onStateChanged)


if __name__ == '__main__':
    main()
