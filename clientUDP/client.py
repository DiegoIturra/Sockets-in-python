from cryptography.fernet import Fernet
import socket
import os
import tqdm
import select


HOST = socket.gethostname()
PORT = 8080
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
SEPARATOR = "<SEPARATOR>"

class Client:

    def __init__(self):
        self.timeout = 3
    

    def make_request(self,filename):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
            
            socket_udp.sendto(filename,(HOST,PORT))
            
            with open(filename,"wb") as file:
                while True:
                    ready = select.select([socket_udp], [], [], self.timeout)

                    if ready[0]:
                        bytes_read ,server = socket_udp.recvfrom(BUFFER_SIZE)
                        file.write(bytes_read)
                    else:
                        print(f"Archivo {filename} recibido")
                        break
            
        
if __name__ == '__main__':
    client = Client()
    client.make_request(b"libro.pdf")