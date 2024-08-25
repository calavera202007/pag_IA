import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from sqlalchemy import create_engine
import mplcursors
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

    fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño de la figura ajustado

    lines = []
    # Iterar sobre cada combinación de TipoLechuga y Num_cosecha
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                        label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Crecimiento (AF)')
    ax.set_title('Crecimiento de Plantas en Agua por Cosecha y Tipo')
    ax.legend(loc='best')  # Coloca la leyenda en la mejor posición
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())

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

    fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño de la figura ajustado

    lines = []
    # Iterar sobre cada combinación de TipoLechuga y Num_cosecha
    for (tipo_lechuga, num_cosecha) in datos[['TipoLechuga', 'Num_cosecha']].drop_duplicates().itertuples(index=False):
        datos_filtro = datos[(datos['TipoLechuga'] == tipo_lechuga) & (datos['Num_cosecha'] == num_cosecha)]
        promedios_semanales = datos_filtro.groupby('Semana')['AF'].mean().reset_index()
        line, = ax.plot(promedios_semanales['Semana'], promedios_semanales['AF'],
                 label=f'{tipo_lechuga} - Cosecha {num_cosecha}')
        lines.append(line)

    ax.set_xlabel('Semana')
    ax.set_ylabel('Crecimiento (AF)')
    ax.set_title('Crecimiento de Plantas en Tierra por Cosecha y Tipo')
    ax.legend(loc='best')  # Coloca la leyenda en la mejor posición
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())

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

    fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño de la figura ajustado

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
    ax.legend(loc='best')  # Coloca la leyenda en la mejor posición
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nNúmero de Hojas: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())

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

    fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño de la figura ajustado

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
    ax.legend(loc='best')  # Coloca la leyenda en la mejor posición
    ax.grid(True)

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nNúmero de Hojas: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())


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
    fig1, ax1 = plt.subplots(figsize=(5, 5))
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

    ax1.set_title('AF de Plantas (V2) Agua Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax1.grid(True)
    fig1.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas2 = FigureCanvasTkAgg(fig1, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())


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
    fig2, ax2 = plt.subplots(figsize=(5, 5))
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

    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())

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
    fig1, ax1 = plt.subplots(figsize=(5, 5))
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

    ax1.set_title('AF de Plantas (V2) Tierra Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend(loc='best', fontsize='x-small', framealpha=0.5)
    ax1.grid(True)
    fig1.tight_layout()

    # Agregar tooltips
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Semana: {sel.target[0]:.1f}\nAF: {sel.target[1]:.2f}\n{sel.artist.get_label()}'))

    canvas2 = FigureCanvasTkAgg(fig1, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())


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
    fig2, ax2 = plt.subplots(figsize=(5, 5))
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

    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())