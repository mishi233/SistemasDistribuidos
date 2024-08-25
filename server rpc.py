from xmlrpc.server import SimpleXMLRPCServer
import threading

mensajes = []

def mandarMensaje(usuario, mensaje):
    mensajes.append(f"{usuario}: {mensaje}")
    return "Éxito"

def recibirMensajes():
    print(mensajes)
    return mensajes

# Configurar el servidor XML-RPC
server = SimpleXMLRPCServer(("127.0.0.1", 12345))
print("Servidor XML-RPC escuchando en 127.0.0.1:12345")

# Registrar las funciones para que estén disponibles remotamente
server.register_function(mandarMensaje, "mandarMensaje")
server.register_function(recibirMensajes, "recibirMensajes")

# Iniciar el servidor en un hilo separado
def serve():
    server.serve_forever()

server_thread = threading.Thread(target=serve)
server_thread.start()
    