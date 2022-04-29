from src.client import Client

IP_ADDRESS = "172.20.10.13"
IP_PORT = 5432


if __name__ == '__main__':
    tcpclient = Client(IP_ADDRESS, IP_PORT)
    tcpclient.run()

    # get flux and pass to robots...

