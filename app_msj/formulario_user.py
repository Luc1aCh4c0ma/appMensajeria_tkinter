import tkinter as tk
from tkinter import messagebox
import sqlite3

class UsuarioForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Usuario")
        self.root.geometry("350x300")
        self.root.configure(bg="#2c3e50")  # Fondo más oscuro

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        
        titulo = tk.Label(root, text="Agregar Nuevo Usuario", font=("Helvetica", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # Campos de formulario con labels estilizados
        self.crear_label_y_entry("Nombre:", 1)
        self.crear_label_y_entry("Apellido:", 2)
        self.crear_label_y_entry("Edad:", 3)
        self.crear_label_y_entry("Teléfono:", 4)

        # Botón para guardar con estilo moderno
        self.boton_guardar = tk.Button(root, text="Guardar", command=self.guardar_usuario, 
                                       bg="#1abc9c", fg="white", activebackground="#16a085", 
                                       font=("Helvetica", 10, "bold"), bd=0, padx=10, pady=5, relief="ridge")
        self.boton_guardar.grid(row=5, column=0, columnspan=2, pady=20)

    def crear_label_y_entry(self, texto, fila):
        tk.Label(self.root, text=texto, fg="#ecf0f1", bg="#2c3e50", font=("Helvetica", 10, "bold")).grid(row=fila, column=0, padx=20, pady=5, sticky="e")
        entry = tk.Entry(self.root, font=("Helvetica", 10), bd=2, relief="groove", highlightthickness=1, 
                         highlightbackground="#34495e", highlightcolor="#1abc9c")
        entry.grid(row=fila, column=1, padx=10, pady=5, sticky="w")

        if texto == "Nombre:":
            self.entry_nombre = entry
        elif texto == "Apellido:":
            self.entry_apellido = entry
        elif texto == "Edad:":
            self.entry_edad = entry
        elif texto == "Teléfono:":
            self.entry_telefono = entry

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        edad = self.entry_edad.get()
        telefono = self.entry_telefono.get()

        # Validaciones
        if not nombre or not apellido or not edad or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not edad.isdigit() or int(edad) <= 0:
            messagebox.showerror("Error", "El campo 'Edad' debe ser un número positivo")
            return

        if not telefono.isdigit() or len(telefono) != 10 or int(telefono) <= 0:
            messagebox.showerror("Error", "El campo 'Teléfono' debe contener exactamente 10 dígitos y no debe ser negativo")
            return

        # Si pasa todas las validaciones, se guarda en la base de datos
        try:
            conn = sqlite3.connect('mensajeria.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nombre, apellido, edad, telefono)
                VALUES (?, ?, ?, ?)
            ''', (nombre, apellido, edad, telefono))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.root.destroy()  # Cerrar la ventana después de guardar
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

def abrir_formulario_usuario():
    ventana_formulario = tk.Toplevel()
    UsuarioForm(ventana_formulario)
