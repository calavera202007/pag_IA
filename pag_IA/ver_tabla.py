import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import psycopg2
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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
    def get_data(semana=None, num_cosecha=None, ubicacion=None, tipo_lechuga=None, tipo_siembra=None, planta=None):
        query = """
            SELECT L."PKIdLechuga", S."Tip_siembra", L."Ubicacion", L."Planta", T."TipoLechuga", D."NumHojas", D."AF", D."H", D."Semana", 
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
              AND (%s IS NULL OR L."Planta" = %s)
        """

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
            None if tipo_siembra == '' else tipo_siembra,
            None if planta == '' else planta,
            None if planta == '' else planta
        )

        cur.execute(query, params)
        data = cur.fetchall()
        return data

    # Función para mostrar los datos en la tabla
    def show_data(semana=None, num_cosecha=None, ubicacion=None, tipo_lechuga=None, tipo_siembra=None, planta=None):
        data = get_data(semana, num_cosecha, ubicacion, tipo_lechuga, tipo_siembra, planta)
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
            new_num_h = simpledialog.askstring("Actualizar Registro", "Numero de hojas", parent=root,
                                            initialvalue=data[5])
            new_af = simpledialog.askstring("Actualizar Registro", "Nueva Área Foliar (cm2):", parent=root,
                                            initialvalue=data[6])
            new_h = simpledialog.askstring("Actualizar Registro", "Nueva Altura (cm):", parent=root, initialvalue=data[7])
            new_semana = simpledialog.askstring("Actualizar Registro", "Nueva Semana:", parent=root, initialvalue=data[8])
            new_num_cosecha = simpledialog.askstring("Actualizar Registro", "Nuevo Número de Siembra:", parent=root,
                                                     initialvalue=data[9])
            new_observaciones = simpledialog.askstring("Actualizar Registro", "Nuevas Observaciones:", parent=root,
                                                       initialvalue=data[10])

            if new_af and new_h and new_semana and new_num_cosecha and new_observaciones:
                cur.execute("""
                    UPDATE "Hidroponia"."TBDatos"
                    SET "NumHojas" = %s, "AF" = %s, "H" = %s, "Semana" = %s, "Num_cosecha" = %s, "Observaciones" = %s
                    WHERE "FKIdLechuga" = %s
                """, (new_num_h,new_af, new_h, new_semana, new_num_cosecha, new_observaciones, lechuga_id))
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
        planta = filtro_planta.get()

        data = get_data(semana, num_cosecha, ubicacion, tipo_lechuga, tipo_siembra, planta)

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
        table_data = [
            ["ID", "Tipo_Siembra", "Ubicación", "Planta", "Tipo_Lechuga", "Num_H", "Área_Foliar", "Altura", "Semana",
             "Número de Siembra", "Observaciones"]]

        for record in data:
            record = tuple('-' if v is None or v == '' else v for v in record)
            row = [record[0][:3] + '..'] + list(record[1:8]) + [record[8], record[
                9], record[10]]  # Asegurarse de incluir las columnas "Número de Siembra" y "Observaciones"
            table_data.append(row)

        # Crear y ajustar la tabla
        col_widths = [25, 50, 45, 50, 40, 40, 30, 50, 60, 80,
                      100]  # Aumentar el ancho para "Número de Siembra" y "Observaciones"
        table = Table(table_data, colWidths=col_widths)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),  # Reducir el tamaño de la fuente del encabezado
            ('FONTSIZE', (0, 1), (-1, -1), 6),  # Reducir el tamaño de la fuente de los datos
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK')  # Habilitar ajuste de texto
        ])
        table.setStyle(style)

        elements.append(table)
        doc.build(elements)
        messagebox.showinfo("Reporte generado", "El reporte en PDF se ha generado exitosamente.")

    # Nueva función para generar un reporte en Excel
    def generar_reporte_excel():
        # Obtener los valores de los filtros
        semana = filtro_semana.get()
        num_cosecha = filtro_num_cosecha.get()
        ubicacion = filtro_ubicacion.get()
        tipo_lechuga = filtro_tipo_lechuga.get()
        tipo_siembra = filtro_tipo_siembra.get()
        planta = filtro_planta.get()

        # Obtener los datos filtrados
        data = get_data(semana, num_cosecha, ubicacion, tipo_lechuga, tipo_siembra, planta)

        # Crear un nuevo libro de Excel
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Reporte Lestoma"

        # Definir los encabezados sin las columnas de fotos
        headers = ["ID", "Tipo de Siembra", "Ubicación", "Planta", "Tipo de Lechuga", "Num H", "AF", "H", "Semana", "Nº Siembra",
                   "Observaciones"]
        sheet.append(headers)

        # Añadir los datos a la hoja, excluyendo las columnas de fotos
        for record in data:
            # Excluir las últimas tres columnas (asumiendo que estas son las columnas de fotos)
            filtered_record = record[:-3]  # Esto elimina los últimos 3 elementos de cada tupla
            sheet.append(list(filtered_record))

        # Formatear los encabezados
        for cell in sheet["1:1"]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        # Guardar el archivo Excel
        file_path = "Reporte_Lestoma.xlsx"
        workbook.save(file_path)

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Reporte Generado", f"El reporte en Excel ha sido generado y guardado como {file_path}")

    # Interfaz Gráfica
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Semana:").grid(row=0, column=0, padx=5, pady=5)
    filtro_semana = ttk.Entry(frame)
    filtro_semana.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Nº Cosecha:").grid(row=0, column=2, padx=5, pady=5)
    filtro_num_cosecha = ttk.Entry(frame)
    filtro_num_cosecha.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame, text="Ubicación:").grid(row=1, column=0, padx=5, pady=5)
    filtro_ubicacion = ttk.Entry(frame)
    filtro_ubicacion.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Tipo de Lechuga:").grid(row=1, column=2, padx=5, pady=5)
    filtro_tipo_lechuga = ttk.Entry(frame)
    filtro_tipo_lechuga.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame, text="Tipo de Siembra:").grid(row=2, column=0, padx=5, pady=5)
    filtro_tipo_siembra = ttk.Entry(frame)
    filtro_tipo_siembra.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Numero planta:").grid(row=2, column=2, padx=5, pady=5)
    filtro_planta = ttk.Entry(frame)
    filtro_planta.grid(row=2, column=3, padx=5, pady=5)

    frame_buscar = tk.Frame(root)
    frame_buscar.pack(pady=10)
    boton_buscar = ttk.Button(frame_buscar, text="Buscar", command=lambda: show_data(
        filtro_semana.get(),
        filtro_num_cosecha.get(),
        filtro_ubicacion.get(),
        filtro_tipo_lechuga.get(),
        filtro_tipo_siembra.get(),
        filtro_planta.get()
    ))
    boton_buscar.pack(pady=10)

    columns = ("ID", "Tipo de Siembra", "Ubicación", "Planta", "Tipo de Lechuga", "Num h", "AF", "H", "Semana", "Nº Siembra", "Observaciones", "Foto Nombre", "Foto Ruta", "Foto Descripción")
    tabla = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tabla.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    for col in columns:
        tabla.heading(col, text=col)
        tabla.column(col, minwidth=0, width=70)

    tabla.bind("<Double-1>", ver_detalles)

    frame_botones = tk.Frame(root)
    frame_botones.pack(padx=10, pady=10)

    boton_eliminar = ttk.Button(frame_botones, text="Eliminar", command=eliminar_registro)
    boton_eliminar.grid(row=0, column=0, padx=5, pady=5)

    boton_actualizar = ttk.Button(frame_botones, text="Actualizar", command=actualizar_registro)
    boton_actualizar.grid(row=0, column=1, padx=5, pady=5)

    boton_reporte = ttk.Button(frame_botones, text="Generar Reporte PDF", command=generar_reporte)
    boton_reporte.grid(row=0, column=2, padx=5, pady=5)

    boton_reporte_excel = ttk.Button(frame_botones, text="Generar Reporte Excel", command=generar_reporte_excel)
    boton_reporte_excel.grid(row=0, column=3, padx=5, pady=5)

    show_data()