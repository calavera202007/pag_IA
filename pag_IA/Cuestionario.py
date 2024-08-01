import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import uuid
import psycopg2

def validate_numeric_input(new_value):
    if new_value == "" or new_value.replace(".", "", 1).isdigit():
        return True
    return False

def highlight_empty_fields(fields):
    for field in fields:
        if 'entry' in field and field['entry'] is not None:
            if not field['var'].get():
                field['entry'].config(background='red')
            else:
                field['entry'].config(background='white')

def save_data():
    siembra = siembra_var.get()
    ubicacion = ubicacion_var.get()
    lechuga = lechuga_var.get()
    af = af_entry.get()
    h = h_entry.get()
    semana = semana_entry.get()
    num_cosecha = num_cosecha_entry.get()
    observaciones = observaciones_entry.get()
    nombre_foto = nombre_foto_entry.get()
    ruta_foto = ruta_foto_entry.get()
    descripcion_foto = descripcion_foto_entry.get()

    # Validación de campos obligatorios
    mandatory_fields = [
        {'var': siembra_var, 'entry': None},
        {'var': ubicacion_var, 'entry': None},
        {'var': lechuga_var, 'entry': None},
        {'var': tk.StringVar(value=af), 'entry': af_entry},
        {'var': tk.StringVar(value=h), 'entry': h_entry},
        {'var': tk.StringVar(value=semana), 'entry': semana_entry},
        {'var': tk.StringVar(value=num_cosecha), 'entry': num_cosecha_entry}
    ]

    highlight_empty_fields(mandatory_fields)

    if not all([siembra, ubicacion, lechuga, af, h, semana, num_cosecha]):
        messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
        return

    # Validación de campos numéricos
    try:
        float(af)
        float(h)
        float(semana)
        float(num_cosecha)
    except ValueError:
        messagebox.showerror("Error", "Los campos AF, H, Semana y Número de Siembra deben ser números válidos.")
        return

    # Generar UUIDs
    id_tip_siembra = str(uuid.uuid4())
    id_tipo_lechuga = str(uuid.uuid4())
    id_lechuga = str(uuid.uuid4())
    id_datos = str(uuid.uuid4())
    id_reporte = str(uuid.uuid4())
    id_foto = str(uuid.uuid4()) if nombre_foto else None

    # Conectar a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="Yamile25",
            host="localhost",
            port="5432",
            database="Hidroponia"
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
        INSERT INTO "Hidroponia"."TBLechuga" ("PKIdLechuga", "FKIdTipoLechuga", "FKIdTipSiembra", "Ubicacion")
        VALUES (%s, %s, %s, %s);
        """, (id_lechuga, id_tipo_lechuga, id_tip_siembra, ubicacion))

        # Insertar en TBFoto (si se proporcionó información)
        if nombre_foto:
            cursor.execute("""
            INSERT INTO "Hidroponia"."TBFoto" ("PKIdFoto", "Nombre", "Ruta", "Descripcion")
            VALUES (%s, %s, %s, %s);
            """, (id_foto, nombre_foto, ruta_foto, descripcion_foto))

        # Insertar en TBDatos
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBDatos" ("PKIdDatos", "AF", "H", "Semana", "Num_cosecha", "Observaciones", "FKIdLechuga")
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (id_datos, af, h, semana, num_cosecha, observaciones, id_lechuga))

        # Insertar en TBReporte
        cursor.execute("""
        INSERT INTO "Hidroponia"."TBReporte" ("PKIdReporte", "FKIdDatos", "FKIdFoto")
        VALUES (%s, %s, %s);
        """, (id_reporte, id_datos, id_foto if nombre_foto else None))

        # Confirmar cambios
        conn.commit()
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")

        # Limpiar campos de entrada
        clear_fields()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e.pgcode} - {e.pgerror}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

def clear_fields():
    siembra_var.set("Agua")
    ubicacion_var.set("L1")
    lechuga_var.set("V1")
    af_entry.delete(0, tk.END)
    h_entry.delete(0, tk.END)
    semana_entry.delete(0, tk.END)
    num_cosecha_entry.delete(0, tk.END)
    observaciones_entry.delete(0, tk.END)
    nombre_foto_entry.delete(0, tk.END)
    ruta_foto_entry.delete(0, tk.END)
    descripcion_foto_entry.delete(0, tk.END)
    # Restablecer el color de fondo de los campos
    af_entry.config(background='white')
    h_entry.config(background='white')
    semana_entry.config(background='white')
    num_cosecha_entry.config(background='white')

def main(frame):
    global siembra_var, ubicacion_var, lechuga_var, af_entry, h_entry, semana_entry, num_cosecha_entry
    global observaciones_entry, nombre_foto_entry, ruta_foto_entry, descripcion_foto_entry

    for widget in frame.winfo_children():
        widget.destroy()  # Limpiar widgets anteriores en el frame

    container = ttk.Frame(frame, padding="50")
    container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    font_large = ("Helvetica", 20)

    ttk.Label(container, text="Tipo de Siembra:", font=font_large).grid(row=1, column=1, sticky=tk.W)
    siembra_var = tk.StringVar(value="Agua")
    tk.Radiobutton(container, text="Agua", variable=siembra_var, value="Agua", font=font_large).grid(row=1, column=2, sticky=tk.W)
    tk.Radiobutton(container, text="Tierra", variable=siembra_var, value="Tierra", font=font_large).grid(row=1, column=3, sticky=tk.W)

    ttk.Label(container, text="Ubicación:", font=font_large).grid(row=2, column=1, sticky=tk.W)
    ubicacion_var = tk.StringVar(value="L1")
    tk.Radiobutton(container, text="L1", variable=ubicacion_var, value="L1", font=font_large).grid(row=2, column=2, sticky=tk.W)
    tk.Radiobutton(container, text="L2", variable=ubicacion_var, value="L2", font=font_large).grid(row=2, column=3, sticky=tk.W)
    tk.Radiobutton(container, text="L3", variable=ubicacion_var, value="L3", font=font_large).grid(row=2, column=4, sticky=tk.W)
    tk.Radiobutton(container, text="L4", variable=ubicacion_var, value="L4", font=font_large).grid(row=2, column=5, sticky=tk.W)

    ttk.Label(container, text="Tipo de Lechuga:", font=font_large).grid(row=3, column=1, sticky=tk.W)
    lechuga_var = tk.StringVar(value="V1")
    tk.Radiobutton(container, text="V1", variable=lechuga_var, value="V1", font=font_large).grid(row=3, column=2, sticky=tk.W)
    tk.Radiobutton(container, text="V2", variable=lechuga_var, value="V2", font=font_large).grid(row=3, column=3, sticky=tk.W)

    ttk.Label(container, text="Área Foliar (cm2):", font=font_large).grid(row=4, column=1, sticky=tk.W)
    af_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(container.register(validate_numeric_input), '%P'))
    af_entry.grid(row=4, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Altura (cm):", font=font_large).grid(row=5, column=1, sticky=tk.W)
    h_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(container.register(validate_numeric_input), '%P'))
    h_entry.grid(row=5, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Semana:", font=font_large).grid(row=6, column=1, sticky=tk.W)
    semana_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(container.register(validate_numeric_input), '%P'))
    semana_entry.grid(row=6, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Número de Siembra:", font=font_large).grid(row=7, column=1, sticky=tk.W)
    num_cosecha_entry = ttk.Entry(container, font=font_large, validate="key", validatecommand=(container.register(validate_numeric_input), '%P'))
    num_cosecha_entry.grid(row=7, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Observaciones:", font=font_large).grid(row=8, column=1, sticky=tk.W)
    observaciones_entry = ttk.Entry(container, font=font_large)
    observaciones_entry.grid(row=8, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Nombre Foto (Opcional):", font=font_large).grid(row=9, column=1, sticky=tk.W)
    nombre_foto_entry = ttk.Entry(container, font=font_large)
    nombre_foto_entry.grid(row=9, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Ruta Foto (Opcional):", font=font_large).grid(row=10, column=1, sticky=tk.W)
    ruta_foto_entry = ttk.Entry(container, font=font_large)
    ruta_foto_entry.grid(row=10, column=2, columnspan=4, sticky=(tk.W, tk.E))

    ttk.Label(container, text="Descripción Foto (Opcional):", font=font_large).grid(row=11, column=1, sticky=tk.W)
    descripcion_foto_entry = ttk.Entry(container, font=font_large)
    descripcion_foto_entry.grid(row=11, column=2, columnspan=4, sticky=(tk.W, tk.E))

    tk.Button(container, text="Guardar", command=save_data, font=font_large).grid(row=12, column=2, columnspan=4, sticky=tk.E)

    for i in range(1, 6):
        container.columnconfigure(i, weight=1)

# Aquí deberías tener el código para crear la ventana principal y llamar a main()