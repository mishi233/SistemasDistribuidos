import xmlrpc.client
import os

# Conectarse al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://127.0.0.1:12345/")

#Manejo de terminal
def clsTerminal():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix o Linux
    else:
        os.system('clear')

#Inicio de usuario
remitente = input("Bienvenido, indique su usuario: ")
usuarios = server.usuariosRegistrados()
if not (remitente in usuarios):
    server.registrar(remitente)

clsTerminal()

opcion = 0
while opcion != 3:
    opcion = int(input("Indique una opcion: \n1 - Mandar Mensaje\n2 - Ver Mensajes\n3 - Desconectar\n"))

    if opcion == 1:
        #Mandar Mensaje
        usuariosConRemitente = server.usuariosRegistrados()
        usuarios = []
        for user in usuariosConRemitente:
            if user != remitente:
                usuarios.append(user)
        print("Estos son los usuarios activos:")
        for usuario in usuarios:
            print(usuario)
        destinatario = input("¿A quien desea mandarle un mensaje?")
        if (destinatario in usuarios):
            mensaje = input("Indique el mensaje:")
            server.mandarMensaje(remitente, destinatario, mensaje)
            clsTerminal()
            print("Mensaje enviado con éxito")
        else:
            clsTerminal()
            print("El usuario no es valido")

    elif opcion == 2:
        #Ver mensajes
        listaChats = server.conservacionesActivas(remitente)
        if listaChats == 0:
            clsTerminal()
            print("No hay conversaciones")
        else:
            print("Conversaciones activas:")
            for chat in listaChats:
                print(chat)
            chatSeleccionado = input("Seleccione con cual de los siguientes usuarios desea interactuar:")
            if chatSeleccionado in listaChats:
                clsTerminal()
                print("Conversación: ")
                mensajes = server.recibirMensajes(remitente, chatSeleccionado)
                for mensaje in mensajes:
                    print(mensaje[0], "dice: " , mensaje[1])
                print()
            else:
                clsTerminal()
                print("El usuario no se encuentra")
    elif opcion == 3:
        continue
    else:
        clsTerminal()
        print("Opcion no válida ")