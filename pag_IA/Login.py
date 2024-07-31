import tkinter as tk
from tkinter import messagebox

# Función para validar las credenciales
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Validaciones básicas
    if len(username) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y una contraseña.")
    elif username != "admin" or password != "admin123":
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
    else:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("600x400")  # Aumentar el tamaño de la ventana
root.resizable(False, False)

# Configuración del fondo
background_image = tk.PhotoImage(file="fondo.png")  # Reemplaza "fondo.png" con la ruta de tu imagen de fondo
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Configuración del frame de login
login_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
login_frame.place(x=150, y=100, width=300, height=200)  # Ajustar la posición del frame

# Título del login
title_label = tk.Label(login_frame, text="Iniciar Sesión", font=("Arial", 14, "bold"), bg="#FFFFFF")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Campo de nombre de usuario
username_label = tk.Label(login_frame, text="Nombre de usuario:", font=("Arial", 10), bg="#FFFFFF")
username_label.grid(row=1, column=0, pady=5)
entry_username = tk.Entry(login_frame, font=("Arial", 10))
entry_username.grid(row=1, column=1, pady=5)

# Campo de contraseña
password_label = tk.Label(login_frame, text="Contraseña:", font=("Arial", 10), bg="#FFFFFF")
password_label.grid(row=2, column=0, pady=5)
entry_password = tk.Entry(login_frame, font=("Arial", 10), show="*")
entry_password.grid(row=2, column=1, pady=5)

# Botón de inicio de sesión
login_button = tk.Button(login_frame, text="Iniciar Sesión", font=("Arial", 10), bg="#4CAF50", fg="#FFFFFF", command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)  # Ajuste horizontal

# Iniciar el loop principal
root.mainloop()
