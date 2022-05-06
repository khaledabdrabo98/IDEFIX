from src.com.receiver import Receiver
from src.camserver import RaspiCamServer

PC_IP_ADDRESS = "172.20.10.3"
PC_IP_PORT = 5432


def main():
    configReceiver = Receiver(PC_IP_ADDRESS, PC_IP_PORT, True)
    configReceiver.run()

    while !configReceiver.receivedConfiguration():
        None

    coordSender = RaspiCamServer(PC_IP_ADDRESS, PC_IP_PORT)
    coordSender.capture()


if __name__ == '__main__':
    main()


