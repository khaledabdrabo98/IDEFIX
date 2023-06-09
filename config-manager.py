from src.com.receiver import Receiver
from src.com.tcpcom.tcpcom import TCPServer
import json
from time import sleep

from src.config import LED_COLORS, NB_ROBOTS, NB_CHATS, NB_SOURIS

# RASPBERRY_PI_IP_ADDRESS = "172.20.10.13" khaled tel
RASPBERRY_PI_IP_ADDRESS = "192.168.1.67"  # co box
# RASPBERRY_PI_IP_ADDRESS = "192.168.121.103" # co tel
# RASPBERRY_PI_IP_PORT = 5005 #khaled
RASPBERRY_PI_IP_PORT = 5005


def onStateChanged(state, msg):
    global isConnected
    if state == "LISTENING":
        print("PC:-- Listening...")
    elif state == "CONNECTED":

        print("PC:-- Connected to Raspberry Pi")
        print("PC:-- Sending configuration...")
        # init and send config
        config = {'nbrobots': NB_ROBOTS, 'colors': LED_COLORS,
                  'nbchats': NB_CHATS, 'nbsouris': NB_SOURIS}
        configSender.sendMessage(json.dumps(config))
        sleep(5)
        coordReceiver = Receiver(RASPBERRY_PI_IP_ADDRESS, RASPBERRY_PI_IP_PORT, False)
        coordReceiver.run()
        configSender.terminate()
        isConnected = True


def main():
    global configSender, coordReceiver
    configSender = TCPServer(RASPBERRY_PI_IP_PORT, stateChanged=onStateChanged)


if __name__ == '__main__':
    main()
