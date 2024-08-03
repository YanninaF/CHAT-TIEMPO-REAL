import socket
import threading
#EL CLIENTE INGRESA UN APODO
print("""----*---------------*--------*-------------------*
             Bienvenido a la sala de chat...!
---------------*-------------------*--------------
      """)


apodo = input("Ingresa un apodo: ")

#CONECTAMOS AL SERVIDOR
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5000))

# Definimos los metodos para los clientes
# Funcion checkeadora de comandos 

#FUNC. RECIBIR MENSAJE
def recibir():
    while True:
        try:
            mensaje = cliente.recv(2048).decode('UTF-8')#RECIBIMOS DEL SERVIDOR
            if mensaje == 'APODO':
                cliente.send(apodo.encode('UTF-8'))
            else:
                print(mensaje)
        except:
            print("Se ha producido un Error")
            cliente.close()
            break

#FUNCION ESCRIBIR MENSAJE
def escribir():
    while True:
        mensaje = f'{apodo}: {input("")}'
        cliente.send(mensaje.encode('UTF-8'))

#CREAMOS LOS HILOS CORRESPONDIENTES PARA LAS FUNCIONES
recibir_hilo = threading.Thread(target=recibir)
recibir_hilo.start()

escribir_hilo = threading.Thread(target=escribir)
escribir_hilo.start()
