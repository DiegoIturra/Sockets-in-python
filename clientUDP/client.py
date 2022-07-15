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

    
    def __decrypt_file(self,filename):
        #obtengo la clave
        key = self.__load_key()

        fernet = Fernet(key)
        with open(filename,"rb") as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(filename,"wb") as file:
            file.write(decrypted_data)
            
    
    def __load_key(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = ""
        with open(complete_name,"rb") as key_file:
            key = key_file.read()
        return key
    

    def make_request(self,filename):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
            
            socket_udp.sendto(filename,(HOST,PORT)) #Enviamos el nombre del archivo
            
            filename = filename.decode('utf-8')

            filesize , _ = socket_udp.recvfrom(BUFFER_SIZE) #recibimos el tamaño del archivo
            if filesize:
                filesize = int(filesize.decode('utf-8'))

                progress = tqdm.tqdm(range(filesize) , f"Receiving {filename}" , unit="B",unit_scale=True,unit_divisor=1024)
                with open(filename,"wb") as file:
                    while True:
                        ready = select.select([socket_udp], [], [], self.timeout)

                        if ready[0]:
                            bytes_read ,server = socket_udp.recvfrom(BUFFER_SIZE)
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        else:
                            print(f"Archivo {filename} recibido")
                            self.__decrypt_file(filename)
                            break
            else:
                print(f"Servidor no puede enviar archivo inexistente {filename}")
                

          
if __name__ == '__main__':
    client = Client()
    client.make_request(b"libro.pdf")