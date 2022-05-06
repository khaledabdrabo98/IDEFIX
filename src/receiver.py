from src.tcpcom.tcpcom import TCPClient
from src.utils import is_json
import json

raspberry_pi = "Raspberry Pi"
pc = "PC"
waiting_for_config = "Waiting for configuration..."
config_received_reply = "Configuration received!"
config_false_format_reply = "Bad configuration format, please retry"
tcp_start_sending_coord = "Start sending coordinates..."


class Receiver:
    def __init__(self, ipaddress, port, validateConfigMode):
        super().__init__()
        self.ipaddress = ipaddress
        self.port = port
        self.isConnected = False
        self.validateConfigMode = validateConfigMode
        self.receivedConfig = False
        self.config = None

    def onStateChanged(self, state, msg):
        if self.validateConfigMode:
            node1 = raspberry_pi
            node2 = pc
        else:
            node1 = pc
            node2 = raspberry_pi
        if state == "CONNECTING":
            print(node1, ":-- Waiting for connection...")
        elif state == "CONNECTED":
                print(node1, ":-- Connected to ", node2)
                if self.validateConfigMode:
                    print(waiting_for_config)
        elif state == "DISCONNECTED":
            print(node1, ":-- Connection lost.")
            self.isConnected = False
        elif state == "MESSAGE":
            if self.validateConfigMode:
                if is_json(msg):
                    self.receivedConfig = True
                    config = json.loads(msg)
                    print(config_received_reply)
                    print("Configuration: ", config)
                    print(tcp_start_sending_coord)
                else:
                    print(config_false_format_reply)
                    self.receivedConfig = False
            else:
                print(node1, ":-- Received data: ", msg)

    def run(self):
        if self.validateConfigMode:
            node = pc
        else:
            node = raspberry_pi
        receiver = TCPClient(self.ipaddress, self.port, stateChanged=self.onStateChanged)
        response_connection = receiver.connect()
        if response_connection:
            self.isConnected = True
        else:
            print("DEBUG:-- Connection failed, please check the ", node," is UP.")

    def receivedConfiguration(self):
        return self.receivedConfig
