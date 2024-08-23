import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import psycopg2
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import os
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
    def get_data(semana=None, num_cosecha=None, ubicacion=None, tipo_lechuga=None, tipo_siembra=None):
        query = """
            SELECT L."PKIdLechuga", S."Tip_siembra", L."Ubicacion", T."TipoLechuga", D."AF", D."H", D."Semana", 
            D."Num_cosecha", D."Observaciones", F."Nombre", F."Ruta", F."Descripcion"
            FROM "Hidroponia"."TBLechuga" L
            JOIN "Hidroponia"."TBTipoSiembra" S ON L."FKIdTipSiembra" = S."PKIdTipSiembra"
            JOIN "Hidroponia"."TBTipoLechuga" T ON L."FKIdTipoLechuga" = T."PKIdTipoLechuga"
            JOIN "Hidroponia"."TBDatos" D ON L."PKIdLechuga" = D."FKIdLechuga"
            LEFT JOIN "Hidroponia"."TBReporte" R ON D."PKIdDatos" = R."FKIdDatos"
            LEFT JOIN "Hidroponia"."TBFoto" F ON R."FKIdFoto" = F."PKIdFoto"
            WHERE (%s IS NULL OR D."Semana" = %s)
              AND (%s IS NULL OR D."Num_cosecha" = %s)
              AND (%s IS NULL OR L."Ubicacion" = %s)
              AND (%s IS NULL OR T."TipoLechuga" = %s)
              AND (%s IS NULL OR S."Tip_siembra" = %s)
        """

        # Reemplaza las cadenas vacías con None
        params = (
            None if semana == '' else semana,
            None if semana == '' else semana,
            None if num_cosecha == '' else num_cosecha,
            None if num_cosecha == '' else num_cosecha,
            None if ubicacion == '' else ubicacion,
            None if ubicacion == '' else ubicacion,
            None if tipo_lechuga == '' else tipo_lechuga,
            None if tipo_lechuga == '' else tipo_lechuga,
            None if tipo_siembra == '' else tipo_siembra,
            None if tipo_siembra == '' else tipo_siembra
        )

        cur.execute(query, params)
        data = cur.fetchall()
        return data

    # Función para mostrar los datos en la tabla
    def show_data(semana=None, num_cosecha=None, ubicacion=None, tipo_lechuga=None, tipo_siembra=None):
        data = get_data(semana, num_cosecha, ubicacion, tipo_lechuga, tipo_siembra)
        for row in tabla.get_children():
            tabla.delete(row)
        for record in data:
            record = tuple('-' if v is None or v == '' else v for v in record)
            tabla.insert("", "end", values=record)

    # Función para ver los detalles de un registro
    def ver_detalles(event=None):
        try:
            item_selected = tabla.selection()[0]
            data = tabla.item(item_selected, "values")
            data = tuple('-' if v == '' else v for v in data)
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
        try:
            item_selected = tabla.selection()[0]
            lechuga_id = tabla.item(item_selected, "values")[0]
            confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")
            if confirm:
                # Obtener el ID de "TBDatos" relacionado
                cur.execute('SELECT "PKIdDatos" FROM "Hidroponia"."TBDatos" WHERE "FKIdLechuga" = %s', (lechuga_id,))
                datos_ids = cur.fetchall()

                # Eliminar registros en "TBReporte"
                for datos_id in datos_ids:
                    cur.execute('DELETE FROM "Hidroponia"."TBReporte" WHERE "FKIdDatos" = %s', (datos_id,))
                    conn.commit()
                    print(f"Registros eliminados en TBReporte para FKIdDatos={datos_id}")  # Depuración

                # Eliminar registros en "TBDatos"
                cur.execute('DELETE FROM "Hidroponia"."TBDatos" WHERE "FKIdLechuga" = %s', (lechuga_id,))
                conn.commit()
                print(f"Registros eliminados en TBDatos para FKIdLechuga={lechuga_id}")  # Depuración

                # Finalmente, eliminar el registro en "TBLechuga"
                cur.execute('DELETE FROM "Hidroponia"."TBLechuga" WHERE "PKIdLechuga" = %s', (lechuga_id,))
                conn.commit()
                print(f"Registro eliminado en TBLechuga para PKIdLechuga={lechuga_id}")  # Depuración

                show_data()
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro primero.")

    # Función para actualizar un registro
    def actualizar_registro():
        try:
            item_selected = tabla.selection()[0]
            lechuga_id = tabla.item(item_selected, "values")[0]
            data = tabla.item(item_selected, "values")

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
        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro primero.")

    # Función para generar el reporte en PDF
    def generar_reporte():
        semana = filtro_semana.get()
        num_cosecha = filtro_num_cosecha.get()
        ubicacion = filtro_ubicacion.get()
        tipo_lechuga = filtro_tipo_lechuga.get()
        tipo_siembra = filtro_tipo_siembra.get()

        data = get_data(semana, num_cosecha, ubicacion, tipo_lechuga, tipo_siembra)

        doc = SimpleDocTemplate("Reporte_Lestoma.pdf", pagesize=letter)
        elements = []

        # Agregar encabezado con imágenes
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Lestoma - " + datetime.datetime.now().strftime("%Y-%m-%d"), styles["Heading1"])

        logo_izq = Image(os.path.join("images", "logo.png"), width=60, height=60)
        logo_der = Image(os.path.join("images", "lestoma.png"), width=60, height=60)

        header_table = Table([[logo_izq, header, logo_der]], colWidths=[60, 400, 60])
        header_table.setStyle(TableStyle([('ALIGN', (1, 0), (1, 0), 'CENTER')]))

        elements.append(header_table)

        # Crear los datos de la tabla
        table_data = [["ID", "Tipo de Siembra", "Ubicación", "Tipo de Lechuga", "Área Foliar", "Altura", "Semana",
                       "Número de Siembra", "Observaciones"]]

        for record in data:
            record = tuple('-' if v is None or v == '' else v for v in record)
            row = [record[0][:3] + '..'] + list(record[1:8]) + [record[8]]
            table_data.append(row)

        # Crear y ajustar la tabla
        table = Table(table_data, colWidths=[30, 70, 60, 70, 45, 45, 35, 70, 80])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),  # Reducir el tamaño de la fuente del encabezado
            ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reducir el tamaño de la fuente de los datos
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK')  # Habilitar ajuste de texto
        ])
        table.setStyle(style)

        # Ajustar la longitud de las celdas para que el texto se ajuste dentro
        for row_num, row in enumerate(table_data):
            for col_num, cell in enumerate(row):
                table._argW[col_num] = max(table._argW[col_num], len(str(cell)) * 4)  # Ajustar según el contenido

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

    # Crear el frame de filtros
    frame_filtros = ttk.Frame(root)
    frame_filtros.pack(pady=10, padx=10, fill=tk.X)

    # Filtros
    ttk.Label(frame_filtros, text="Semana:").grid(row=0, column=0, padx=5, pady=5)
    filtro_semana = tk.StringVar()
    ttk.Entry(frame_filtros, textvariable=filtro_semana).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_filtros, text="Número de Cosecha:").grid(row=1, column=0, padx=5, pady=5)
    filtro_num_cosecha = tk.StringVar()
    ttk.Entry(frame_filtros, textvariable=filtro_num_cosecha).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_filtros, text="Ubicación:").grid(row=2, column=0, padx=5, pady=5)
    filtro_ubicacion = tk.StringVar()
    ttk.Entry(frame_filtros, textvariable=filtro_ubicacion).grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_filtros, text="Tipo de Lechuga:").grid(row=3, column=0, padx=5, pady=5)
    filtro_tipo_lechuga = tk.StringVar()
    ttk.Entry(frame_filtros, textvariable=filtro_tipo_lechuga).grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_filtros, text="Tipo de Siembra:").grid(row=4, column=0, padx=5, pady=5)
    filtro_tipo_siembra = tk.StringVar()
    ttk.Entry(frame_filtros, textvariable=filtro_tipo_siembra).grid(row=4, column=1, padx=5, pady=5)

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


