import os
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from PIL import Image, ImageTk
import io

def main(root):
    # Inicializar el modelo YOLO
    model = YOLO('models/best.pt')

    # Establecer la conexión con PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="Yamile25",
        host="localhost",
        port="5432",
        database="meme"
    )
    cur = conn.cursor()

    def analizar_imagen():
        # Obtener el ID de la imagen seleccionada
        meme_id_str = meme_seleccionado.get()

        # Verificar si el ID del meme está vacío
        if meme_id_str.strip() == "":
            messagebox.showerror("Error", "Por favor selecciona un meme antes de analizar la imagen.")
            return

        meme_id = int(meme_id_str)

        # Obtener la ruta de la imagen de la base de datos
        cur.execute("SELECT image FROM meme WHERE id = %s", (meme_id,))
        imagen_path = cur.fetchone()[0]

        # Cargar la imagen desde la ruta
        image = cv2.imread(imagen_path)

        # Predecir utilizando el modelo YOLO en la imagen
        results = model.predict(image, imgsz=640, conf=0.4)

        # Verificar si se han detectado herramientas en la imagen
        if len(results) != 0:
            for res in results:
                print(f'Herramientas detectadas en la imagen {meme_id}')

            # Obtener la imagen con las herramientas detectadas
            annotated_image = results[0].plot()

            # Redimensionar la imagen a 640x640 píxeles
            annotated_image = cv2.resize(annotated_image, (350, 350))

            # Mostrar la imagen con las herramientas detectadas
            cv2_img = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_img)
            img_tk = ImageTk.PhotoImage(image=img)
            resultado_label.configure(image=img_tk)
            resultado_label.image = img_tk
        else:
            print(f'No se detectaron herramientas en la imagen {meme_id}')
            resultado_label.configure(image=None)
            resultado_label.image = None

    def cargar_memes():
        # Obtener los datos de la tabla meme
        cur.execute("SELECT id, title FROM meme")
        memes = cur.fetchall()

        # Limpiar la lista de memes
        listbox_memes.delete(0, tk.END)

        # Agregar los memes a la lista
        for meme in memes:
            listbox_memes.insert(tk.END, f"{meme[0]} - {meme[1]}")

    def seleccionar_meme(event):
        # Obtener el índice del meme seleccionado
        index = listbox_memes.curselection()
        if index:
            # Obtener el texto del meme seleccionado
            selected_text = listbox_memes.get(index)
            # Obtener solo el ID del meme (antes del primer '-')
            meme_id_str = selected_text.split('-')[0].strip()
            # Actualizar meme_seleccionado
            meme_seleccionado.set(meme_id_str)

    # Sección para seleccionar la imagen
    label_memes = tk.Label(root, text="Selecciona una imagen:")
    label_memes.pack()

    listbox_memes = tk.Listbox(root, width=50)
    listbox_memes.pack()

    # Vincular la función seleccionar_meme al evento de selección de la lista
    listbox_memes.bind("<<ListboxSelect>>", seleccionar_meme)

    # Cargar los memes inicialmente
    cargar_memes()

    # Variable para almacenar el ID del meme seleccionado
    meme_seleccionado = tk.StringVar()

    # Botón para analizar la imagen
    analizar_boton = tk.Button(root, text="Analizar Imagen", command=analizar_imagen)
    analizar_boton.pack()

    # Etiqueta para mostrar el resultado
    resultado_label = tk.Label(root)
    resultado_label.pack()

    # Devolver el cursor y la conexión para que la aplicación principal pueda cerrarlos
    return cur, conn
