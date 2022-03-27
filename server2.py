from src.tcpcom.tcpcom import TCPServer

tcp_ip = "192.168.1.67"
tcp_port = 65432
tcp_reply = "Server message"


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        print("Server:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("Server:-- Connected to " + msg)
    elif state == "MESSAGE":
        print("Server:-- Message received: ", msg)
        server.sendMessage(tcp_reply)


def main():
    global server
    server = TCPServer(tcp_port, stateChanged=onStateChanged)


if __name__ == '__main__':
    main()
