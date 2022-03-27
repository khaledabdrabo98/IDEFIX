from src.tcpcom.tcpcom import TCPClient
from time import sleep
import threading

# IP_ADDRESS = "192.168.1.151"
# IP_PORT = 65432
#
#
# class Client:
#     def __init__(self):
#         super().__init__()
#         self.isConnected = False
#
#     def onStateChanged(self, state, msg):
#         if state == "CONNECTING":
#             print("Client:-- Waiting for connection...")
#         elif state == "CONNECTED":
#             print("Client:-- Connection established.")
#         elif state == "DISCONNECTED":
#             print("Client:-- Connection lost.")
#             self.isConnected = False
#         elif state == "MESSAGE":
#             print("Client:-- Received data: ", msg)
#
#     def run(self):
#         tcpclient = TCPClient(IP_ADDRESS, IP_PORT, stateChanged=self.onStateChanged)
#         response_connection = tcpclient.connect()
#         if response_connection:
#             self.isConnected = True
#             while self.isConnected:
#                 print("Client:-- Sending command: go...")
#                 tcpclient.sendMessage("go")
#                 time.sleep(2)
#             print("Done")
#         else:
#             print("Client:-- Connection failed")
#
#
# if __name__ == '__main__':
#     Client().run()


server_ip = "192.168.1.151"
server_port = 65432


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        print("Client:-- Listening...")

    elif state == "CONNECTED":
        isConnected = True
        print("Client:-- Connected to ", msg)

    elif state == "DISCONNECTED":
        isConnected = False
        print("Client:-- Connection lost.")
        main()

    elif state == "MESSAGE":
        print("Client:-- Message received: ", msg)


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
                while isConnected:
                    print("Client:-- Sending command: go...")
                    client.sendMessage("go")
                    sleep(2)
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
