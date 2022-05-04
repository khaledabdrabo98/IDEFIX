from src.tcpcom.tcpcom import TCPClient
from time import sleep
import threading

server_ip = "172.20.10.3"
server_port = 5005


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        print("DEBUG: Client:-- Listening...")

    elif state == "CONNECTED":
        isConnected = True
        print("DEBUG: Client:-- Connected to ", msg)

    elif state == "DISCONNECTED":
        isConnected = False
        print("DEBUG: Client:-- Connection lost.")
        main()

    elif state == "MESSAGE":
        print("DEBUG: Client:-- Message received: ", msg)


def main():
    global client

    client = TCPClient(server_ip, server_port, stateChanged=onStateChanged)
    print("Client starting")

    try:
        while True:
            rc = client.connect()
            sleep(0.01)
            if rc:
                isConnected = True
                client.sendMessage("Can you receive this?")
                while isConnected:
                    sleep(0.001)
            else:
                print("Client:-- Connection failed")
                sleep(0.1)
    except KeyboardInterrupt:
        pass

    # missin done; close connection
    client.disconnect()
    threading.cleanup_stop_thread()  # needed if we want to restart the client


if __name__ == '__main__':
    main()