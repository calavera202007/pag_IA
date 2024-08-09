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
        database="Lestoma"
    )
    cur = conn.cursor()

    # Función para obtener los datos de la tabla TBLechuga
    def get_data():
        cur.execute("""
            SELECT L."PKIdLechuga", S."Tip_siembra", L."Ubicacion", T."TipoLechuga", D."AF", D."H", D."Semana", 
            D."Num_cosecha", D."Observaciones", F."Nombre", F."Ruta", F."Descripcion"
            FROM "Hidroponia"."TBLechuga" L
            JOIN "Hidroponia"."TBTipoSiembra" S ON L."FKIdTipSiembra" = S."PKIdTipSiembra"
            JOIN "Hidroponia"."TBTipoLechuga" T ON L."FKIdTipoLechuga" = T."PKIdTipoLechuga"
            JOIN "Hidroponia"."TBDatos" D ON L."PKIdLechuga" = D."FKIdLechuga"
            LEFT JOIN "Hidroponia"."TBFoto" F ON D."PKIdDatos" = F."PKIdFoto"
        """)
        data = cur.fetchall()
        print(data)  # Agrega esta línea para depurar
        return data

    # Función para mostrar los datos en la tabla
    def show_data():
        data = get_data()
        for row in tabla.get_children():
            tabla.delete(row)
        for record in data:
            tabla.insert("", "end", values=record)

    # Función para ver los detalles de un registro
    def ver_detalles(event=None):
        try:
            item_selected = tabla.selection()[0]
            data = tabla.item(item_selected, "values")
            messagebox.showinfo("Detalles del Registro",
                                f"ID: {data[0]}\nTipo de Siembra: {data[1]}\nUbicación: {data[2]}"
                                f"\nTipo de Lechuga: {data[3]}\nÁrea Foliar: {data[4]}"
                                f"\nAltura: {data[5]}\nSemana: {data[6]}\nNúmero de Siembra: {data[7]}"
                                f"\nObservaciones: {data[8]}\nNombre Foto: {data[9]}"
                                f"\nRuta Foto: {data[10]}\nDescripción Foto: {data[11]}")
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro primero.")

    # Función para ver los detalles de un registro
    def ver_detalles(event=None):
        try:
            item_selected = tabla.selection()[0]
            data = tabla.item(item_selected, "values")
            messagebox.showinfo("Detalles del Registro",
                                f"ID: {data[0]}\nTipo de Siembra: {data[1]}\nUbicación: {data[2]}"
                                f"\nTipo de Lechuga: {data[3]}\nÁrea Foliar: {data[4]}"
                                f"\nAltura: {data[5]}\nSemana: {data[6]}\nNúmero de Siembra: {data[7]}"
                                f"\nObservaciones: {data[8]}\nNombre Foto: {data[9]}"
                                f"\nRuta Foto: {data[10]}\nDescripción Foto: {data[11]}")
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro primero.")
    # Función para eliminar un registro
    def eliminar_registro():
        item_selected = tabla.selection()[0]
        lechuga_id = tabla.item(item_selected, "values")[0]
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")
        if confirm:
            cur.execute('DELETE FROM "Hidroponia"."TBLechuga" WHERE "PKIdLechuga" = %s', (lechuga_id,))
            conn.commit()
            show_data()

    # Función para actualizar un registro
    def actualizar_registro():
        item_selected = tabla.selection()[0]
        lechuga_id = tabla.item(item_selected, "values")[0]
        data = tabla.item(item_selected, "values")

        # Solicitar nueva información
        new_af = simpledialog.askstring("Actualizar Registro", "Nueva Área Foliar (cm2):", parent=root,
                                        initialvalue=data[4])
        new_h = simpledialog.askstring("Actualizar Registro", "Nueva Altura (cm):", parent=root, initialvalue=data[5])
        new_semana = simpledialog.askstring("Actualizar Registro", "Nueva Semana:", parent=root, initialvalue=data[6])
        new_num_cosecha = simpledialog.askstring("Actualizar Registro", "Nuevo Número de Siembra:", parent=root,
                                                 initialvalue=data[7])
        new_observaciones = simpledialog.askstring("Actualizar Registro", "Nuevas Observaciones:", parent=root,
                                                   initialvalue=data[8])

        if new_af and new_h and new_semana and new_num_cosecha and new_observaciones:
            cur.execute("""
                UPDATE "Hidroponia"."TBDatos"
                SET "AF" = %s, "H" = %s, "Semana" = %s, "Num_cosecha" = %s, "Observaciones" = %s
                WHERE "FKIdLechuga" = %s
            """, (new_af, new_h, new_semana, new_num_cosecha, new_observaciones, lechuga_id))
            conn.commit()
            show_data()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Función para generar el reporte en PDF
    def generar_reporte():
        data = get_data()
        doc = SimpleDocTemplate("Reporte_Lestoma.pdf", pagesize=letter)
        elements = []

        # Agregar encabezado
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Lestoma - " + datetime.datetime.now().strftime("%Y-%m-%d"), styles["Heading1"])
        elements.append(header)

        table_data = [["ID", "Tipo de Siembra", "Ubicación", "Tipo de Lechuga", "Área Foliar", "Altura", "Semana",
                       "Número de Siembra", "Observaciones", "Nombre Foto", "Ruta Foto", "Descripción Foto"]]
        for record in data:
            table_data.append(record)

        table = Table(table_data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)
        elements.append(table)
        doc.build(elements)
        messagebox.showinfo("Reporte generado", "El reporte en PDF se ha generado exitosamente.")

    # Crear la tabla con estilos personalizados
    style = ttk.Style()
    style.configure("Treeview",
                    background="lightblue",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="lightblue")
    style.map("Treeview", background=[('selected', 'blue')])

    tabla = ttk.Treeview(root, style="Treeview")
    tabla["columns"] = (
        "id", "siembra", "ubicacion", "lechuga", "af", "h", "semana", "num_cosecha", "observaciones", "nombre_foto",
        "ruta_foto", "descripcion_foto"
    )

    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("id", width=40, anchor="center")
    tabla.column("siembra", width=120, anchor="w")
    tabla.column("ubicacion", width=80, anchor="w")
    tabla.column("lechuga", width=120, anchor="w")
    tabla.column("af", width=80, anchor="center")
    tabla.column("h", width=80, anchor="center")
    tabla.column("semana", width=80, anchor="center")
    tabla.column("num_cosecha", width=120, anchor="center")
    tabla.column("observaciones", width=150, anchor="w")
    tabla.column("nombre_foto", width=120, anchor="w")
    tabla.column("ruta_foto", width=150, anchor="w")
    tabla.column("descripcion_foto", width=100, anchor="w")

    tabla.heading("id", text="ID", anchor="center")
    tabla.heading("siembra", text="Tipo de Siembra", anchor="w")
    tabla.heading("ubicacion", text="Ubicación", anchor="w")
    tabla.heading("lechuga", text="Tipo de Lechuga", anchor="w")
    tabla.heading("af", text="Área Foliar (cm2)", anchor="center")
    tabla.heading("h", text="Altura (cm)", anchor="center")
    tabla.heading("semana", text="Semana", anchor="center")
    tabla.heading("num_cosecha", text="Número de Siembra", anchor="center")
    tabla.heading("observaciones", text="Observaciones", anchor="w")
    tabla.heading("nombre_foto", text="Nombre Foto", anchor="w")
    tabla.heading("ruta_foto", text="Ruta Foto", anchor="w")
    tabla.heading("descripcion_foto", text="Descripción Foto", anchor="w")

    tabla.pack(pady=18, padx=18, fill=tk.BOTH, expand=True)
    tabla.bind("<Double-1>", ver_detalles)

    # Botones con estilos ttk
    boton_detalles = ttk.Button(root, text="Ver Detalles", command=ver_detalles)
    boton_detalles.pack(pady=5)

    boton_eliminar = ttk.Button(root, text="Eliminar", command=eliminar_registro)
    boton_eliminar.pack(pady=5)

    boton_actualizar = ttk.Button(root, text="Actualizar", command=actualizar_registro)
    boton_actualizar.pack(pady=5)

    boton_reporte = ttk.Button(root, text="Generar Reporte", command=generar_reporte)
    boton_reporte.pack(pady=10)

    # Mostrar los datos inicialmente
    show_data()

    # Ejecutar la interfaz
    root.mainloop()

    # Cerrar la conexión con PostgreSQL
    cur.close()
    conn.close()


