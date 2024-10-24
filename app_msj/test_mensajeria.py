# test_mensajeria.py
import pytest
from mensajeria import Mensajeria

@pytest.fixture
def sistema_mensajeria():
    return Mensajeria()

def test_enviar_y_recibir_mensaje(sistema_mensajeria):
    remitente = "Alice"
    destinatario = "Bob"
    mensaje = "Hola Bob!"
    
    # Enviar mensaje
    sistema_mensajeria.enviar_mensaje(remitente, destinatario, mensaje)
    
    # Recibir mensaje
    resultado = sistema_mensajeria.recibir_mensaje(destinatario)
    assert resultado == "De Alice: Hola Bob!", "El flujo de conversación no funcionó correctamente"

def test_recibir_mensaje_sin_mensajes(sistema_mensajeria):
    destinatario = "Bob"
    resultado = sistema_mensajeria.recibir_mensaje(destinatario)
    assert resultado == "No hay mensajes", "El sistema debería indicar que no hay mensajes"

def test_enviar_mensaje_varios_remitentes(sistema_mensajeria):
    sistema_mensajeria.enviar_mensaje("Alice", "Bob", "Hola")
    sistema_mensajeria.enviar_mensaje("Charlie", "Bob", "Adiós")

    # Recibir mensajes en orden
    assert sistema_mensajeria.recibir_mensaje("Bob") == "De Alice: Hola", "No se recibió el mensaje correcto"
    assert sistema_mensajeria.recibir_mensaje("Bob") == "De Charlie: Adiós", "No se recibió el mensaje correcto"
