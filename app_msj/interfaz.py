import sqlite3
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from mensajeria import Mensajeria
from formulario_user import abrir_formulario_usuario
from tkinter import messagebox
from usuarios import GestionUsuarios  



class MensajeriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Mensajería Instantánea")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")
        self.mensajeria = Mensajeria()

        # Configurar la expansión responsiva de las columnas
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(6, weight=1)  # Para que el área de texto crezca

        # Fuente personalizada
        fuente_titulo = font.Font(family="Arial", size=14, weight="bold")
        fuente_labels = font.Font(family="Arial", size=11)

        self.cargar_logo()
        self.usuarios = self.cargar_usuarios()


        self.remitente_var = tk.StringVar(root)

        # Título
        titulo = tk.Label(root, text="Sistema de Mensajería", font=fuente_titulo, fg="#ecf0f1", bg="#2c3e50")
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

       

        # Sección de remitente
        self.label_remitente = tk.Label(root, text="Remitente:", font=fuente_labels, fg="#ecf0f1", bg="#2c3e50")
        self.label_remitente.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        if self.usuarios:
            self.remitente_var.set(self.usuarios[0])
            self.entry_remitente = tk.OptionMenu(root, self.remitente_var, *self.usuarios)
            self.entry_remitente.config(bg="#34495e", fg="white", activebackground="#1abc9c", bd=0, relief="flat")
            self.entry_remitente.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
        else:
            self.remitente_var.set('')
            messagebox.showwarning("Advertencia", "No hay usuarios disponibles para seleccionar.")
            self.entry_remitente = tk.Label(root, text="No hay usuarios disponibles", bg="#2c3e50", fg="red")
            self.entry_remitente.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # Sección de destinatario
        self.label_destinatario = tk.Label(root, text="Destinatario:", font=fuente_labels, fg="#ecf0f1", bg="#2c3e50")
        self.label_destinatario.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.destinatario_var = tk.StringVar()
        if self.usuarios:
            self.destinatario_var.set(self.usuarios[0])
            self.entry_destinatario = tk.OptionMenu(root, self.destinatario_var, *self.usuarios)
            self.entry_destinatario.config(bg="#34495e", fg="white", activebackground="#1abc9c", bd=0, relief="flat")
            self.entry_destinatario.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
        else:
            self.destinatario_var.set('')
            self.entry_destinatario = tk.Label(root, text="No hay usuarios disponibles", bg="#2c3e50", fg="red")
            self.entry_destinatario.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # Sección de mensaje a enviar
        self.label_mensaje = tk.Label(root, text="Mensaje a enviar:", font=fuente_labels, fg="#ecf0f1", bg="#2c3e50")
        self.label_mensaje.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_mensaje = tk.Entry(root, width=40, font=fuente_labels, relief="flat", bg="#ecf0f1")
        self.entry_mensaje.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # Sección de mensaje recibido
        self.label_respuesta = tk.Label(root, text="Mensaje recibido:", font=fuente_labels, fg="#ecf0f1", bg="#2c3e50")
        self.label_respuesta.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_respuesta = tk.Entry(root, width=40, font=fuente_labels, relief="flat", bg="#ecf0f1")
        self.entry_respuesta.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # Botones
        self.boton_enviar = tk.Button(root, text="Enviar Mensaje", command=self.enviar_mensaje, bg="#3498db", fg="white", font=fuente_labels, bd=0, padx=10, pady=5, activebackground="#2980b9")
        self.boton_enviar.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)

        self.boton_recibir = tk.Button(root, text="Recibir Mensaje", command=self.recibir_mensaje, bg="#2ecc71", fg="white", font=fuente_labels, bd=0, padx=10, pady=5, activebackground="#27ae60")
        self.boton_recibir.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

        # Área de texto
        self.text_area = tk.Text(root, height=10, width=60, state=tk.DISABLED, bg="#ecf0f1", font=("Arial", 10), fg="#333333", relief="flat", wrap=tk.WORD)
        self.text_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N+tk.S+tk.W+tk.E)

        # Barra de desplazamiento
        self.scrollbar = tk.Scrollbar(root, command=self.text_area.yview)
        self.scrollbar.grid(row=6, column=2, sticky='nsew')
        self.text_area['yscrollcommand'] = self.scrollbar.set

        self.boton_limpiar = tk.Button(root, text="Vaciar Chat", command=self.vaciar_chat, bg="#e74c3c", fg="white", font=fuente_labels, bd=0, padx=10, pady=5, activebackground="#c0392b")
        self.boton_limpiar.grid(row=7, column=0, columnspan=3, pady=10)

        self.boton_usuarios = tk.Button(self.root, text="Gestionar Usuarios", command=self.abrir_gestion_usuarios)
        self.boton_usuarios.grid(row=7, column=0, padx=2, pady=10)

    def cargar_usuarios(self):
        conn = sqlite3.connect('mensajeria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre || ' ' || apellido FROM usuarios")
        usuarios = [row[0] for row in cursor.fetchall()]
        conn.close()
        return usuarios

    def cargar_logo(self):
        try:
            imagen_original = Image.open("assets\pngwing.com (59).png")
            imagen_redimensionada = imagen_original.resize((100, 100), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(imagen_redimensionada)
            self.label_logo = tk.Label(self.root, image=self.logo, bg="#2c3e50")
            self.label_logo.grid(row=0, column=0, columnspan=2, pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def enviar_mensaje(self):
        remitente = self.remitente_var.get().strip()
        destinatario = self.destinatario_var.get().strip()
        mensaje = self.entry_mensaje.get().strip()
        if remitente and destinatario and mensaje:
            self.mensajeria.enviar_mensaje(remitente, destinatario, mensaje)
            self.mostrar_mensaje(f"[Enviado] {remitente} a {destinatario}: {mensaje}")
            self.entry_mensaje.delete(0, tk.END)
        else:
            self.mostrar_mensaje("Error: Todos los campos de envío son obligatorios.")

    def recibir_mensaje(self):
        respuesta = self.entry_respuesta.get().strip()
        destinatario = self.destinatario_var.get().strip()
        if destinatario and respuesta:
            self.mostrar_mensaje(f"[Recibido] De {destinatario}: {respuesta}")
            self.entry_respuesta.delete(0, tk.END)
        else:
            self.mostrar_mensaje("Error: Todos los campos de recepción son obligatorios.")

    def vaciar_chat(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

    def mostrar_mensaje(self, mensaje):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, mensaje + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def abrir_gestion_usuarios(self):
        GestionUsuarios(self.root) 



root = tk.Tk()

# Crear un botón para abrir el formulario de agregar usuarios
boton_agregar_usuario = tk.Button(root, text="Agregar Usuario", command=abrir_formulario_usuario)
boton_agregar_usuario.grid(row=0, column=0, padx=10, pady=10)

app = MensajeriaApp(root)
root.mainloop()