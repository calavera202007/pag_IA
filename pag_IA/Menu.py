import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageFont, ImageDraw, Image, ImageTk
import hashlib
import re
import time
import psycopg2
import graficos
import ver_tabla
import IA
import inicio
import Cuestionario
import matplotlib.pyplot as plt


#######
# Definición de la clase MainApp antes de su uso
class MainApp(tk.Tk):
    def __init__(self, user_name, user_role):
        super().__init__()
        self.title("Menú Lateral")
        self.geometry("1350x650")
        self.resizable(False, False)
        self.user_name = user_name
        self.user_role = user_role  # Guardar el rol del usuario

        font_path = "MaterialIcons-Regular.ttf"
        self.material_icons = ImageFont.truetype(font_path, 18)

        self.dark_mode = False
        self.current_page = "Inicio"

        self.sidebar = tk.Frame(self, width=200, height=800)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_content = tk.Frame(self)
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_content_widgets = []

        self.style = ttk.Style()
        self.configure_styles()

        self.colors = self.get_colors()

        self.create_sidebar_content()

        self.toggle_dark_mode_btn = tk.Canvas(self.sidebar, width=40, height=20, bd=0, highlightthickness=0)
        self.toggle_dark_mode_btn.pack(side=tk.BOTTOM, pady=15)
        self.toggle_button_circle = self.toggle_dark_mode_btn.create_oval(2, 2, 18, 18, fill="white", outline="")
        self.toggle_dark_mode_btn.bind("<Button-1>", self.toggle_dark_mode)

        self.apply_dark_mode()
        self.create_main_content()
        self.show_time()

    def get_colors(self):
        return {
            'sidebar': '#333' if self.dark_mode else '#4CAF50',
            'text': '#fff' if self.dark_mode else '#000',
            'bg': '#222' if self.dark_mode else '#fff',
            'fg': '#fff' if self.dark_mode else '#000',
            'icon': 'white' if self.dark_mode else 'black',
            'icon_hover': 'grey'
        }

    def configure_styles(self):
        self.style.configure("Sidebar.TButton",
                             font=("Arial", 6),
                             padding=8)
        self.style.map("Sidebar.TButton",
                       relief=[("pressed", "sunken")],
                       borderwidth=[("pressed", 2)])

    def create_icon_image(self, icon_char, color=None):
        image = Image.new("RGBA", (25, 25), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        icon_color = color if color else self.colors['icon']
        draw.text((5, 5), icon_char, font=self.material_icons, fill=icon_color)
        return ImageTk.PhotoImage(image)

    def create_sidebar_content(self):
        self.date_time = tk.Label(self.sidebar, text="", bg=self.colors['sidebar'], fg=self.colors['text'])
        self.date_time.pack(pady=(15, 8), anchor='center')

        self.logoImage = ImageTk.PhotoImage(file='images/hyy.png')
        self.logo = tk.Label(self.sidebar, image=self.logoImage, bg=self.colors['sidebar'])
        self.logo.pack(pady=(8, 8), anchor='center')

        self.brandName = tk.Label(self.sidebar, text=self.user_name, bg=self.colors['sidebar'], font=("", 15, "bold"),
                                  fg=self.colors['text'])
        self.brandName.pack(pady=(0, 15), anchor='center')

        # Definir los botones del menú lateral
        buttons = [
            ("Dashboard", "\ue871", "Inicio"),
            ("Modelo matemático", "\ue8b8", "Modelo matemático"),
            ("IA", "\ue8b6", "IA"),
            ("Reportes", "\ue8b3", "Reportes"),
            ("Salir", "\ue879", "Salir")
        ]

        # Añadir el botón "Cuestionario" solo si el rol del usuario es "Super Administrador"
        if self.user_role == "Super Administrador":
            buttons.insert(-1, ("Cuestionario", "\ue8f4", "Cuestionario"))

        for text, icon_char, page in buttons:
            icon_image = self.create_icon_image(icon_char)
            button = tk.Button(self.sidebar, image=icon_image, bg=self.colors['sidebar'], bd=0,
                               cursor='hand2', activebackground=self.colors['sidebar'],
                               command=lambda p=page: self.on_button_click(p))
            button.image = icon_image
            button.pack(pady=3, anchor='center')
            button.bind("<Enter>", lambda event, ic=icon_char, b=button: self.on_hover(event, ic, b))
            button.bind("<Leave>", lambda event, ic=icon_char, b=button: self.on_leave(event, ic, b))

            label = tk.Label(self.sidebar, text=text, bg=self.colors['sidebar'], font=("", 13, "bold"),
                             fg=self.colors['text'])
            label.pack(pady=(0, 15), anchor='center')
            setattr(self, f"{page.lower().replace(' ', '_')}_button", button)
            setattr(self, f"{page.lower().replace(' ', '_')}_label", label)

    def on_hover(self, event, icon_char, button):
        icon_image = self.create_icon_image(icon_char, color=self.colors['icon_hover'])
        button.config(image=icon_image)
        button.image = icon_image

    def on_leave(self, event, icon_char, button):
        icon_image = self.create_icon_image(icon_char)
        button.config(image=icon_image)
        button.image = icon_image
##
    def create_main_content(self):
        for widget in self.main_content_widgets:
            widget.destroy()
        self.main_content_widgets.clear()

        frame = tk.Frame(self.main_content, bg=self.colors['bg'])
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.main_content_widgets.append(frame)

        if self.current_page == "Inicio":
            inicio.main(frame)
        elif self.current_page == "Modelo matemático":
            canvas = tk.Canvas(frame, bg=self.colors['bg'])
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.mostrar_graficos_modelo_matematico(scrollable_frame)
        elif self.current_page == "IA":
            IA.main(frame)
        elif self.current_page == "Reportes":
            ver_tabla.main(frame, self.user_role)  # Pasa el rol del usuario a ver_tabla
        elif self.current_page == "Cuestionario":
            Cuestionario.main(frame)

    def mostrar_graficos_modelo_matematico(self, parent):
        try:
            main_frame = ttk.Frame(parent)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Opciones del menú desplegable y sus funciones correspondientes
            opciones_menu = {
                "Crecimiento": [
                    graficos.mostrar_grafico_crecimiento_plantas,
                    graficos.mostrar_grafico_crecimiento_plantas_tierra
                ],
                "N. Hojas": [
                    graficos.mostrar_grafico_n_hojas,
                    graficos.mostrar_grafico_n_hojas_tierra
                ],
                "Área Foliar Tierra": [
                    graficos.mostrar_grafico_af_plantas_agua_v1,
                    graficos.mostrar_grafico_af_plantas_agua_v2
                ],
                "Área Foliar Agua": [
                    graficos.mostrar_grafico_af_plantas_tierra_v1,
                    graficos.mostrar_grafico_af_plantas_tierra_v2
                ],
                "Regresión Polynomial": [
                    graficos.mostrar_grafico_regresion_polynomial
                ],
                "Todos": [
                    graficos.mostrar_grafico_crecimiento_plantas,
                    graficos.mostrar_grafico_crecimiento_plantas_tierra,
                    graficos.mostrar_grafico_n_hojas,
                    graficos.mostrar_grafico_n_hojas_tierra,
                    graficos.mostrar_grafico_af_plantas_agua_v1,
                    graficos.mostrar_grafico_af_plantas_agua_v2,
                    graficos.mostrar_grafico_af_plantas_tierra_v1,
                    graficos.mostrar_grafico_af_plantas_tierra_v2,
                    graficos.mostrar_grafico_regresion_polynomial
                ]
            }

            # Crear un menú desplegable con "Todos" como opción seleccionada por defecto
            selected_option = tk.StringVar(value="Todos")
            dropdown = ttk.OptionMenu(main_frame, selected_option, "Todos", *opciones_menu.keys())
            dropdown.pack(pady=10)

            # Función para actualizar los gráficos mostrados según la selección del menú desplegable
            def actualizar_graficos(*args):
                # Limpiar gráficos actuales
                for widget in main_frame.winfo_children():
                    if isinstance(widget, ttk.Frame) and widget is not dropdown:
                        widget.destroy()

                # Obtener las funciones de gráficos correspondientes a la opción seleccionada
                funciones_graficos = opciones_menu.get(selected_option.get(), [])

                # Mostrar las gráficas en una cuadrícula de dos por fila
                for i in range(0, len(funciones_graficos), 2):
                    row_frame = ttk.Frame(main_frame)
                    row_frame.pack(fill=tk.X, expand=True, pady=5)

                    for j in range(2):
                        if i + j < len(funciones_graficos):
                            # Verificar si la opción seleccionada es "Regresión Polynomial" para ajustar el tamaño
                            if selected_option.get() == "Regresión Polynomial":
                                graph_frame = ttk.Frame(row_frame, width=1140, height=940)  # Duplicar tamaño
                            else:
                                graph_frame = ttk.Frame(row_frame, width=570, height=470)  # Tamaño estándar

                            graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
                            graph_frame.pack_propagate(False)

                            funciones_graficos[i + j](graph_frame, self.main_content_widgets)

                            # Asegurarse de cerrar la figura para liberar memoria
                            plt.close('all')

            # Llamar a la función para actualizar gráficos inicialmente con la opción "Todos"
            actualizar_graficos()

            # Llamar a la función para actualizar gráficos al cambiar la selección del menú desplegable
            selected_option.trace_add("write", actualizar_graficos)

            # Agregar el marco principal a los widgets de contenido principal
            self.main_content_widgets.append(main_frame)

        except ValueError as e:
            print(f"Error al mostrar gráficos: {e}")

    def on_button_click(self, page_name):
        self.current_page = page_name
        if page_name == "Salir":
            self.confirm_exit()
        else:
            self.create_main_content()

    def confirm_exit(self):
        response = messagebox.askyesno("Confirmar Salida", "¿Estás seguro de que quieres salir?")
        if response:
            self.quit_app()
        else:
            self.current_page = "Inicio"
            self.create_main_content()

    def apply_dark_mode(self):
        self.colors = self.get_colors()

        self.sidebar.config(bg=self.colors['sidebar'])
        self.main_content.config(bg=self.colors['bg'])
        self.date_time.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.logo.config(bg=self.colors['sidebar'])
        self.brandName.config(bg=self.colors['sidebar'], fg=self.colors['text'])

        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
            elif isinstance(widget, tk.Label):
                widget.config(bg=self.colors['sidebar'], fg=self.colors['text'])

        self.style.configure("Sidebar.TButton",
                             background=self.colors['sidebar'],
                             foreground=self.colors['text'])
        self.style.map("Sidebar.TButton",
                       background=[("active", self.colors['sidebar']),
                                   ("pressed", self.colors['sidebar'])],
                       foreground=[("active", self.colors['text']),
                                   ("pressed", self.colors['text'])])

        self.update_icons()

    def update_icons(self):
        buttons = [
            ("Dashboard", "\ue871", "Inicio"),
            ("Modelo matemático", "\ue8b8", "Modelo matemático"),
            ("IA", "\ue8b6", "IA"),
            ("Reportes", "\ue8b3", "Reportes"),
            ("Cuestionario", "\ue8f4", "Cuestionario"),
            ("Salir", "\ue879", "Salir")
        ]

        for _, icon_char, page in buttons:
            icon_image = self.create_icon_image(icon_char)

            # Verificar si el botón existe antes de intentar actualizar su ícono
            button_name = f"{page.lower().replace(' ', '_')}_button"
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                button.config(image=icon_image)
                button.image = icon_image

    def toggle_dark_mode(self, event=None):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()
        self.create_main_content()

        if self.dark_mode:
            self.toggle_dark_mode_btn.coords(self.toggle_button_circle, 25, 2, 46, 23)
            self.toggle_dark_mode_btn.config(bg="#555")
        else:
            self.toggle_dark_mode_btn.coords(self.toggle_button_circle, 2, 2, 23, 23)
            self.toggle_dark_mode_btn.config(bg="#ccc")

    def quit_app(self):
        try:
            self.destroy()
        except tk.TclError:
            pass

    def show_time(self):
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%d/%m/%Y")
        self.date_time.config(text=f"{current_time}\n{current_date}")
        self.after(1000, self.show_time)


# Función login, después de definir MainApp
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def is_robot_detected(entry):
    return time.time() - entry.last_modified < 0.5


def verify_credentials(username, password):
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="Yamile25",
            host="localhost",
            port="5432",
            database="Lestoma"
        )
        cursor = conn.cursor()
        encoded_password = hashlib.sha512(password.encode()).hexdigest()

        # Asegúrate de que el nombre de la columna coincida con el de tu base de datos
        cursor.execute("""
            SELECT u."UsrNombre", r."RolNombre"
            FROM "Super Administrador"."Usuario" u
            JOIN "Super Administrador"."Rol" r ON u."UsrIdRol" = r."RolId"
            WHERE u."UsrCorreo" = %s AND u."UsrContrasenna" = %s
        """, (username, encoded_password))

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0], result[1]  # Retornar el nombre del usuario y el nombre del rol
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Error", f"Error al conectarse a la base de datos: {error}")
        return None



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
    else:
        user_info = verify_credentials(username, password)
        if user_info is None:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
        else:
            user_name, user_role = user_info  # Obtener el nombre del usuario y el rol
            messagebox.showinfo("Éxito", f"Inicio de sesión exitoso. Rol: {user_role}")
            root.destroy()  # Cerrar la ventana de inicio de sesión
            app = MainApp(user_name, user_role)  # Pasar el nombre de usuario y el rol a MainApp
            app.mainloop()




def on_entry_change(event, entry):
    entry.last_modified = time.time()


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

background_image = tk.PhotoImage(file="images/fondo.png")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

login_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
login_frame.place(x=150, y=100, width=300, height=260)

title_label = tk.Label(login_frame, text="Iniciar Sesión", font=("Arial", 14, "bold"), bg="#FFFFFF")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

username_label = tk.Label(login_frame, text="Correo electrónico:", font=("Arial", 10), bg="#FFFFFF")
username_label.grid(row=1, column=0, pady=5)
entry_username = tk.Entry(login_frame, font=("Arial", 10))
entry_username.grid(row=1, column=1, pady=5)
entry_username.last_modified = time.time()
entry_username.bind("<KeyRelease>", lambda event: on_entry_change(event, entry_username))

password_label = tk.Label(login_frame, text="Contraseña:", font=("Arial", 10), bg="#FFFFFF")
password_label.grid(row=2, column=0, pady=5)
entry_password = tk.Entry(login_frame, font=("Arial", 10), show="*")
entry_password.grid(row=2, column=1, pady=5)
entry_password.last_modified = time.time()
entry_password.bind("<KeyRelease>", lambda event: on_entry_change(event, entry_password))

show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(login_frame, text="Mostrar contraseña", variable=show_password_var, bg="#FFFFFF",
                                     command=toggle_password_visibility)
show_password_check.grid(row=3, column=0, columnspan=2, pady=5)

var_no_robot = tk.BooleanVar()
check_no_robot = tk.Checkbutton(login_frame, text="No soy un robot", variable=var_no_robot, bg="#FFFFFF")
check_no_robot.grid(row=4, column=0, columnspan=2, pady=5)

login_button = tk.Button(login_frame, text="Iniciar Sesión", font=("Arial", 10), bg="#4CAF50", fg="#FFFFFF",
                         command=login)
login_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
