from tkinter import *
from PIL import ImageTk, Image
import webbrowser
import graficos

class Dashboard2:
    def __init__(self, frame):
        self.frame = frame
        self.frame.config(bg="white")

        self.theme = 'light'  # Tema por defecto
        self.colors = self.get_colors(self.theme)

        self.init_ui()

    def init_ui(self):
        # Creación de los marcos con el color de fondo apropiado
        self.bodyFrame1 = Frame(self.frame, bg=self.colors['body_frame'])
        self.bodyFrame1.place(x=20, y=20, width=1300, height=350)
        self.bodyFrame2 = Frame(self.frame, bg=self.colors['body_frame2'])
        self.bodyFrame2.place(x=200, y=380, width=310, height=220)
        self.bodyFrame3 = Frame(self.frame, bg=self.colors['body_frame3'])
        self.bodyFrame3.place(x=520, y=380, width=310, height=220)
        self.bodyFrame4 = Frame(self.frame, bg=self.colors['body_frame4'])
        self.bodyFrame4.place(x=840, y=380, width=310, height=220)

        self.show_graphs(self.bodyFrame1)
        self.load_images()

        # Agregar texto de derechos de autor
        self.copyright_label = Label(
            self.frame,
            text="© Derechos de autor pertenecen al Semillero de Investigación GISTFA, Laboratorio Lestoma",
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.copyright_label.place(x=450, y=750)

    def get_colors(self, theme):
        if theme == 'dark':
            return {
                'bg': '#2e2e2e', 'body_frame': '#3e3e3e', 'body_frame2': '#4e4e4e',
                'body_frame3': '#5e5e5e', 'body_frame4': '#6e6e6e',
                'heading': '#ffffff', 'fg': '#ffffff'
            }
        else:
            return {
                'bg': '#eff5f6', 'body_frame': '#ffffff', 'body_frame2': '#009aa5',
                'body_frame3': '#e21f26', 'body_frame4': '#ffcb1f',
                'heading': '#0064d3', 'fg': '#000000'
            }

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.colors = self.get_colors(self.theme)
        self.update_ui_colors()

    def update_ui_colors(self):
        # Actualización de colores para todos los marcos y widgets
        self.frame.config(bg=self.colors['bg'])
        for i in range(1, 5):
            getattr(self, f'bodyFrame{i}').config(bg=self.colors[f'body_frame{i if i == 1 else ""}'])

        # Actualizar color del texto de derechos de autor
        self.copyright_label.config(bg=self.colors['bg'], fg=self.colors['fg'])

    def show_graphs(self, frame):
        # Resize image to match the size of the graph
        image = Image.open('images/blender.jpeg')
        image = image.resize((600, 400), Image.Resampling.LANCZOS)  # Adjust the size as needed
        photo = ImageTk.PhotoImage(image)
        image_label = Label(frame, image=photo, borderwidth=0)
        image_label.image = photo  # keep a reference!
        image_label.pack(side=LEFT, fill=BOTH, expand=True)

        # Adjust the size of the custom plot similarly
        main_content_widgets = []
        graficos.mostrar_grafico_regresion_polynomial(frame, main_content_widgets)

    def load_images(self):
        # Cargando y centrando imágenes en los tres marcos inferiores
        for i, img_name in enumerate(["train.jpg", "repositorio.jpg", "result.jpg"]):
            img_path = f'images/{img_name}'
            img = Image.open(img_path)
            img = img.resize((300, 200), Image.Resampling.LANCZOS)  # Ajusta el tamaño según sea necesario
            photo = ImageTk.PhotoImage(img)
            img_label = Label(getattr(self, f'bodyFrame{i + 2}'), image=photo, borderwidth=0)
            img_label.image = photo
            img_label.pack(fill=BOTH, expand=True)  # Asegura que la imagen se centre y ajuste al tamaño del marco

            # Vinculando el enlace solo a la imagen repositorio.jpg
            if img_name == "repositorio.jpg":
                img_label.bind('<Button-1>',
                               lambda e, url="https://universe.roboflow.com/ia-nsg4u/pest_detector-2": webbrowser.open(
                                   url))


def main(root):
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)
    app = Dashboard2(frame)
