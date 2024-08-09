import tkinter as tk
from tkinter import ttk
from PIL import ImageFont, ImageTk
import graficos
import ver_tabla
import IA
import inicio
import Cuestionario
import time

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Lateral")
        self.geometry("1500x800")

        font_path = "MaterialIcons-Regular.ttf"
        self.material_icons = ImageFont.truetype(font_path, 16)

        self.dark_mode = False
        self.current_page = "Inicio"

        self.sidebar = tk.Frame(self, width=250, height=800)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_content = tk.Frame(self)
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_content_widgets = []

        self.style = ttk.Style()
        self.configure_styles()

        self.colors = self.get_colors()

        self.create_sidebar_content()

        self.toggle_dark_mode_btn = tk.Canvas(self.sidebar, width=50, height=25, bd=0, highlightthickness=0)
        self.toggle_dark_mode_btn.pack(side=tk.BOTTOM, pady=20)
        self.toggle_button_circle = self.toggle_dark_mode_btn.create_oval(2, 2, 23, 23, fill="white", outline="")
        self.toggle_dark_mode_btn.bind("<Button-1>", self.toggle_dark_mode)

        self.apply_dark_mode()
        self.create_main_content()
        self.show_time()

    def get_colors(self):
        return {
            'sidebar': '#333' if self.dark_mode else '#4CAF50',
            'text': '#fff' if self.dark_mode else '#000',
            'bg': '#222' if self.dark_mode else '#fff',
            'fg': '#fff' if self.dark_mode else '#000'
        }

    def configure_styles(self):
        self.style.configure("Sidebar.TButton",
                             font=("Arial", 12),
                             padding=10)
        self.style.map("Sidebar.TButton",
                       relief=[("pressed", "sunken")],
                       borderwidth=[("pressed", 2)])

    def create_sidebar_content(self):
        self.date_time = tk.Label(self.sidebar, text="", bg=self.colors['sidebar'], fg=self.colors['text'])
        self.date_time.pack(pady=(20, 10), anchor='center')

        self.logoImage = ImageTk.PhotoImage(file='images/hyy.png')
        self.logo = tk.Label(self.sidebar, image=self.logoImage, bg=self.colors['sidebar'])
        self.logo.pack(pady=(10, 10), anchor='center')

        self.brandName = tk.Label(self.sidebar, text='Sen Gideons', bg=self.colors['sidebar'], font=("", 15, "bold"),
                                  fg=self.colors['text'])
        self.brandName.pack(pady=(0, 20), anchor='center')

        buttons = [
            ("Dashboard", "dashboard-icon.png", "Inicio"),
            ("Modelo matemático", "manage-icon.png", "Modelo matemático"),
            ("IA", "settings-icon.png", "IA"),
            ("Reportes", "exit-icon.png", "Reportes"),
            ("Cuestionario", "quiz-icon.png", "Cuestionario")
        ]

        for text, icon, page in buttons:
            image = ImageTk.PhotoImage(file=f'images/{icon}')
            button = tk.Button(self.sidebar, image=image, bg=self.colors['sidebar'], bd=0,
                               cursor='hand2', activebackground=self.colors['sidebar'],
                               command=lambda p=page: self.on_button_click(p))
            button.image = image
            button.pack(pady=5, anchor='center')
            label = tk.Label(self.sidebar, text=text, bg=self.colors['sidebar'], font=("", 13, "bold"),
                             fg=self.colors['text'])
            label.pack(pady=(0, 20), anchor='center')
            setattr(self, f"{page.lower().replace(' ', '_')}_button", button)
            setattr(self, f"{page.lower().replace(' ', '_')}_label", label)

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
            ver_tabla.main(frame)
        elif self.current_page == "Cuestionario":
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

    def show_time(self):
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%d/%m/%Y")
        self.date_time.config(text=f"{current_time}\n{current_date}")
        self.after(1000, self.show_time)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()