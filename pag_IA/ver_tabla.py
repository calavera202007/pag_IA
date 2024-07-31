import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import psycopg2
import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def main(root):
    # Establecer la conexión con PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="Yamile25",
        host="localhost",
        port="5432",
        database="meme"
    )
    cur = conn.cursor()

    # Carpeta de destino para guardar las imágenes
    img_folder = "imagenes"
    os.makedirs(img_folder, exist_ok=True)  # Crear la carpeta si no existe

    # Función para obtener los datos de la tabla meme
    def get_memes():
        cur.execute("SELECT * FROM meme")
        return cur.fetchall()

    # Función para mostrar los memes en la tabla
    def show_memes():
        memes = get_memes()
        for row in tabla.get_children():
            tabla.delete(row)
        for meme in memes:
            tabla.insert("", "end", values=meme)

    # Función para agregar un nuevo meme
    def agregar_meme():
        description = simpledialog.askstring("Agregar Meme", "Descripción:", parent=root)
        image_path = filedialog.askopenfilename(title="Seleccionar imagen", initialdir="/", filetypes=[("Image files", "*.jpg *.png")])
        title = simpledialog.askstring("Agregar Meme", "Título:", parent=root)
        if description and image_path and title:
            # Copiar la imagen a la carpeta de destino
            img_filename = os.path.basename(image_path)
            dest_path = os.path.join(img_folder, img_filename)
            shutil.copy(image_path, dest_path)

            # Insertar los datos en la tabla meme
            cur.execute("INSERT INTO meme (description, image, title) VALUES (%s, %s, %s)", (description, dest_path, title))
            conn.commit()
            show_memes()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Función para ver los detalles de un meme
    def ver_detalles(event):
        item_selected = tabla.selection()[0]
        meme_data = tabla.item(item_selected, "values")
        messagebox.showinfo("Detalles del Meme", f"ID: {meme_data[0]}\nDescripción: {meme_data[1]}\nImagen: {meme_data[2]}\nTítulo: {meme_data[3]}")

    # Función para eliminar un meme
    def eliminar_meme():
        item_selected = tabla.selection()[0]
        meme_id = tabla.item(item_selected, "values")[0]
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este meme?")
        if confirm:
            cur.execute("DELETE FROM meme WHERE id = %s", (meme_id,))
            conn.commit()
            show_memes()

    # Función para actualizar un meme
    def actualizar_meme():
        item_selected = tabla.selection()[0]
        meme_id = tabla.item(item_selected, "values")[0]
        meme_data = tabla.item(item_selected, "values")
        new_description = simpledialog.askstring("Actualizar Meme", "Nueva descripción:", parent=root, initialvalue=meme_data[1])
        new_image_path = filedialog.askopenfilename(title="Seleccionar nueva imagen", initialdir="/", filetypes=[("Image files", "*.jpg *.png")])
        new_title = simpledialog.askstring("Actualizar Meme", "Nuevo título:", parent=root, initialvalue=meme_data[3])

        if new_description and new_image_path and new_title:
            # Copiar la nueva imagen a la carpeta de destino
            img_filename = os.path.basename(new_image_path)
            dest_path = os.path.join(img_folder, img_filename)
            shutil.copy(new_image_path, dest_path)

            # Actualizar los datos en la tabla meme
            cur.execute("UPDATE meme SET description = %s, image = %s, title = %s WHERE id = %s", (new_description, dest_path, new_title, meme_id))
            conn.commit()
            show_memes()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Función para generar el reporte en PDF
    def generar_reporte():
        memes = get_memes()
        doc = SimpleDocTemplate("Reporte plantas.pdf", pagesize=letter)
        elements = []

        # Agregar encabezado
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte laboratorio lestoma - " + datetime.datetime.now().strftime("%Y-%m-%d"), styles["Heading1"])
        elements.append(header)

        data = [["ID", "Descripción", "Imagen", "Título"]]
        for meme in memes:
            data.append(meme)
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                           ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0,0), (-1,0), 12),
                           ('GRID', (0,0), (-1,-1), 1, colors.black)])
        table.setStyle(style)
        elements.append(table)
        doc.build(elements)
        messagebox.showinfo("Reporte generado", "El reporte en PDF se ha generado exitosamente.")

    # Crear la tabla con estilos personalizados
    style = ttk.Style()
    style.configure("Treeview",
                    background="lightgreen",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="lightgreen")
    style.map("Treeview", background=[('selected', 'green')])

    tabla = ttk.Treeview(root, style="Treeview")
    tabla["columns"] = ("id", "description", "image", "title")
    tabla.column("#0", width=50, anchor="center")
    tabla.column("id", width=50, anchor="center")
    tabla.column("description", width=200, anchor="w")
    tabla.column("image", width=200, anchor="w")
    tabla.column("title", width=200, anchor="w")

    tabla.heading("#0", text="ID", anchor="center")
    tabla.heading("id", text="ID", anchor="center")
    tabla.heading("description", text="Descripción", anchor="w")
    tabla.heading("image", text="Imagen", anchor="w")
    tabla.heading("title", text="Título", anchor="w")

    tabla.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Botones con estilos ttk
    boton_agregar = ttk.Button(root, text="Agregar", command=agregar_meme)
    boton_agregar.pack(pady=5)

    boton_detalles = ttk.Button(root, text="Ver Detalles", command=lambda: tabla.bind("<Double-1>", ver_detalles))
    boton_detalles.pack(pady=5)

    boton_eliminar = ttk.Button(root, text="Eliminar", command=eliminar_meme)
    boton_eliminar.pack(pady=5)

    boton_actualizar = ttk.Button(root, text="Actualizar", command=actualizar_meme)
    boton_actualizar.pack(pady=5)

    boton_reporte = ttk.Button(root, text="Generar Reporte", command=generar_reporte)
    boton_reporte.pack(pady=10)

    # Mostrar los memes inicialmente
    show_memes()

    # Ejecutar la interfaz
    root.mainloop()

    # Cerrar la conexión con PostgreSQL
    cur.close()
    conn.close()

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestor de Memes")
    root.geometry("800x600")
    style = ttk.Style(root)
    style.theme_use('clam')  # Puedes probar otros temas: 'default', 'classic', 'clam', 'alt', 'vista', 'xpnative'
    main(root)
