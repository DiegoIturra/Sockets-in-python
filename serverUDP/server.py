from cryptography.fernet import Fernet
import socket
import os
import tqdm

HOST = socket.gethostname()
PORT = 8080
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
SEPARATOR = "<SEPARATOR>"


class ServerUDP:

    def __init__(self):
        pass

    
    def start_server(self):
        with socket.socket(socket.AF_INET , socket.SOCK_DGRAM) as socket_udp:
            socket_udp.bind((HOST,PORT))

            while True:
                data , address = socket_udp.recvfrom(BUFFER_SIZE)

                if data:
                    print(f'mensaje recibido: {str(data)}')
                    sent = socket_udp.sendto(data, address)
                    break


if __name__ == '__main__':
    server = ServerUDP()
    server.start_server()