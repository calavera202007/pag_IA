import os
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from PIL import Image, ImageTk
import numpy as np

def main(root):
    # Inicializar el modelo YOLO
    global model
    model = YOLO('models/best.pt')

    # Establecer la conexión con PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="Yamile25",
        host="localhost",
        port="5432",
        database="Lestoma"
    )
    cur = conn.cursor()

    def analizar_imagen():
        # Obtener el índice de la imagen seleccionada
        selected_index = listbox_fotos.curselection()
        if not selected_index:
            # Limpiar la imagen y la información si no se selecciona una imagen
            resultado_label.config(image='', text='')
            info_text_var.set('')
            return

        # Convertir el índice a un número entero
        selected_index = selected_index[0]

        # Obtener la información de la foto seleccionada
        foto_info = fotos[selected_index]
        imagen_path = foto_info[1]  # Suponiendo que la ruta de la imagen está en la segunda posición

        print(f"Ruta de la imagen: {imagen_path}")

        # Verificar si la imagen existe en la ruta especificada
        if not os.path.exists(imagen_path):
            messagebox.showerror("Error", f"La imagen no se encuentra en la ruta: {imagen_path}")
            return

        # Cargar la imagen usando OpenCV
        img = cv2.imread(imagen_path)
        if img is None:
            messagebox.showerror("Error", f"No se pudo cargar la imagen en la ruta: {imagen_path}")
            return

        # Realizar la predicción con el modelo YOLO
        results = model(img)

        # Procesar los resultados y dibujar las cajas de predicción
        img_with_boxes = draw_boxes(img, results)

        # Redimensionar la imagen a 350x350 píxeles
        img_resized = cv2.resize(img_with_boxes, (350, 350))

        # Convertir la imagen a formato RGB para Tkinter
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        # Mostrar la imagen en la interfaz gráfica
        resultado_label.config(image=img_tk)
        resultado_label.image = img_tk  # Mantener una referencia para evitar que la imagen sea recogida por el recolector de basura

        # Mostrar la información de la plaga detectada
        display_results(results)

    def draw_boxes(img, results):
        # Procesar los resultados y dibujar las cajas de predicción
        for result in results:
            boxes = result.boxes.xyxy.numpy()  # Coordenadas de las cajas en formato numpy array
            confidences = result.boxes.conf.numpy()  # Confidencias de las predicciones en formato numpy array
            classes = result.boxes.cls.numpy()  # Clases de las predicciones en formato numpy array
            class_names = result.names  # Nombres de las clases

            for box, conf, cls in zip(boxes, confidences, classes):
                cls_name = class_names[int(cls)] if int(cls) in class_names else "Desconocida"
                x1, y1, x2, y2 = map(int, box)  # Convertir coordenadas a enteros

                # Dibujar la caja delimitadora
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Dibujar la etiqueta
                label = f"{cls_name} {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img

    def display_results(results):
        # Crear un diccionario con la información sobre las plagas
        plagas_info = {
            "gray worm": """
Los gusanos grises, también conocidos como orugas cortadoras, pueden causar daños significativos a los cultivos. 
Aquí tienes información sobre los daños que provocan y cómo controlarlos:
Daños causados por gusanos grises:
- Cortan los tallos de las plantas jóvenes a nivel del suelo
- Se alimentan de hojas, dejando agujeros irregulares
- Dañan raíces y tubérculos subterráneos
- Pueden destruir completamente plántulas recién emergidas
- Reducen el rendimiento y la calidad de los cultivos

Métodos de control:
Control cultural:
- Rotación de cultivos
- Manejo adecuado de malezas
- Labranza del suelo para exponer las larvas a depredadores

Control biológico:
- Uso de enemigos naturales como avispas parasitoides y nematodos entomopatógenos
- Fomento de aves insectívoras en el área de cultivo

Control químico:
- Aplicación de insecticidas específicos, preferiblemente de bajo impacto ambiental
- Uso de cebos envenenados cerca de las plantas

Control físico:
- Colocación de barreras alrededor de las plantas
- Recolección manual de las larvas durante la noche

Monitoreo:
- Inspección regular del cultivo para detectar daños temprano
- Uso de trampas de feromonas para monitorear poblaciones

Manejo integrado de plagas:
- Combinación de varios métodos de control para un manejo más efectivo y sostenible
""",
            "slug": """
Las babosas son moluscos terrestres sin concha, de cuerpo blando y alargado. Suelen medir entre 1 y 15 cm de longitud, 
dependiendo de la especie. Son de movimiento lento y dejan un rastro de baba brillante. Son principalmente activas 
durante la noche y en condiciones húmedas.

Daños causados por babosas:
- Perforan hojas, dejando agujeros irregulares
- Consumen plántulas jóvenes, a veces completamente
- Dañan frutos y hortalizas, especialmente los que están en contacto con el suelo
- Dejan rastros de baba que pueden afectar la calidad y aspecto de las cosechas
- Pueden transmitir enfermedades de una planta a otra

Métodos de control:
Control cultural:
- Mantener el área de cultivo limpia de restos vegetales y escombros
- Regar por la mañana para que el suelo se seque durante el día
- Usar acolchados ásperos como cáscaras de huevo trituradas o diatomeas

Control físico:
- Colocar trampas (tablas, tejas o recipientes con cerveza)
- Crear barreras con materiales abrasivos (ceniza, serrín, arena)
- Recolección manual durante la noche o en días húmedos

Control biológico:
- Fomentar la presencia de depredadores naturales como erizos, sapos y aves
- Utilizar nematodos específicos contra babosas (Phasmarhabditis hermaphrodita)

Control químico:
- Uso de molusquicidas en cebos o gránulos, preferiblemente productos de bajo impacto ambiental
- Aplicación de sal o sulfato de cobre (con precaución, ya que pueden afectar al suelo)

Métodos alternativos:
- Usar plantas repelentes como ajo, menta o lavanda alrededor del cultivo
- Aplicar café molido o cáscaras de cítricos alrededor de las plantas

Prevención:
- Mantener el césped corto alrededor del área de cultivo
- Evitar el exceso de humedad en el suelo
- Inspeccionar regularmente el cultivo, especialmente en condiciones húmedas

Manejo integrado:
- Combinar varios métodos para un control más efectivo y sostenible
""",
            "aphid": """
Los pulgones son pequeños insectos de cuerpo blando, generalmente de 1-3 mm de longitud. Pueden ser de varios colores 
(verde, negro, marrón, rosa). Tienen antenas largas y, en algunas especies, un par de estructuras tubulares llamadas 
sifones en la parte posterior del abdomen. Se reproducen rápidamente y suelen vivir en colonias.

Daños causados:
- Succionan la savia de las plantas, debilitándolas
- Producen una sustancia pegajosa llamada melaza que fomenta el crecimiento de hongos
- Deforman hojas y brotes nuevos
- Transmiten enfermedades virales entre plantas
- En grandes infestaciones, pueden causar marchitamiento y muerte de la planta

Métodos de control:
Control biológico:
- Fomentar la presencia de depredadores naturales como mariquitas, crisopas y avispas parásitas
- Introducir estos insectos beneficiosos en el cultivo

Control cultural:
- Eliminar manualmente las partes infestadas de las plantas
- Usar trampas de color amarillo
- Mantener un buen equilibrio de nutrientes en el suelo

Control físico:
- Rociar las plantas con agua a presión para eliminar los pulgones
- Usar mallas anti-insectos en invernaderos

Control químico:
- Aplicar insecticidas específicos, preferiblemente de origen natural como el aceite de neem
- Usar jabones insecticidas

Control con plantas repelentes:
- Plantar especies como ajo, cebolla o caléndula cerca del cultivo

Monitoreo:
- Inspeccionar regularmente las plantas, especialmente los brotes nuevos
- Actuar rápidamente al detectar los primeros signos de infestación

Manejo integrado:
- Combinar varios métodos para un control más efectivo y sostenible
"""
        }

        # Crear texto informativo sobre las plagas detectadas
        info_text = ""
        for result in results:
            boxes = result.boxes.xyxy.numpy()  # Coordenadas de las cajas en formato numpy array
            classes = result.boxes.cls.numpy()  # Clases de las predicciones en formato numpy array
            class_names = result.names  # Nombres de las clases

            for cls in classes:
                cls_name = class_names[int(cls)] if int(cls) in class_names else "Desconocida"
                if cls_name in plagas_info:
                    info_text += f"{cls_name}:\n{plagas_info[cls_name]}\n\n"

        # Limpiar la información anterior
        info_text_var.set(info_text)

    def cargar_fotos():
        # Obtener los datos de la tabla TBFoto
        cur.execute('SELECT "PKIdFoto", "Ruta" FROM "Hidroponia"."TBFoto"')
        global fotos
        fotos = cur.fetchall()

        # Limpiar la lista de fotos
        listbox_fotos.delete(0, tk.END)

        # Agregar las fotos a la lista
        for foto in fotos:
            id_foto = foto[0]
            nombre_foto = os.path.basename(foto[1])  # Mostrar solo el nombre del archivo
            listbox_fotos.insert(tk.END, f"{id_foto} - {nombre_foto}")

        print("Fotos cargadas:", [foto[0] for foto in fotos])

    def seleccionar_foto(event):
        # Mostrar el índice de la foto seleccionada en la etiqueta de resultado
        index = listbox_fotos.curselection()
        if index:
            resultado_label.config(text=f"Índice seleccionado: {index[0]}")

    # Crear un marco con scroll
    scroll_frame = tk.Frame(root)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    # Crear un canvas y una scrollbar
    canvas = tk.Canvas(scroll_frame)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configurar el canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Empaquetar scrollbar y canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Configurar el frame que contendrá todos los widgets
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Sección para seleccionar la imagen (alineada a la derecha)
    selection_frame = tk.Frame(scrollable_frame)
    selection_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    label_fotos = tk.Label(selection_frame, text="Selecciona una imagen:")
    label_fotos.pack()

    listbox_fotos = tk.Listbox(selection_frame, width=50)
    listbox_fotos.pack()

    # Vincular la función seleccionar_foto al evento de selección de la lista
    listbox_fotos.bind("<<ListboxSelect>>", seleccionar_foto)

    # Cargar las fotos inicialmente
    cargar_fotos()

    # Botón para analizar la imagen
    analizar_boton = tk.Button(selection_frame, text="Analizar Imagen", command=analizar_imagen, pady=10)
    analizar_boton.pack(pady=10)

    # Etiqueta para mostrar la imagen
    global resultado_label
    resultado_label = tk.Label(selection_frame)
    resultado_label.pack(pady=10)

    # Frame para la información de la plaga
    info_frame = tk.Frame(scrollable_frame)
    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Etiqueta para mostrar la información
    global info_text_var
    info_text_var = tk.StringVar()
    info_label = tk.Label(info_frame, textvariable=info_text_var, justify=tk.LEFT, wraplength=400)
    info_label.pack(fill=tk.BOTH, expand=True)

    # Devolver el cursor y la conexión para que la aplicación principal pueda cerrarlos
    return cur, conn
