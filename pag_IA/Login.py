import tkinter as tk
from tkinter import messagebox
import time
import psycopg2
import hashlib
import re  # Importar el módulo de expresiones regulares
import os  # Importar el módulo os para ejecutar el menú

# Función para validar si es una dirección de correo válida
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Función para validar el tiempo entre teclas
def is_robot_detected(entry):
    return time.time() - entry.last_modified < 0.5

# Función para conectar y verificar credenciales
def verify_credentials(username, password):
    try:
        # Conexión a la base de datos PostgreSQL
        conn = psycopg2.connect(
            user="postgres",
            password="Yamile25",
            host="localhost",
            port="5432",
            database="Lestoma"
        )
        cursor = conn.cursor()

        # Codificar la contraseña ingresada con SHA-512
        encoded_password = hashlib.sha512(password.encode()).hexdigest()

        # Consulta para verificar las credenciales
        cursor.execute("""
            SELECT 1 
            FROM "Super Administrador"."Usuario" 
            WHERE "Usuario"."UsrCorreo" = %s AND "Usuario"."UsrContrasenna" = %s
        """, (username, encoded_password))

        # Si se encuentra una coincidencia, devolver True
        result = cursor.fetchone()
        conn.close()

        return result is not None

    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Error", f"Error al conectarse a la base de datos: {error}")
        return False

# Función para validar las credenciales y el captcha
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not var_no_robot.get():
        messagebox.showerror("Error", "Por favor, confirme que no es un robot.")
        return

    if is_robot_detected(entry_username) or is_robot_detected(entry_password):
        messagebox.showerror("Error", "Acción sospechosa detectada. Podría ser un robot.")
        return

    if len(username) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y una contraseña.")
    elif not is_valid_email(username):
        messagebox.showerror("Error", "Por favor, ingrese una dirección de correo válida.")
    elif not verify_credentials(username, password):
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
    else:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
        root.destroy()  # Cerrar la ventana de inicio de sesión
        os.system('python Menu.py')  # Ejecutar el archivo Menu.py


# Función para actualizar el tiempo de modificación
def on_entry_change(event, entry):
    entry.last_modified = time.time()

# Función para mostrar u ocultar la contraseña
def toggle_password_visibility():
    if show_password_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("600x400")
root.resizable(False, False)

# Configuración del fondo
background_image = tk.PhotoImage(file="fondo.png")  # Reemplaza "fondo.png" con la ruta de tu imagen de fondo
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Configuración del frame de login
login_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
login_frame.place(x=150, y=100, width=300, height=260)

# Título del login
title_label = tk.Label(login_frame, text="Iniciar Sesión", font=("Arial", 14, "bold"), bg="#FFFFFF")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Campo de nombre de usuario
username_label = tk.Label(login_frame, text="Correo electrónico:", font=("Arial", 10), bg="#FFFFFF")
username_label.grid(row=1, column=0, pady=5)
entry_username = tk.Entry(login_frame, font=("Arial", 10))
entry_username.grid(row=1, column=1, pady=5)
entry_username.last_modified = time.time()  # Inicializar el tiempo de modificación
entry_username.bind("<KeyRelease>", lambda event: on_entry_change(event, entry_username))

# Campo de contraseña
password_label = tk.Label(login_frame, text="Contraseña:", font=("Arial", 10), bg="#FFFFFF")
password_label.grid(row=2, column=0, pady=5)
entry_password = tk.Entry(login_frame, font=("Arial", 10), show="*")
entry_password.grid(row=2, column=1, pady=5)
entry_password.last_modified = time.time()  # Inicializar el tiempo de modificación
entry_password.bind("<KeyRelease>", lambda event: on_entry_change(event, entry_password))

# Casilla de verificación para mostrar/ocultar la contraseña
show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(login_frame, text="Mostrar contraseña", variable=show_password_var, bg="#FFFFFF", command=toggle_password_visibility)
show_password_check.grid(row=3, column=0, columnspan=2, pady=5)

# Casilla de verificación "No soy un robot"
var_no_robot = tk.BooleanVar()
check_no_robot = tk.Checkbutton(login_frame, text="No soy un robot", variable=var_no_robot, bg="#FFFFFF")
check_no_robot.grid(row=4, column=0, columnspan=2, pady=5)

# Botón de inicio de sesión
login_button = tk.Button(login_frame, text="Iniciar Sesión", font=("Arial", 10), bg="#4CAF50", fg="#FFFFFF", command=login)
login_button.grid(row=5, column=0, columnspan=2, pady=10)

# Iniciar el loop principal
root.mainloop()
