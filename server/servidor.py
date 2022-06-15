from cryptography.fernet import Fernet
import socket
import os
import tqdm


HOST = socket.gethostname()
PORT = 8080
BUFFER_SIZE = 4096
FORMAT = 'utf-8'
SEPARATOR = "<SEPARATOR>"


class Server:

    def __init__(self):
        self.key = None

    #Cargar la clave secreta a partir de un fichero
    def __load_key(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        
        path = os.path.dirname(file_path)
        print(path)

        complete_name = os.path.join(path,file_name)
        
        with open(complete_name,"rb") as key_file:
            self.key = key_file.read()
    
    #Desencriptar el fichero en servidor
    def __decrypt_file(self,filename):
        
        fernet = Fernet(self.key)
        with open(filename,"rb") as file:
            encrypted_data = file.read()
        
        print("Desencriptando archivo...")
        decrypted_data = fernet.decrypt(encrypted_data)
        print("Archivo desencriptado...")

        with open(filename,"wb") as file:
            file.write(decrypted_data)


    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
            socket_tcp.bind((HOST, PORT))
            socket_tcp.listen(5)
            connection, address = socket_tcp.accept()
            received = connection.recv(BUFFER_SIZE).decode()
            filename, filesize , is_encrypted = received.split(SEPARATOR)

            filename = os.path.basename(filename)
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize) , f"Receiving {filename}" , unit="B",unit_scale=True,unit_divisor=1024)
            
            with open(filename,"wb") as file:
                while True:
                    bytes_read = connection.recv(BUFFER_SIZE)
                    
                    if not bytes_read:
                        break
                    file.write(bytes_read)
                    progress.update(len(bytes_read))

            #una vez que el fichero es recibido se procede a desencriptarlo
            if is_encrypted == 'Y':
                print("Archivo viene encriptado desde cliente")
                self.__load_key()
                self.__decrypt_file(filename)
            elif is_encrypted == 'N':
                print("Archivo No encriptado desde cliente")
                
                
if __name__ == '__main__':
    server = Server()
    server.start_server()
