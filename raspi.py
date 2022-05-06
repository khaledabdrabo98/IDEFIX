from src.receiver import Receiver
from src.camserver import RaspiCamServer

PC_IP_ADDRESS = "172.20.10.3"
PC_IP_PORT = 5005


def main():
    configReceiver = Receiver(PC_IP_ADDRESS, PC_IP_PORT, True)
    configReceiver.run()

    received = configReceiver.receivedConfiguration()
    while not received:
        received = configReceiver.receivedConfiguration()

    config = configReceiver.getConfig()
    if config:
        print("in if config")
        configReceiver.terminate()
        # start receiving coord
        coordSender = RaspiCamServer(PC_IP_ADDRESS, PC_IP_PORT, config)
        coordSender.capture()


if __name__ == '__main__':
    main()


