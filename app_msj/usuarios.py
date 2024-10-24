# usuarios.py

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class GestionUsuarios(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Gestión de Usuarios")
        self.geometry("900x400")
        self.configure(bg="#2c3e50")

        self.setup_ui()
        self.mostrar_usuarios()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        

    def setup_ui(self):
        
        # Configuración de la tabla de usuarios
        self.treeview = ttk.Treeview(self, columns=("nombre", "apellido", "edad", "telefono"), show="headings", height=8)
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("apellido", text="Apellido")
        self.treeview.heading("edad", text="Edad")
        self.treeview.heading("telefono", text="Teléfono")
        self.treeview.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky="ns")

        # Botones para Editar y Eliminar
        boton_editar = tk.Button(self, text="Editar Usuario", command=self.editar_usuario, bg="#3498db", fg="white", bd=0, padx=10, pady=5)
        boton_editar.grid(row=1, column=0, padx=10, pady=5)

        boton_eliminar = tk.Button(self, text="Eliminar Usuario", command=self.eliminar_usuario, bg="#e74c3c", fg="white", bd=0, padx=10, pady=5)
        boton_eliminar.grid(row=1, column=1, padx=10, pady=5)
        

    def mostrar_usuarios(self):
        # Limpiar el treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Cargar los datos de la base de datos
        conn = sqlite3.connect('mensajeria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, edad, telefono FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        # Insertar datos en el treeview
        for usuario in usuarios:
            self.treeview.insert("", tk.END, values=usuario)

    def editar_usuario(self):
        # Obtener el usuario seleccionado
        selected = self.treeview.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para editar.")
            return

        # Obtener los datos del usuario seleccionado
        valores = self.treeview.item(selected[0], "values")

        # Crear una ventana para editar los datos del usuario
        self.ventana_editar = tk.Toplevel(self)
        self.ventana_editar.title("Editar Usuario")
        self.ventana_editar.geometry("300x300")
        self.ventana_editar.configure(bg="#34495e")

        tk.Label(self.ventana_editar, text="Nombre", fg="white", bg="#34495e").pack(pady=5)
        self.entry_nombre = tk.Entry(self.ventana_editar)
        self.entry_nombre.pack(pady=5)
        self.entry_nombre.insert(0, valores[0])

        tk.Label(self.ventana_editar, text="Apellido", fg="white", bg="#34495e").pack(pady=5)
        self.entry_apellido = tk.Entry(self.ventana_editar)
        self.entry_apellido.pack(pady=5)
        self.entry_apellido.insert(0, valores[1])

        tk.Label(self.ventana_editar, text="Edad", fg="white", bg="#34495e").pack(pady=5)
        self.entry_edad = tk.Entry(self.ventana_editar)
        self.entry_edad.pack(pady=5)
        self.entry_edad.insert(0, valores[2])

        tk.Label(self.ventana_editar, text="Teléfono", fg="white", bg="#34495e").pack(pady=5)
        self.entry_telefono = tk.Entry(self.ventana_editar)
        self.entry_telefono.pack(pady=5)
        self.entry_telefono.insert(0, valores[3])

        boton_guardar = tk.Button(self.ventana_editar, text="Guardar Cambios", command=lambda: self.guardar_cambios_usuario(selected[0]), bg="#1abc9c", fg="white", padx=10, pady=5)
        boton_guardar.pack(pady=20)

    def guardar_cambios_usuario(self, item_id):
        # Obtener los nuevos valores
        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_apellido = self.entry_apellido.get().strip()
        nueva_edad = self.entry_edad.get().strip()
        nuevo_telefono = self.entry_telefono.get().strip()

        # Validar que los campos no estén vacíos
        if not nuevo_nombre or not nuevo_apellido or not nueva_edad or not nuevo_telefono:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Actualizar los datos en la base de datos
        conn = sqlite3.connect('mensajeria.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre = ?, apellido = ?, edad = ?, telefono = ? 
            WHERE telefono = ?
        """, (nuevo_nombre, nuevo_apellido, nueva_edad, nuevo_telefono, self.treeview.item(item_id, "values")[3]))
        conn.commit()
        conn.close()

        # Actualizar el treeview
        self.treeview.item(item_id, values=(nuevo_nombre, nuevo_apellido, nueva_edad, nuevo_telefono))
        self.ventana_editar.destroy()

    def eliminar_usuario(self):
        # Obtener el usuario seleccionado
        selected = self.treeview.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
            return

        # Obtener el teléfono del usuario para eliminar
        telefono = self.treeview.item(selected[0], "values")[3]

        # Eliminar el usuario de la base de datos
        conn = sqlite3.connect('mensajeria.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE telefono = ?", (telefono,))
        conn.commit()
        conn.close()

        # Eliminar del treeview
        self.treeview.delete(selected[0])
        messagebox.showinfo("Información", "Usuario eliminado correctamente.")
