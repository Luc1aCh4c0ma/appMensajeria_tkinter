# mensajeria.py

from cifrado import encriptar_mensaje, desencriptar_mensaje

class Mensajeria:
    def __init__(self):
        self.mensajes = {}  # Diccionario: clave = destinatario, valor = lista de mensajes encriptados

    def enviar_mensaje(self, remitente, destinatario, mensaje):
        mensaje_encriptado = encriptar_mensaje(mensaje)
        if destinatario not in self.mensajes:
            self.mensajes[destinatario] = []
        self.mensajes[destinatario].append((remitente, mensaje_encriptado))
        return "Mensaje enviado"

    def recibir_mensaje(self, destinatario):
        if destinatario in self.mensajes and self.mensajes[destinatario]:
            # Obtener el último mensaje y luego eliminarlo para que no se reciba de nuevo
            remitente, mensaje_encriptado = self.mensajes[destinatario].pop(0)
            mensaje_desencriptado = desencriptar_mensaje(mensaje_encriptado)
            return f"De {remitente}: {mensaje_desencriptado}"
        return "No hay mensajes"

