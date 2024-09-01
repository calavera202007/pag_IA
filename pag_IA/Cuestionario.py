import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import uuid
import os
import shutil
import psycopg2
import pandas as pd

def download_template():
    try:
        # Definir la ruta de la plantilla
        template_path = os.path.join('models', 'Plantilla_Lestoma.xlsx')

        # Verificar si la plantilla existe
        if not os.path.exists(template_path):
            messagebox.showerror("Error", "No se encontró la plantilla.")
            return

        # Dialogo para seleccionar la ubicación de guardado
        save_path = filedialog.asksaveasfilename(
            title="Guardar formato",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")],
            initialfile="Plantilla_Lestoma.xlsx"
        )

        # Copiar la plantilla a la ubicación seleccionada
        if save_path:
            shutil.copy(template_path, save_path)
            messagebox.showinfo("Éxito", "Formato descargado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar el formato: {str(e)}")


def upload_excel():
    filepath = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx;*.xls")]
    )

    if filepath:
        try:
            # Leer el archivo Excel
            df = pd.read_excel(filepath)

            # Verificar el número de registros
            if len(df) > 100:
                messagebox.showerror("Error", "El archivo Excel no debe contener más de 100 registros.")
                return

            # Reemplazar comas por puntos para asegurar la correcta conversión a float
            df = df.replace({',': '.'}, regex=True)

            # Iterar sobre cada fila y guardar los datos en la base de datos
            for index, row in df.iterrows():
                siembra = row['Tipo de Siembra']
                ubicacion = row['Ubicación']
                lechuga = row['Tipo de Lechuga']
                planta = row['Planta']
                num_h = row['NumHojas']
                af = row['AF']
                h = row['H']
                semana = row['Semana']
                num_cosecha = row['Nº Siembra']
                observaciones = row['Observaciones']

                # Validación de campos numéricos
                try:
                    af = float(af)
                    h = float(h)
                    semana = float(semana)
                    num_cosecha = float(num_cosecha)
                    planta = int(planta)
                    num_h = int(num_h)
                except ValueError:
                    messagebox.showerror(
                        "Error", f"Los campos AF, H, Semana, Número de Siembra, Planta y NumHojas deben ser números válidos en la fila {index + 1}."
                    )
                    return

                # Guardar datos en la base de datos
                save_data_to_db(siembra, ubicacion, lechuga, planta, num_h, af, h, semana, num_cosecha, observaciones)

            messagebox.showinfo("Éxito", "Datos cargados correctamente desde el archivo Excel.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo Excel: {str(e)}")


def save_data_to_db(siembra, ubicacion, lechuga, planta, num_h, af, h, semana, num_cosecha, observaciones):
    # Generar UUIDs
    id_tip_siembra = str(uuid.uuid4())
    id_tipo_lechuga = str(uuid.uuid4())
    id_lechuga = str(uuid.uuid4())
    id_datos = str(uuid.uuid4())

    # Conectar a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="Yamile25",
            host="localhost",
            port="5432",
            database="Lestoma"
        )
        cursor = conn.cursor()

        # Insertar en TBTipoSiembra
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBTipoSiembra" ("PKIdTipSiembra", "Tip_siembra")
        VALUES (%s, %s);
        """, (id_tip_siembra, siembra))

        # Insertar en TBTipoLechuga
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBTipoLechuga" ("PKIdTipoLechuga", "TipoLechuga")
        VALUES (%s, %s);
        """, (id_tipo_lechuga, lechuga))

        # Insertar en TBLechuga
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBLechuga" ("PKIdLechuga", "FKIdTipoLechuga", "FKIdTipSiembra", "Ubicacion", "Planta")
        VALUES (%s, %s, %s, %s, %s);
        """, (id_lechuga, id_tipo_lechuga, id_tip_siembra, ubicacion, planta))

        # Insertar en TBDatos
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBDatos" ("PKIdDatos", "AF", "H", "Semana", "Num_cosecha", "Observaciones", "FKIdLechuga", "NumHojas")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (id_datos, af, h, semana, num_cosecha, observaciones, id_lechuga, num_h))

        # Confirmar cambios
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e.pgcode} - {e.pgerror}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


def validate_numeric_input(new_value):
    if new_value == "" or new_value.replace(".", "", 1).isdigit():
        return True
    return False


def highlight_empty_fields(fields):
    for field in fields:
        if 'entry' in field and field['entry'] is not None:
            if not field['var'].get().strip():
                field['entry'].config(background='red')
            else:
                field['entry'].config(background='white')


def save_data():
    siembra = siembra_var.get().strip()
    ubicacion = ubicacion_var.get().strip()
    lechuga = lechuga_var.get().strip()
    planta = planta_entry.get().strip()
    num_h = num_h_entry.get().strip()
    af = af_entry.get().strip()
    h = h_entry.get().strip()
    semana = semana_entry.get().strip()
    num_cosecha = num_cosecha_entry.get().strip()
    observaciones = observaciones_entry.get().strip()
    nombre_foto = nombre_foto_entry.get().strip()
    ruta_foto = ruta_foto_entry.get().strip()
    descripcion_foto = descripcion_foto_entry.get().strip()

    # Validación de campos obligatorios
    mandatory_fields = [
        {'var': siembra_var, 'entry': None},
        {'var': ubicacion_var, 'entry': None},
        {'var': lechuga_var, 'entry': None},
        {'var': tk.StringVar(value=planta), 'entry': planta_entry},
        {'var': tk.StringVar(value=num_h), 'entry': num_h_entry},
        {'var': tk.StringVar(value=af), 'entry': af_entry},
        {'var': tk.StringVar(value=h), 'entry': h_entry},
        {'var': tk.StringVar(value=semana), 'entry': semana_entry},
        {'var': tk.StringVar(value=num_cosecha), 'entry': num_cosecha_entry}
    ]

    highlight_empty_fields(mandatory_fields)

    if not all([siembra, ubicacion, lechuga, planta, num_h, af, h, semana, num_cosecha]):
        messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
        return

    # Validación de campos numéricos
    try:
        af = float(af)
        h = float(h)
        semana = float(semana)
        num_cosecha = float(num_cosecha)
        planta = int(planta)
        num_h = int(num_h)
    except ValueError:
        messagebox.showerror("Error", "Los campos AF, H, Semana, Número de Siembra, Planta y NumHojas deben ser números válidos.")
        return

    # Generar UUIDs
    id_tip_siembra = str(uuid.uuid4())
    id_tipo_lechuga = str(uuid.uuid4())
    id_lechuga = str(uuid.uuid4())
    id_datos = str(uuid.uuid4())
    id_reporte = str(uuid.uuid4())
    id_foto = str(uuid.uuid4()) if nombre_foto else None

    try:
        conn = psycopg2.connect(
            user="postgres",
            password="Yamile25",
            host="localhost",
            port="5432",
            database="Lestoma"
        )
        cursor = conn.cursor()

        # Insertar en TBTipoSiembra
        cursor.execute("""
                INSERT INTO "Hidroponia"."TBTipoSiembra" ("PKIdTipSiembra", "Tip_siembra")
                VALUES (%s, %s);
            """, (id_tip_siembra, siembra))

        # Insertar en TBTipoLechuga
        cursor.execute("""
                INSERT INTO "Hidroponia"."TBTipoLechuga" ("PKIdTipoLechuga", "TipoLechuga")
                VALUES (%s, %s);
            """, (id_tipo_lechuga, lechuga))

        # Insertar en TBLechuga
        cursor.execute("""
                INSERT INTO "Hidroponia"."TBLechuga" ("PKIdLechuga", "FKIdTipoLechuga", "FKIdTipSiembra", "Ubicacion", "Planta")
                VALUES (%s, %s, %s, %s, %s);
            """, (id_lechuga, id_tipo_lechuga, id_tip_siembra, ubicacion, planta))

        # Insertar en TBFoto si se proporciona
        if nombre_foto:
            cursor.execute("""
                    INSERT INTO "Hidroponia"."TBFoto" ("PKIdFoto", "Nombre", "Ruta", "Descripcion")
                    VALUES (%s, %s, %s, %s);
                """, (id_foto, nombre_foto, ruta_foto, descripcion_foto))

        # Insertar en TBDatos
        cursor.execute("""
                INSERT INTO "Hidroponia"."TBDatos" ("PKIdDatos", "AF", "H", "Semana", "Num_cosecha", "Observaciones", "FKIdLechuga", "NumHojas")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (id_datos, af, h, semana, num_cosecha, observaciones, id_lechuga, num_h))

        # Insertar en TBReporte
        cursor.execute("""
                INSERT INTO "Hidroponia"."TBReporte" ("PKIdReporte", "FKIdDatos", "FKIdFoto")
                VALUES (%s, %s, %s);
            """, (id_reporte, id_datos, id_foto))

        conn.commit()
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        clear_fields()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e.pgcode} - {e.pgerror}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def clear_fields():
    siembra_var.set("Agua")
    ubicacion_var.set("L1")
    lechuga_var.set("V1")
    planta_entry.delete(0, tk.END)
    num_h_entry.delete(0, tk.END)
    af_entry.delete(0, tk.END)
    h_entry.delete(0, tk.END)
    semana_entry.delete(0, tk.END)
    num_cosecha_entry.delete(0, tk.END)
    observaciones_entry.delete(0, tk.END)
    nombre_foto_entry.delete(0, tk.END)
    ruta_foto_entry.delete(0, tk.END)
    descripcion_foto_entry.delete(0, tk.END)
    # Restablecer el color de fondo de los campos
    planta_entry.config(background='white')
    num_h_entry.config(background='white')
    af_entry.config(background='white')
    h_entry.config(background='white')
    semana_entry.config(background='white')
    num_cosecha_entry.config(background='white')


def select_image():
    filetypes = [("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    filepath = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=filetypes)

    if filepath:
        image_folder = "imagenes"
        os.makedirs(image_folder, exist_ok=True)

        # Generar un nombre único para la imagen
        image_name = os.path.basename(filepath)
        new_filepath = os.path.join(image_folder, image_name)

        # Copiar la imagen seleccionada a la carpeta "imagenes"
        shutil.copy(filepath, new_filepath)

        # Actualizar la entrada de ruta_foto con la nueva ruta
        ruta_foto_entry.delete(0, tk.END)
        ruta_foto_entry.insert(0, new_filepath)


def main(frame):
    global siembra_var, ubicacion_var, lechuga_var, planta_entry, num_h_entry, af_entry, h_entry, semana_entry, num_cosecha_entry
    global observaciones_entry, nombre_foto_entry, ruta_foto_entry, descripcion_foto_entry

    for widget in frame.winfo_children():
        widget.destroy()  # Limpiar widgets anteriores en el frame

    # Definir estilo para botones grandes
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 16), padding=10)

    container = ttk.Frame(frame, padding="20 20 20 20")
    container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    font_large = ("Helvetica", 18)

    # Registrar la función de validación numérica
    validate_cmd = frame.register(validate_numeric_input)

    # Configurar las columnas para el contenido principal
    container.grid_columnconfigure(0, weight=1)  # Espacio adicional a la izquierda
    container.grid_columnconfigure(1, weight=0)  # Texto de etiquetas
    container.grid_columnconfigure(2, weight=0)  # Contenido principal
    container.grid_columnconfigure(3, weight=0)  # Más contenido principal
    container.grid_columnconfigure(4, weight=0)  # Más contenido principal
    container.grid_columnconfigure(5, weight=1)  # Espacio adicional a la derecha

    ttk.Label(container, text="Tipo de Siembra:", font=font_large).grid(row=1, column=1, sticky=tk.W, pady=5)
    siembra_var = tk.StringVar(value="Agua")
    tk.Radiobutton(container, text="Agua", variable=siembra_var, value="Agua", font=font_large).grid(row=1, column=2,
                                                                                                     sticky=tk.W,
                                                                                                     padx=(20, 0))
    tk.Radiobutton(container, text="Tierra", variable=siembra_var, value="Tierra", font=font_large).grid(row=1,
                                                                                                         column=3,
                                                                                                         sticky=tk.W)

    ttk.Label(container, text="Ubicación:", font=font_large).grid(row=2, column=1, sticky=tk.W, pady=5)
    ubicacion_var = tk.StringVar(value="L1")
    tk.Radiobutton(container, text="L1", variable=ubicacion_var, value="L1", font=font_large).grid(row=2, column=2,
                                                                                                   sticky=tk.W,
                                                                                                   padx=(20, 0))
    tk.Radiobutton(container, text="L2", variable=ubicacion_var, value="L2", font=font_large).grid(row=2, column=3,
                                                                                                   sticky=tk.W,
                                                                                                   padx=(10, 0))
    tk.Radiobutton(container, text="L3", variable=ubicacion_var, value="L3", font=font_large).grid(row=2, column=4,
                                                                                                   sticky=tk.W,
                                                                                                   padx=(10, 0))
    tk.Radiobutton(container, text="L4", variable=ubicacion_var, value="L4", font=font_large).grid(row=2, column=5,
                                                                                                   sticky=tk.W,
                                                                                                   padx=(10, 0))

    ttk.Label(container, text="Tipo de Lechuga:", font=font_large).grid(row=3, column=1, sticky=tk.W, pady=5)
    lechuga_var = tk.StringVar(value="V1")
    tk.Radiobutton(container, text="V1", variable=lechuga_var, value="V1", font=font_large).grid(row=3, column=2,
                                                                                                 sticky=tk.W,
                                                                                                 padx=(20, 0))
    tk.Radiobutton(container, text="V2", variable=lechuga_var, value="V2", font=font_large).grid(row=3, column=3,
                                                                                                 sticky=tk.W,
                                                                                                 padx=(10, 0))

    ttk.Label(container, text="Numero Planta(1 al 4):", font=font_large).grid(row=4, column=1, sticky=tk.W, pady=5)
    planta_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    planta_entry.grid(row=4, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Numero de hojas:", font=font_large).grid(row=5, column=1, sticky=tk.W, pady=5)
    num_h_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    num_h_entry.grid(row=5, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="AF:", font=font_large).grid(row=6, column=1, sticky=tk.W, pady=5)
    af_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    af_entry.grid(row=6, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="H:", font=font_large).grid(row=7, column=1, sticky=tk.W, pady=5)
    h_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    h_entry.grid(row=7, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Semana:", font=font_large).grid(row=8, column=1, sticky=tk.W, pady=5)
    semana_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    semana_entry.grid(row=8, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Número de Cosecha:", font=font_large).grid(row=9, column=1, sticky=tk.W, pady=5)
    num_cosecha_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(validate_cmd, '%P'))
    num_cosecha_entry.grid(row=9, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Observaciones:", font=font_large).grid(row=10, column=1, sticky=tk.W, pady=5)
    observaciones_entry = ttk.Entry(container, font=font_large)
    observaciones_entry.grid(row=10, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Nombre Foto:", font=font_large).grid(row=11, column=1, sticky=tk.W, pady=5)
    nombre_foto_entry = ttk.Entry(container, font=font_large)
    nombre_foto_entry.grid(row=11, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Ruta Foto:", font=font_large).grid(row=12, column=1, sticky=tk.W, pady=5)
    ruta_foto_entry = ttk.Entry(container, font=font_large)
    ruta_foto_entry.grid(row=12, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    ttk.Label(container, text="Descripción Foto:", font=font_large).grid(row=13, column=1, sticky=tk.W, pady=5)
    descripcion_foto_entry = ttk.Entry(container, font=font_large)
    descripcion_foto_entry.grid(row=13, column=2, sticky=(tk.W, tk.E), columnspan=2, padx=(20, 0))

    # Botón para seleccionar imagen
    ttk.Button(container, text="Seleccionar Imagen", command=select_image, style='TButton').grid(row=12, column=4,
                                                                                                 sticky=tk.W, pady=4)

    # Botones más grandes para guardar y subir masivo
    ttk.Button(container, text="Guardar", command=save_data, style='TButton').grid(row=14, column=2, sticky=tk.E,
                                                                                   pady=6)
    ttk.Button(container, text="Subir Masivo", command=upload_excel, style='TButton').grid(row=14, column=3,
                                                                                           sticky=tk.E, pady=6)
    ttk.Button(container, text="Descargar formato", command=download_template, style='TButton').grid(row=14, column=4,
                                                                                                     sticky=tk.E,
                                                                                                     pady=6)
