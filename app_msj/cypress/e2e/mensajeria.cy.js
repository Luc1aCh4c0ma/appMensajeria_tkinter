describe('Flujo de Mensajería', () => {
    beforeEach(() => {
        cy.visit('http://localhost:8000');  // URL de tu aplicación Tkinter servida en un servidor
    });

    it('Debería enviar un mensaje', () => {
        cy.get('input[name="remitente"]').type('Juan');
        cy.get('input[name="destinatario"]').type('Ana');
        cy.get('input[name="mensaje"]').type('Hola, ¿cómo estás?');
        cy.get('button').contains('Enviar Mensaje').click();

        cy.get('textarea').should('contain', '[Enviado] Juan a Ana: Hola, ¿cómo estás?');
    });

    it('Debería recibir un mensaje', () => {
        cy.get('input[name="destinatario"]').type('Ana');
        cy.get('input[name="respuesta"]').type('Estoy bien, gracias.');
        cy.get('button').contains('Recibir Mensaje').click();

        cy.get('textarea').should('contain', '[Recibido] De Ana: Estoy bien, gracias.');
    });
});
