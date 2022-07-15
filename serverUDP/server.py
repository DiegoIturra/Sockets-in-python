from cryptography.fernet import Fernet
import socket
import time
import os
import tqdm

HOST = socket.gethostname()
PORT = 8080
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
SEPARATOR = "<SEPARATOR>"


class ServerUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        self.socket.bind((HOST,PORT))


    def encrypt_file(self,filename):
        key = self.__load_key()
        fernet = Fernet(key)

        encrypted_data = ""
        encrypted_file = None

        try:
            with open(filename,"rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)

            with open(filename,"wb") as file:
                file.write(encrypted_data)
                encrypted_file = file
        except FileNotFoundError as error:
           print("Fichero a encriptar no existe")


    def decrypt_file(self,filename):
        #obtengo la clave
        key = self.__load_key()

        fernet = Fernet(key)
        with open(filename,"rb") as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(filename,"wb") as file:
            file.write(decrypted_data)

    
    def __exist_file(self,filename):
        exist_file = True
        try:
            filesize = os.path.getsize(filename) #get the file size in bytes
        except FileNotFoundError as error:
            exist_file = False
        return exist_file
    
    
    def __send_file(self,filename,address):
        with open(filename,"rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)
                
                if not bytes_read:
                    break

                self.socket.sendto(bytes_read, address)
                time.sleep(0.02)
    
    def handle_request(self):
        while True:
            data , address = self.socket.recvfrom(BUFFER_SIZE)

            if data:
                print(f"nombre del archivo: {data.decode('utf-8')}")
            
                filename = data.decode('utf-8')
                
                if self.__exist_file(filename):
                    self.__send_file(filename,address)      
                else:
                    print(f"Archivo solicitado {str(filename)} no existe")
                break

if __name__ == '__main__':
    server = ServerUDP()
    server.handle_request()