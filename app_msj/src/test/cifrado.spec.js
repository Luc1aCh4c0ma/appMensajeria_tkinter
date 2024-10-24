// Importamos las funciones de cifrado
const { encriptar_mensaje, desencriptar_mensaje } = require('./cifrado');

// Grupo de pruebas para las funciones de cifrado y desencriptado
describe('Funciones de cifrado y desencriptado', () => {

    // Test para la función encriptar_mensaje
    it('encriptar_mensaje debería invertir el mensaje', () => {
        const mensaje = "Hola Mundo";
        const mensaje_encriptado = encriptar_mensaje(mensaje);

        // Verificamos que el resultado sea el mensaje invertido
        expect(mensaje_encriptado).to.equal("odnuM aloH");
    });

    // Test para la función desencriptar_mensaje
    it('desencriptar_mensaje debería revertir el mensaje encriptado', () => {
        const mensaje_encriptado = "odnuM aloH";
        const mensaje_desencriptado = desencriptar_mensaje(mensaje_encriptado);

        // Verificamos que el resultado sea el mensaje desencriptado correctamente
        expect(mensaje_desencriptado).to.equal("Hola Mundo");
    });
});
