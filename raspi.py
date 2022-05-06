from src.receiver import Receiver
from src.camserver import RaspiCamServer

PC_IP_ADDRESS = "172.20.10.3"
PC_IP_PORT = 5005
config_false_format_reply = "Bad configuration format, please retry"


def main():
    configReceiver = Receiver(PC_IP_ADDRESS, PC_IP_PORT, True)
    configReceiver.run()

    received = configReceiver.receivedConfiguration()
    while not received:
        received = configReceiver.receivedConfiguration()


    if configReceiver.receivedWrongConfig():
        print(config_false_format_reply)
        configReceiver.terminate()
    else:
        config = configReceiver.getConfig()
        if config is not None:
            # configReceiver.terminate()
            # open camera and start receiving coord
            coordSender = RaspiCamServer(PC_IP_ADDRESS, PC_IP_PORT, config)
            coordSender.capture()


if __name__ == '__main__':
    main()


