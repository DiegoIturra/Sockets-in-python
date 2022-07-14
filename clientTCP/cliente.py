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
    
    #Guardar clave en un fichero
    def save_key_into_a_file(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = self.__generate_key()

        with open(complete_name,"wb") as key_file:
            key_file.write(key)
    

    #Generar clave
    def __generate_key(self):
        key = Fernet.generate_key()
        return key


    #Cargar clave antes creada y guardada en un fichero
    def __load_key(self):
        file_name = "key_file.key"
        file_path = os.getcwd()
        path = os.path.dirname(file_path)
        complete_name = os.path.join(path,file_name)

        key = ""
        with open(complete_name,"rb") as key_file:
            key = key_file.read()
        return key

    #Encriptamos el fichero y lo guardamos en la misma
    #referencia
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


    #Desencriptar el fichero en cliente
    def decrypt_file(self,filename):
        #obtengo la clave
        key = self.__load_key()
        
        fernet = Fernet(key)
        with open(filename,"rb") as file:
            encrypted_data = file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(filename,"wb") as file:
            file.write(decrypted_data)


    #Enviamos archivo asumiendo que este está en 
    #el mismo directorio que el codigo actual
    def send_file(self, filename, is_encrypted):
        exist_file = True

        try:
            filesize = os.path.getsize(filename) #get the file size in bytes
        except FileNotFoundError as error:
            exist_file = False
        
        if exist_file:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
                try:
                    socket_tcp.connect((HOST, PORT))
                    socket_tcp.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{is_encrypted}".encode())

                    progress = tqdm.tqdm(range(filesize) , f"Sending {filename}" , unit="B",unit_scale=True,unit_divisor=1024)
                    with open(filename,"rb") as file:
                        
                        while True:
                            bytes_read = file.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            socket_tcp.sendall(bytes_read)
                            progress.update(len(bytes_read))
                except ConnectionRefusedError as error:
                    print("Error al conectarse al servidor, servidor no encontrado")
        
        else:
            print("No se puede enviar archivo inexistente")


if __name__ == '__main__':
    client = Client()
    client.save_key_into_a_file() #Se guarda la clave en un fichero
    
    is_encrypted = input(str("Desea encriptar archivo a enviar? [Y/N][y/n]: "))

    while is_encrypted != 'Y' and is_encrypted != 'y' and is_encrypted != 'n' and is_encrypted != 'N':
        is_encrypted = input(str("Ingrese respuesta valida: [Y/N][y/n]: "))

    if is_encrypted == 'y' or is_encrypted == 'Y':
        client.encrypt_file("lab1.pdf")
        client.send_file("lab1.pdf",'Y')
        client.decrypt_file("lab1.pdf") #desencriptar archivo de vuelta solo para evitar problemas con claves
    elif is_encrypted == 'n' or is_encrypted == 'N':
        client.send_file("lab1.pdf",'N')


    
