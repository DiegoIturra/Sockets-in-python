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
        self.__save_key_into_a_file()


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


    def __generate_key(self):
        key = Fernet.generate_key()
        return key

    def __save_key_into_a_file(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = self.__generate_key()

        with open(complete_name,"wb") as key_file:
            key_file.write(key)


    def __load_key(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = ""
        with open(complete_name,"rb") as key_file:
            key = key_file.read()
        return key


    def __decrypt_file(self,filename):
        #obtener la clave
        key = self.__load_key()

        fernet = Fernet(key)
        with open(filename,"rb") as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(filename,"wb") as file:
            file.write(decrypted_data)


    def __convert_int_to_bytes(self,filesize):
        str_filesize = str(filesize)
        return str_filesize.encode()


    def __get_file_size(self,filename):
        return os.path.getsize(filename)


    def __exist_file(self,filename):
        exist_file = True
        try:
            filesize = self.__get_file_size(filename) #get the file size in bytes
        except FileNotFoundError as error:
            exist_file = False
        return exist_file
    
    
    def __send_file(self,filename,address):

        filesize = self.__get_file_size(filename)
        progress = tqdm.tqdm(range(filesize) , f"Receiving {filename}" , unit="B",unit_scale=True,unit_divisor=1024)
        
        with open(filename,"rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)
                
                if not bytes_read:
                    break

                self.socket.sendto(bytes_read, address)
                time.sleep(0.02)

                progress.update(len(bytes_read))
    

    def handle_request(self):
        while True:
            data , address = self.socket.recvfrom(BUFFER_SIZE)
            
            if data:
                print(f"nombre del archivo: {data.decode('utf-8')}")
            
                filename = data.decode('utf-8')
                
                if self.__exist_file(filename):
                    filesize = self.__get_file_size(filename)
                    filesize = self.__convert_int_to_bytes(filesize)

                    self.socket.sendto(filesize, address) #envia tamaño del fichero de forma anticipada

                    self.encrypt_file(filename)
                    self.__send_file(filename,address)  
                    self.__decrypt_file(filename)    
                else:
                    print(f"Archivo solicitado {filename} no existe")
                    self.socket.sendto(b"", address)
                break


if __name__ == '__main__':
    server = ServerUDP()
    server.handle_request()