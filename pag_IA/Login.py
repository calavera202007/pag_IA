import tkinter as tk
from tkinter import messagebox
import time

# Función para validar las credenciales
def login():
    try:
        username = entry_username.get()
        password = entry_password.get()

        # Verificación de la casilla "No soy un robot"
        if not var_no_robot.get():
            raise Exception("Por favor, confirme que no es un robot.")

        # Simulación de una detección de robot (si el tiempo entre el último ingreso de texto es muy corto)
        if (time.time() - entry_username.last_modified < 0.5) or (time.time() - entry_password.last_modified < 0.5):
            raise Exception("Acción sospechosa detectada. Podría ser un robot.")

        # Validaciones básicas
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y una contraseña.")
        elif not username.endswith("@ucundinamarca.edu.co"):
            messagebox.showerror("Error", "El correo debe terminar en @ucundinamarca.edu.co.")
        elif username != "admin@ucundinamarca.edu.co" or password != "admin123":
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
        else:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función para actualizar el tiempo de modificación
def on_entry_change(event, entry):
    entry.last_modified = time.time()

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
login_frame.place(x=150, y=100, width=300, height=220)

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

# Casilla de verificación "No soy un robot"
var_no_robot = tk.BooleanVar()
check_no_robot = tk.Checkbutton(login_frame, text="No soy un robot", variable=var_no_robot, bg="#FFFFFF")
check_no_robot.grid(row=3, column=0, columnspan=2, pady=5)

# Botón de inicio de sesión
login_button = tk.Button(login_frame, text="Iniciar Sesión", font=("Arial", 10), bg="#4CAF50", fg="#FFFFFF", command=login)
login_button.grid(row=4, column=0, columnspan=2, pady=10)

# Iniciar el loop principal
root.mainloop()
