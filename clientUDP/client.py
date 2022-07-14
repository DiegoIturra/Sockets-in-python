from cryptography.fernet import Fernet
import socket
import os
import tqdm


HOST = socket.gethostname()
PORT = 8080
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
SEPARATOR = "<SEPARATOR>"

class Client:

    def __init__(self):
        pass

    #Generar clave
    def __generate_key(self):
        key = Fernet.generate_key()
        return key


    #Guardar clave en un fichero
    def save_key_into_a_file(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = self.__generate_key()

        with open(complete_name,"wb") as key_file:
            key_file.write(key)
    

    def send_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
            message = b'Hola mundo'

            sent = socket_udp.sendto(message, (HOST,PORT))
            data,server = socket_udp.recvfrom(BUFFER_SIZE)
            print(f'mensaje recibido desde servidor: {str(data)}')

        

if __name__ == '__main__':
    client = Client()
    client.send_file()