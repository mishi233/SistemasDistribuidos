from xmlrpc.server import SimpleXMLRPCServer
import threading

usuarios = []

class Mensajes:
    def __init__(self, usuario1, usuario2):
        self.usuario1 = usuario1
        self.usuario2 = usuario2
        self.mensajes = []

    def registrarMensaje(self, remitente, mensaje):
        self.mensajes.append([remitente, mensaje])

    def clientesParticipantes(self, cliente):
        if cliente == self.usuario1:
            return self.usuario2
        elif cliente == self.usuario2:
            return self.usuario1
        else:
            []
        
mensajes = []

def registrar(usuario):
    usuarios.append(usuario)
    return "Registrado"
    
def usuariosRegistrados():
    return usuarios

def mandarMensaje(remitente, destinatario, mensaje):
    for mensajesListados in mensajes:
        if mensajesListados.clientesParticipantes(remitente) != [] and mensajesListados.clientesParticipantes(destinatario) != []:
            mensajesListados.registrarMensaje(remitente, mensaje)
            return "Enviado"
    nuevoMensaje = Mensajes(remitente, destinatario)
    nuevoMensaje.registrarMensaje(remitente, mensaje)
    mensajes.append(nuevoMensaje)
    return "Enviado"

def conservacionesActivas(remitente):
    listaChatsActivos = []
    for mensaje in mensajes:
        participanteChat = mensaje.clientesParticipantes(remitente)
        if participanteChat != []:
            listaChatsActivos.append(participanteChat)
    if listaChatsActivos == []:
        return 0
    else:
        return listaChatsActivos
    
def recibirMensajes(remitente, destinatario):
    for mensaje in mensajes:
        if mensaje.clientesParticipantes(remitente) != [] and mensaje.clientesParticipantes(destinatario) != []:
            return mensaje.mensajes
        else: 
            return None

# Configurar el servidor XML-RPC
server = SimpleXMLRPCServer(("127.0.0.1", 12345))
print("Servidor XML-RPC escuchando en 127.0.0.1:12345")

# Registrar las funciones para que estén disponibles remotamente
server.register_function(registrar, "registrar")
server.register_function(usuariosRegistrados, "usuariosRegistrados")
server.register_function(mandarMensaje, "mandarMensaje")
server.register_function(conservacionesActivas, "conservacionesActivas")
server.register_function(recibirMensajes, "recibirMensajes")

# Iniciar el servidor en un hilo separado
def serve():
    server.serve_forever()

server_thread = threading.Thread(target=serve)
server_thread.start()
    