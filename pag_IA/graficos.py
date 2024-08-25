import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from sqlalchemy import create_engine
import mplcursors
import numpy as np
from sklearn.metrics import r2_score
from mpldatacursor import datacursor
def obtener_datos_desde_db(query):
    try:
        # Crear una conexión con SQLAlchemy
        engine = create_engine('postgresql+psycopg2://postgres:Yamile25@localhost:5432/Lestoma')

        # Ejecutar la consulta usando pandas con SQLAlchemy
        datos = pd.read_sql(query, engine)

        # Imprimir la consulta y los datos obtenidos para depuración
        print("Consulta ejecutada:")
        print(query)
        print("Datos obtenidos:")
        print(datos.head())  # Muestra las primeras filas del DataFrame

        return datos
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None

def mostrar_grafico_crecimiento_plantas(parent, main_content_widgets):
    query = """
                SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", tl."TipoLechuga"
                FROM "Hidroponia"."TBDatos" d
                JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
                JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
                JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
                WHERE ts."Tip_siembra" = 'Agua'
            """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots(figsize=(6, 4))  # Reducido el tamaño vertical

    lines = []
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                        label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Crecimiento (AF)')
    ax.set_title('Crecimiento de Plantas en Agua por Cosecha y Tipo')
    ax.legend(loc='best', fontsize='small')  # Reducido el tamaño de la leyenda
    ax.grid(True)

    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Este gráfico muestra el crecimiento de las plantas de diferentes tipos de lechuga\n"
    info_text += f"en sistemas hidroponicos a lo largo de varias semanas.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Añadir el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)

    # Forzar la actualización de la interfaz
    parent.update_idletasks()

def mostrar_grafico_crecimiento_plantas_tierra(parent, main_content_widgets):
    query = """
            SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", tl."TipoLechuga"
            FROM "Hidroponia"."TBDatos" d
            JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
            JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
            JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
            WHERE ts."Tip_siembra" = 'Tierra'
        """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    # Crear un frame principal
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots(figsize=(6, 4))  # Reducido el tamaño vertical

    lines = []
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                 label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Crecimiento (AF)')
    ax.set_title('Crecimiento de Plantas en Tierra por Cosecha y Tipo')
    ax.legend(loc='best', fontsize='small')  # Reducido el tamaño de la leyenda
    ax.grid(True)

    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Este gráfico muestra el crecimiento de las plantas de diferentes tipos de lechuga\n"
    info_text += f"cultivadas en tierra a lo largo de varias semanas.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Añadir el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)

    # Forzar la actualización de la interfaz
    parent.update_idletasks()

#####@@
def mostrar_grafico_n_hojas(parent, main_content_widgets):
    query = """
            SELECT d."Semana", d."NumHojas", d."Num_cosecha", l."Ubicacion", tl."TipoLechuga"
            FROM "Hidroponia"."TBDatos" d
            JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
            JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
            JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
            WHERE ts."Tip_siembra" = 'Agua'
        """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['NumHojas'] = pd.to_numeric(datos['NumHojas'], errors='coerce')
    datos = datos.dropna(subset=['NumHojas'])

    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario

    lines = []
    # Iterar sobre cada combinación de TipoLechuga y Num_cosecha
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['NumHojas'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['NumHojas'],
                        label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Número de Hojas')
    ax.set_title('Número de Hojas de Plantas en Agua Semana a Semana')
    ax.legend(loc='best', fontsize='x-small')  # Ajusta el tamaño de la fuente de la leyenda
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nNúmero de Hojas: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Este gráfico muestra la evolución del número de hojas de diferentes tipos de lechuga\n"
    info_text += f"cultivadas en sistemas hidroponicos a lo largo de varias semanas.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)

def mostrar_grafico_n_hojas_tierra(parent, main_content_widgets):
    query = """
        SELECT d."Semana", d."NumHojas", d."Num_cosecha", l."Ubicacion", tl."TipoLechuga"
        FROM "Hidroponia"."TBDatos" d
        JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
        JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
        JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
        WHERE ts."Tip_siembra" = 'Tierra'
    """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['NumHojas'] = pd.to_numeric(datos['NumHojas'], errors='coerce')
    datos = datos.dropna(subset=['NumHojas'])

    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario

    lines = []
    # Iterar sobre cada combinación de TipoLechuga y Num_cosecha
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['NumHojas'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['NumHojas'],
                        label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Número de Hojas')
    ax.set_title('Número de Hojas de Plantas en Tierra Semana a Semana')
    ax.legend(loc='best', fontsize='x-small')  # Ajusta el tamaño de la fuente de la leyenda
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nNúmero de Hojas: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Este gráfico muestra la evolución del número de hojas de diferentes tipos de lechuga\n"
    info_text += f"cultivadas en camas de tierra a lo largo de varias semanas.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)


def mostrar_grafico_af_plantas_agua_v1(parent, main_content_widgets):
    query = """
        SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", l."Planta", tl."TipoLechuga"
        FROM "Hidroponia"."TBDatos" d
        JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
        JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
        JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
        WHERE ts."Tip_siembra" = 'Agua'
    """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    datos_v1 = datos[datos['TipoLechuga'] == 'V1']
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig1, ax1 = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario
    lines = []
    for (ubicacion, tipo_lechuga, num_cosecha, planta) in datos_v1[
        ['Ubicacion', 'TipoLechuga', 'Num_cosecha', 'Planta']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos_v1[(datos_v1['Ubicacion'] == ubicacion) &
                                (datos_v1['TipoLechuga'] == tipo_lechuga) &
                                (datos_v1['Num_cosecha'] == num_cosecha) &
                                (datos_v1['Planta'] == planta)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        if not promedios_semanales.empty:
            line, = ax1.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                             label=f'{ubicacion} - {tipo_lechuga} - Cosecha {num_cosecha} - Planta {planta}')
            lines.append(line)

    ax1.set_title('AF de Plantas (V1) Agua Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax1.grid(True)
    fig1.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
    canvas1.draw()
    canvas_widget = canvas1.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Se observan variaciones en el crecimiento del area foliar entre las distintas plantas en camas\n"
    info_text += f"hidroponicas de la priemra variedad, lo que puede indicar diferencias en las condiciones de cultivo o en la respuesta individual de cada planta.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)


def mostrar_grafico_af_plantas_agua_v2(parent, main_content_widgets):
    query = """
        SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", l."Planta", tl."TipoLechuga"
        FROM "Hidroponia"."TBDatos" d
        JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
        JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
        JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
        WHERE ts."Tip_siembra" = 'Agua'
    """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    datos_v2 = datos[datos['TipoLechuga'] == 'V2']
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig2, ax2 = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario
    lines = []
    for (ubicacion, tipo_lechuga, num_cosecha, planta) in datos_v2[
        ['Ubicacion', 'TipoLechuga', 'Num_cosecha', 'Planta']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos_v2[(datos_v2['Ubicacion'] == ubicacion) &
                                (datos_v2['TipoLechuga'] == tipo_lechuga) &
                                (datos_v2['Num_cosecha'] == num_cosecha) &
                                (datos_v2['Planta'] == planta)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        if not promedios_semanales.empty:
            line, = ax2.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                             label=f'{ubicacion} - {tipo_lechuga} - Cosecha {num_cosecha} - Planta {planta}')
            lines.append(line)

    ax2.set_title('AF de Plantas (V2) Agua Semana a Semana')
    ax2.set_xlabel('Semana')
    ax2.set_ylabel('AF')
    ax2.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax2.grid(True)
    fig2.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
    canvas2.draw()
    canvas_widget = canvas2.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información adicional
    info_text = "Se observan variaciones en el crecimiento del area foliar entre las distintas plantas en camas \n"
    info_text += f"hidroponicas, lo que puede indicar diferencias en las condiciones de cultivo o en la respuesta individual de cada planta.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)

def mostrar_grafico_af_plantas_tierra_v1(parent, main_content_widgets):
    query = """
        SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", l."Planta", tl."TipoLechuga"
        FROM "Hidroponia"."TBDatos" d
        JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
        JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
        JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
        WHERE ts."Tip_siembra" = 'Tierra'
    """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    datos_v1 = datos[datos['TipoLechuga'] == 'V1']
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig1, ax1 = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario
    lines = []
    for (ubicacion, tipo_lechuga, num_cosecha, planta) in datos_v1[
        ['Ubicacion', 'TipoLechuga', 'Num_cosecha', 'Planta']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos_v1[(datos_v1['Ubicacion'] == ubicacion) &
                                (datos_v1['TipoLechuga'] == tipo_lechuga) &
                                (datos_v1['Num_cosecha'] == num_cosecha) &
                                (datos_v1['Planta'] == planta)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        if not promedios_semanales.empty:
            line, = ax1.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                             label=f'{ubicacion} - {tipo_lechuga} - Cosecha {num_cosecha} - Planta {planta}')
            lines.append(line)

    ax1.set_title('AF de Plantas (V1) Tierra Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax1.grid(True)
    fig1.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
    canvas1.draw()
    canvas_widget = canvas1.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información resumida
    info_text = "Se observan variaciones en el crecimiento del area foliar entre las distintas plantas en camas de\n"
    info_text += f"tierra de la priemra variedad, lo que puede indicar diferencias en las condiciones de cultivo o en la respuesta individual de cada planta.\n"

    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)


def mostrar_grafico_af_plantas_tierra_v2(parent, main_content_widgets):
    query = """
        SELECT d."Semana", d."AF", d."Num_cosecha", l."Ubicacion", l."Planta", tl."TipoLechuga"
        FROM "Hidroponia"."TBDatos" d
        JOIN "Hidroponia"."TBLechuga" l ON d."FKIdLechuga" = l."PKIdLechuga"
        JOIN "Hidroponia"."TBTipoSiembra" ts ON l."FKIdTipSiembra" = ts."PKIdTipSiembra"
        JOIN "Hidroponia"."TBTipoLechuga" tl ON l."FKIdTipoLechuga" = tl."PKIdTipoLechuga"
        WHERE ts."Tip_siembra" = 'Tierra'
    """

    datos = obtener_datos_desde_db(query)

    if datos is None or datos.empty:
        print("No se obtuvieron datos.")
        return

    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])

    datos_v2 = datos[datos['TipoLechuga'] == 'V2']
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Crear el gráfico
    fig2, ax2 = plt.subplots(figsize=(6, 4))  # Ajusta el tamaño según sea necesario
    lines = []
    for (ubicacion, tipo_lechuga, num_cosecha, planta) in datos_v2[
        ['Ubicacion', 'TipoLechuga', 'Num_cosecha', 'Planta']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos_v2[(datos_v2['Ubicacion'] == ubicacion) &
                                (datos_v2['TipoLechuga'] == tipo_lechuga) &
                                (datos_v2['Num_cosecha'] == num_cosecha) &
                                (datos_v2['Planta'] == planta)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        if not promedios_semanales.empty:
            line, = ax2.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                             label=f'{ubicacion} - {tipo_lechuga} - Cosecha {num_cosecha} - Planta {planta}')
            lines.append(line)

    ax2.set_title('AF de Plantas (V2) Tierra Semana a Semana')
    ax2.set_xlabel('Semana')
    ax2.set_ylabel('AF')
    ax2.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax2.grid(True)
    fig2.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    # Crear un frame para el gráfico
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
    canvas2.draw()
    canvas_widget = canvas2.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Crear un frame para contener la información adicional
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    # Agregar información adicional
    info_text = "Se observan variaciones en el crecimiento del area foliar entre las distintas plantas en camas de\n"
    info_text += f"tierra de la segunda variedad, lo que puede indicar diferencias en las condiciones de cultivo o en la respuesta individual de cada planta.\n"



    info_label = ttk.Label(info_frame, text=info_text, wraplength=500, justify=tk.LEFT)
    info_label.pack(fill=tk.X, padx=5, pady=5)

    # Agregar el frame principal a main_content_widgets
    main_content_widgets.append(main_frame)

##
def mostrar_grafico_regresion_polynomial(parent, main_content_widgets):
    # Creación de muestras aleatorias
    np.random.seed(2)
    itemPrices = np.random.normal(3.0, 1.0, 1000)
    purchaseAmount = np.random.normal(50.0, 10.0, 1000) / itemPrices

    # Calcular la curva polinómica de 4to grado
    x = np.array(itemPrices)
    y = np.array(purchaseAmount)

    p4 = np.poly1d(np.polyfit(x, y, 4))

    # Crear puntos para la gráfica de la curva
    xp = np.linspace(0, 7, 100)

    # Crear la figura
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x, y)
    ax.plot(xp, p4(xp), c='r')
    ax.set_title('Regresión Polinómica de 4to Grado')
    ax.set_xlabel('Precio del Producto')
    ax.set_ylabel('Cantidad Comprada')

    # Calcular y mostrar el error cuadrático medio
    r2 = r2_score(y, p4(x))
    ax.text(0.05, 0.95, f'$R^2 = {r2:.2f}$', transform=ax.transAxes, fontsize=14, verticalalignment='top')

    # Integrar la gráfica en tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())

    # Crear un Frame para contener los textos
    text_frame = tk.Frame(parent, bg="white")
    text_frame.pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(text_frame)

    # Mostrar el polinomio y el error cuadrático en etiquetas de texto
    polynomial_label = tk.Label(text_frame, text=f"El polinomio que se obtiene es:\n{p4}", bg="white")
    polynomial_label.pack(side=tk.TOP, pady=10)
    main_content_widgets.append(polynomial_label)

    r2_label = tk.Label(text_frame, text=f"El error cuadrático del ajuste es:\n{r2}", bg="white")
    r2_label.pack(side=tk.TOP, pady=10)
    main_content_widgets.append(r2_label)
