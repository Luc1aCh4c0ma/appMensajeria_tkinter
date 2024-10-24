
# test_cifrado.py
import unittest
from cifrado import encriptar_mensaje, desencriptar_mensaje

class TestCifrado(unittest.TestCase):

    def test_encriptar_mensaje(self):
        mensaje = "Hola"
        resultado = encriptar_mensaje(mensaje)
        self.assertEqual(resultado, "aloH", "El mensaje no se encriptó correctamente")

    def test_desencriptar_mensaje(self):
        mensaje = "aloH"
        resultado = desencriptar_mensaje(mensaje)
        self.assertEqual(resultado, "Hola", "El mensaje no se desencriptó correctamente")

    def test_encriptar_mensaje_vacio(self):
        mensaje = ""
        resultado = encriptar_mensaje(mensaje)
        self.assertEqual(resultado, "", "El mensaje vacío no se encriptó correctamente")

    def test_desencriptar_mensaje_vacio(self):
        mensaje = ""
        resultado = desencriptar_mensaje(mensaje)
        self.assertEqual(resultado, "", "El mensaje vacío no se desencriptó correctamente")

if __name__ == '__main__':
    unittest.main()

