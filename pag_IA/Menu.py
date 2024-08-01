import tkinter as tk
from tkinter import ttk
from PIL import ImageFont, ImageTk
import graficos  # Importar el archivo graficos.py
import ver_tabla  # Importar el archivo ver_tabla.py
import IA  # Importar el archivo IA.py
import inicio  # Importar el archivo inicio.py
import Cuestionario  # Importar el archivo Cuestionario.py
import time  # Importar el módulo time para actualizar la hora y la fecha

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Lateral")
        self.geometry("1500x800")  # Aumentar el tamaño de la ventana principal

        # Ruta absoluta al archivo de fuente
        font_path = "MaterialIcons-Regular.ttf"
        self.material_icons = ImageFont.truetype(font_path, 16)

        # Inicializar el modo oscuro
        self.dark_mode = False

        # Crear panel izquierdo
        self.sidebar = tk.Frame(self, width=250, height=800)  # Ajustar la altura del panel lateral
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)  # Cambiar el fill a Y para ajustar la altura

        # Crear panel derecho
        self.main_content = tk.Frame(self, bg="white")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Asegurarse de que el panel derecho expanda

        # Inicializar lista de widgets del contenido principal
        self.main_content_widgets = []

        # Crear estilo para los botones
        self.style = ttk.Style()
        self.configure_styles()

        # Añadir contenido al panel lateral
        self.create_sidebar_content()

        # Botón para cambiar modo oscuro
        self.toggle_dark_mode_btn = tk.Canvas(self.sidebar, width=50, height=25, bg="#ccc", bd=0, highlightthickness=0)
        self.toggle_dark_mode_btn.pack(side=tk.BOTTOM, pady=20)
        self.toggle_button_circle = self.toggle_dark_mode_btn.create_oval(2, 2, 23, 23, fill="white", outline="")
        self.toggle_dark_mode_btn.bind("<Button-1>", self.toggle_dark_mode)

        # Configurar modo inicial
        self.apply_dark_mode()  # Asegúrate de aplicar el modo al inicio

        # Establecer la página actual
        self.current_page = "Inicio"
        self.create_main_content()

        # Iniciar la actualización de la hora y la fecha
        self.show_time()

    def configure_styles(self):
        # Configurar estilos para los botones
        self.style.configure("Sidebar.TButton",
                             font=("Arial", 12),
                             padding=10,
                             background="#4CAF50",  # Verde para el modo claro
                             foreground="black"
                             )
        self.style.map("Sidebar.TButton",
                       background=[("active", "#45a049"), ("pressed", "#388e3c")],
                       foreground=[("active", "black"), ("pressed", "white")],
                       relief=[("pressed", "sunken")],
                       borderwidth=[("pressed", 2)]
                       )

    def create_sidebar_content(self):
        self.colors = {
            'sidebar': '#4CAF50' if not self.dark_mode else '#333',
            'text': '#fff' if self.dark_mode else '#000',
            'bg': '#fff' if not self.dark_mode else '#222',
            'fg': '#000' if not self.dark_mode else '#fff'
        }

        # Hora y fecha
        self.date_time = tk.Label(self.sidebar, text="", bg=self.colors['sidebar'], fg=self.colors['text'])
        self.date_time.pack(pady=(20, 10), anchor='center')

        # Logo
        self.logoImage = ImageTk.PhotoImage(file='images/hyy.png')
        self.logo = tk.Label(self.sidebar, image=self.logoImage, bg=self.colors['sidebar'])
        self.logo.pack(pady=(10, 10), anchor='center')

        # Nombre de la marca
        self.brandName = tk.Label(self.sidebar, text='Sen Gideons', bg=self.colors['sidebar'], font=("", 15, "bold"),
                                  fg=self.colors['text'])
        self.brandName.pack(pady=(0, 20), anchor='center')

        # Dashboard
        self.dashboardImage = ImageTk.PhotoImage(file='images/dashboard-icon.png')
        self.dashboard = tk.Button(self.sidebar, image=self.dashboardImage, bg=self.colors['sidebar'], bd=0,
                                   cursor='hand2', activebackground=self.colors['sidebar'],
                                   command=lambda: self.on_button_click("Inicio"))
        self.dashboard.pack(pady=5, anchor='center')
        self.dashboard_text = tk.Label(self.sidebar, text="Dashboard", bg=self.colors['sidebar'], font=("", 13, "bold"),
                                       fg=self.colors['text'])
        self.dashboard_text.pack(pady=(0, 20), anchor='center')

        # Modelo matemático
        self.manageImage = ImageTk.PhotoImage(file='images/manage-icon.png')
        self.manage = tk.Button(self.sidebar, image=self.manageImage, bg=self.colors['sidebar'], bd=0,
                                cursor='hand2', activebackground=self.colors['sidebar'],
                                command=lambda: self.on_button_click("Modelo matemático"))
        self.manage.pack(pady=5, anchor='center')
        self.manage_text = tk.Label(self.sidebar, text="Modelo matemático", bg=self.colors['sidebar'],
                                    font=("", 13, "bold"), fg=self.colors['text'])
        self.manage_text.pack(pady=(0, 20), anchor='center')

        # IA
        self.settingsImage = ImageTk.PhotoImage(file='images/settings-icon.png')
        self.settings = tk.Button(self.sidebar, image=self.settingsImage, bg=self.colors['sidebar'], bd=0,
                                  cursor='hand2', activebackground=self.colors['sidebar'],
                                  command=lambda: self.on_button_click("IA"))
        self.settings.pack(pady=5, anchor='center')
        self.settings_text = tk.Label(self.sidebar, text="IA", bg=self.colors['sidebar'], font=("", 13, "bold"),
                                      fg=self.colors['text'])
        self.settings_text.pack(pady=(0, 20), anchor='center')

        # Reportes
        self.ExitImage = ImageTk.PhotoImage(file='images/exit-icon.png')
        self.Exit = tk.Button(self.sidebar, image=self.ExitImage, bg=self.colors['sidebar'], bd=0,
                              cursor='hand2', activebackground=self.colors['sidebar'],
                              command=lambda: self.on_button_click("Reportes"))
        self.Exit.pack(pady=5, anchor='center')
        self.Exit_text = tk.Label(self.sidebar, text="Reportes", bg=self.colors['sidebar'], font=("", 13, "bold"),
                                  fg=self.colors['text'])
        self.Exit_text.pack(pady=(0, 20), anchor='center')

        # Cuestionario
        self.quizImage = ImageTk.PhotoImage(file='images/quiz-icon.png')  # Asegúrate de tener el icono correcto
        self.quiz = tk.Button(self.sidebar, image=self.quizImage, bg=self.colors['sidebar'], bd=0,
                              cursor='hand2', activebackground=self.colors['sidebar'],
                              command=lambda: self.on_button_click("Cuestionario"))
        self.quiz.pack(pady=5, anchor='center')
        self.quiz_text = tk.Label(self.sidebar, text="Cuestionario", bg=self.colors['sidebar'], font=("", 13, "bold"),
                                  fg=self.colors['text'])
        self.quiz_text.pack(pady=(0, 20), anchor='center')

    def create_main_content(self):
        # Destruye los widgets anteriores en el contenido principal
        for widget in self.main_content_widgets:
            widget.destroy()
        self.main_content_widgets.clear()

        # Crea el contenido principal según la página actual
        if self.current_page == "Inicio":
            # Crear un frame para el contenido del archivo inicio.py
            frame = tk.Frame(self.main_content, bg="white" if not self.dark_mode else "#222")
            frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Añadir padding para un mejor espaciado
            self.main_content_widgets.append(frame)

            # Llamar a la función principal del archivo inicio.py
            inicio.main(frame)
        elif self.current_page == "Modelo matemático":
            # Crear un canvas con scrollbar para el contenido del modelo matemático
            canvas = tk.Canvas(self.main_content, bg="white" if not self.dark_mode else "#222")
            scrollbar = ttk.Scrollbar(self.main_content, orient="vertical", command=canvas.yview)
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

            self.main_content_widgets.append(canvas)
            self.main_content_widgets.append(scrollbar)

            # Llamar a la función para mostrar gráficos
            self.mostrar_graficos_modelo_matematico(scrollable_frame)
        elif self.current_page == "IA":
            frame = tk.Frame(self.main_content, bg="white" if not self.dark_mode else "#222")
            frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            self.main_content_widgets.append(frame)
            IA.main(frame)
        elif self.current_page == "Reportes":
            # Crear un frame para el contenido del archivo ver_tabla.py
            frame = tk.Frame(self.main_content, bg="white" if not self.dark_mode else "#222")
            frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Añadir padding para un mejor espaciado
            self.main_content_widgets.append(frame)

            # Llamar a la función principal del archivo ver_tabla.py
            ver_tabla.main(frame)
        elif self.current_page == "Cuestionario":
            # Crear un frame para el contenido del cuestionario
            frame = tk.Frame(self.main_content, bg="white" if not self.dark_mode else "#222")
            frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Añadir padding para un mejor espaciado
            self.main_content_widgets.append(frame)

            # Llamar a la función principal del archivo Cuestionario.py
            Cuestionario.main(frame)

    def mostrar_graficos_modelo_matematico(self, parent):
        try:
            graficos.mostrar_grafico_crecimiento_plantas(parent, self.main_content_widgets)
            graficos.mostrar_grafico_crecimiento_plantas_tierra(parent, self.main_content_widgets)
            graficos.mostrar_grafico_n_hojas(parent, self.main_content_widgets)
            graficos.mostrar_grafico_af_plantas_agua(parent, self.main_content_widgets)
            graficos.mostrar_grafico_af_plantas_tierra(parent, self.main_content_widgets)
            graficos.mostrar_grafico_regresion_polynomial(parent, self.main_content_widgets)
        except ValueError as e:
            print(f"Error al mostrar gráficos: {e}")

    def on_button_click(self, page_name):
        self.current_page = page_name
        self.create_main_content()

    def apply_dark_mode(self):
        self.colors = {
            'sidebar': '#333' if self.dark_mode else '#4CAF50',
            'text': '#fff' if self.dark_mode else '#000',
            'bg': '#222' if self.dark_mode else '#fff',
            'fg': '#fff' if self.dark_mode else '#000'
        }

        self.sidebar.config(bg=self.colors['sidebar'])
        self.main_content.config(bg=self.colors['bg'])
        self.date_time.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.logo.config(bg=self.colors['sidebar'])
        self.brandName.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.dashboard.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
        self.dashboard_text.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.manage.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
        self.manage_text.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.settings.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
        self.settings_text.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.Exit.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
        self.Exit_text.config(bg=self.colors['sidebar'], fg=self.colors['text'])
        self.quiz.config(bg=self.colors['sidebar'], activebackground=self.colors['sidebar'])
        self.quiz_text.config(bg=self.colors['sidebar'], fg=self.colors['text'])

    def toggle_dark_mode(self, event=None):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()
        self.create_main_content()  # Volver a crear el contenido principal para aplicar el modo oscuro

        # Cambiar la posición del círculo del botón de modo oscuro
        if self.dark_mode:
            self.toggle_dark_mode_btn.coords(self.toggle_button_circle, 25, 2, 46, 23)
            self.toggle_dark_mode_btn.config(bg="#555")
        else:
            self.toggle_dark_mode_btn.coords(self.toggle_button_circle, 2, 2, 23, 23)
            self.toggle_dark_mode_btn.config(bg="#ccc")

    def show_time(self):
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%d/%m/%Y")
        self.date_time.config(text=f"{current_time}\n{current_date}")
        self.after(1000, self.show_time)  # Actualizar cada segundo

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
