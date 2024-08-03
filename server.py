import threading
import socket
#CONFIGURACION DE DIRECCIONES
host = '127.0.0.1' #localhost
port = 5000
#SE DEFINE EL TIPO DE CONEXION Y EL PROTOCOLO
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#LE PASO LA CONFIGURACION AL SERVER & INICIAMOS
server.bind((host,port))
server.listen(10)#pone en modo de escucha 

#SE CREA LA LISTAS DE CLIENTES & USUARIOS
clientes = []
apodos = []

#SE DEFINE LOS METODOS DE FUNCIONES DEL SERVIDOR
#SE TRANSMITE LOS MENSAJES A TODOS
def difusion(mensaje):
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except:
            # Si no se puede enviar el mensaje, cerramos la conexión del cliente
            cliente.close()
            clientes.remove(cliente)


#SE MANEJA AL CLIENTE SI ES QUE EL CLIENTE YA NO ESTA
def manejar(cliente):
    while True:
        try:
            mensaje = cliente.recv(2048)
            if not mensaje:
                # Si no se recibe mensaje, el cliente se desconectó
                break
            difusion(mensaje)
        except:
            # Manejar excepciones si ocurre un error
            break

    # Cuando el cliente se desconecta
    indice = clientes.index(cliente)
    clientes.remove(cliente)
    apodo = apodos[indice]
    apodos.remove(apodo)
    cliente.close()
    difusion(f"{apodo} Abandonó el chat...".encode('UTF-8'))
    print(f"{apodo} ha abandonado la sala.")

#RECIBIR CONEXIONES
def recibir():
    while True:
        #ACEPTAMOS LA CONEXION(TODAS)
        cliente, direccion = server.accept()
        print(f"Se conecto la direccion {str(direccion)}")  

        #SOLICITAMOS EL APODO AL CLIENTE
        cliente.send('APODO'.encode('UTF-8'))  
        apodo = cliente.recv(2048).decode('UTF-8')
        apodos.append(apodo)
        clientes.append(cliente)

        #AVISAMOS DE LA CONEXION
        print(f'El Apodo del cliente es {apodo}!')
        difusion(f'{apodo} Se unio al Chat!'.encode('UTF-8'))
        cliente.send('Conectado al Servidor!'.encode('UTF-8'))

        #CONFIGURACION & INICIALIZA EL HILO PARA PERMITIR LA EJECUCION
        #DE VARIAS PARTES DEL PROGRAMA AL MISMO TIEMPO(FUNCION MANEJAR)
        hilo = threading.Thread(target=manejar, args=(cliente,))
        hilo.start()


print("""----*------------------------*-------------------*
             El Servidor esta en Línea...
*--------------*-------------------*-------------*
      """)
recibir() #SE LLAMA LA FUNC RECIBIR PARA EMPEZAR EL SERVIDOR

