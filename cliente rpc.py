import xmlrpc.client

# Conectarse al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://127.0.0.1:12345/")
nombre = input("Bienvenido, indique su nombre: ")

opcion = 0
while opcion != 3:
    opcion = int(input("Indique una opcion: \n1 - Mandar Mensaje\n2 - Recibir Mensajes\n3 - Desconectar\n"))

    if opcion == 1:
        mensaje = input("Indique el mensaje:")
        server.mandarMensaje(nombre, mensaje)
    elif opcion == 2:
        print(server.recibirMensajes())
    elif opcion == 3:
        continue
    else:
        print("Opcion no válida ")
