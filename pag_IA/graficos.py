import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sklearn.metrics import r2_score
import sklearn


def mostrar_grafico_crecimiento_plantas(parent, main_content_widgets):
    archivo_csv = 'agua.csv'
    datos = pd.read_csv(archivo_csv, encoding='latin1')

    print(datos.head())
    print(datos.columns)

    if 'AF' not in datos.columns:
        raise ValueError("La columna 'AF' no se encuentra en el archivo CSV")

    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])
    datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)

    plt.figure(figsize=(6, 6))
    for ubicacion in datos['V'].unique():
        datos_ubicacion = datos[datos['V'] == ubicacion]
        promedios_semanales = datos_ubicacion.groupby('Semana')['AF'].mean().reset_index()
        plt.plot(promedios_semanales['Semana'], promedios_semanales['AF'], label=f'{ubicacion}')

    plt.xlabel('Semana')
    plt.ylabel('Crecimiento (AF)')
    plt.title('Crecimiento de Plantas en Agua Semana a Semana')
    plt.legend()
    plt.grid(True)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())


def mostrar_grafico_crecimiento_plantas_tierra(parent, main_content_widgets):
    archivo_csv = 'tierra.csv'
    datos = pd.read_csv(archivo_csv, encoding='latin1')

    print(datos.head())
    print(datos.columns)

    if 'AF' not in datos.columns:
        raise ValueError("La columna 'AF' no se encuentra en el archivo CSV")

    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])
    datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)

    plt.figure(figsize=(10, 6))

    for ubicacion in datos['V'].unique():
        datos_ubicacion = datos[datos['V'] == ubicacion]
        promedios_semanales = datos_ubicacion.groupby('Semana')['AF'].mean().reset_index()
        plt.plot(promedios_semanales['Semana'], promedios_semanales['AF'], label=f'{ubicacion}')

    # Ajustar y dibujar la curva polinómica
    semanas = datos['Semana']
    areafoliar = datos['AF'].astype(float)

    x = semanas
    y = areafoliar

    p4 = np.poly1d(np.polyfit(x, y, 3))
    xp = np.linspace(min(semanas), max(semanas), 100)

    plt.scatter(x, y, label='Datos originales', alpha=0.5)
    plt.plot(xp, p4(xp), c='r', label='Ajuste polinómico grado 3')

    plt.xlabel('Semana')
    plt.ylabel('Crecimiento (AF)')
    plt.title('Crecimiento de Plantas en Tierra Semana a Semana')
    plt.legend()
    plt.grid(True)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())


def mostrar_grafico_n_hojas(parent, main_content_widgets):
    archivo_csv = 'agua.csv'
    datos = pd.read_csv(archivo_csv, encoding='latin1')

    print(datos.head())
    print(datos.columns)

    if 'N_Hojas' not in datos.columns:
        raise ValueError("La columna 'N_Hojas' no se encuentra en el archivo CSV")

    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
    datos['N_Hojas'] = pd.to_numeric(datos['N_Hojas'], errors='coerce')
    datos = datos.dropna(subset=['N_Hojas'])
    datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)

    plt.figure(figsize=(6, 6))
    for ubicacion in datos['V'].unique():
        datos_ubicacion = datos[datos['V'] == ubicacion]
        promedios_semanales = datos_ubicacion.groupby('Semana')['N_Hojas'].mean().reset_index()
        plt.plot(promedios_semanales['Semana'], promedios_semanales['N_Hojas'], label=f'{ubicacion}')

    plt.xlabel('Semana')
    plt.ylabel('Número de Hojas')
    plt.title('Número de Hojas de Plantas en Agua Semana a Semana')
    plt.legend()
    plt.grid(True)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas.get_tk_widget())


def mostrar_grafico_af_plantas_agua(parent, main_content_widgets):
    archivo_csv = 'agua.csv'
    datos = pd.read_csv(archivo_csv, encoding='latin1')

    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])
    datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)

    datos_v1 = datos[datos['V'] == 'V1']
    datos_v2 = datos[datos['V'] == 'V2']

    fig1, ax1 = plt.subplots(figsize=(6, 6))
    for planta in datos_v1['Id_planta'].unique():
        datos_planta = datos_v1[datos_v1['Id_planta'] == planta]
        ax1.plot(datos_planta['Semana'], datos_planta['AF'], marker='o', label=f'Planta {planta}')
    ax1.set_title('AF de Plantas (V1) Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend()
    ax1.grid(True)
    fig1.tight_layout()

    canvas1 = FigureCanvasTkAgg(fig1, master=parent)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas1.get_tk_widget())

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    for planta in datos_v2['Id_planta'].unique():
        datos_planta = datos_v2[datos_v2['Id_planta'] == planta]
        ax2.plot(datos_planta['Semana'], datos_planta['AF'], marker='o', label=f'Planta {planta}')
    ax2.set_title('AF de Plantas (V2) Semana a Semana')
    ax2.set_xlabel('Semana')
    ax2.set_ylabel('AF')
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()

    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())


def mostrar_grafico_af_plantas_tierra(parent, main_content_widgets):
    archivo_csv = 'tierra.csv'
    datos = pd.read_csv(archivo_csv, encoding='latin1')

    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
    datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
    datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
    datos['AF'] = pd.to_numeric(datos['AF'], errors='coerce')
    datos = datos.dropna(subset=['AF'])
    datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)

    datos_v1 = datos[datos['V'] == 'V1']
    datos_v2 = datos[datos['V'] == 'V2']

    fig1, ax1 = plt.subplots(figsize=(6, 6))
    for planta in datos_v1['Id_planta'].unique():
        datos_planta = datos_v1[datos_v1['Id_planta'] == planta]
        ax1.plot(datos_planta['Semana'], datos_planta['AF'], marker='o', label=f'Planta {planta}')
    ax1.set_title('AF de Plantas (V1) Semana a Semana')
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('AF')
    ax1.legend()
    ax1.grid(True)
    fig1.tight_layout()

    canvas1 = FigureCanvasTkAgg(fig1, master=parent)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas1.get_tk_widget())

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    for planta in datos_v2['Id_planta'].unique():
        datos_planta = datos_v2[datos_v2['Id_planta'] == planta]
        ax2.plot(datos_planta['Semana'], datos_planta['AF'], marker='o', label=f'Planta {planta}')
    ax2.set_title('AF de Plantas (V2) Semana a Semana')
    ax2.set_xlabel('Semana')
    ax2.set_ylabel('AF')
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()

    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    main_content_widgets.append(canvas2.get_tk_widget())

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

    def leer_datos_csv(archivo_csv, columnas_requeridas):
        datos = pd.read_csv(archivo_csv, encoding='latin1')
        for columna in columnas_requeridas:
            if columna not in datos.columns:
                raise ValueError(f"La columna '{columna}' no se encuentra en el archivo CSV")
        datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
        datos['Semana'] = pd.to_numeric(datos['Semana'], errors='coerce')
        datos['Id_planta'] = pd.to_numeric(datos['Id_planta'], errors='coerce')
        for columna in columnas_requeridas:
            datos[columna] = pd.to_numeric(datos[columna], errors='coerce')
        datos = datos.dropna(subset=columnas_requeridas)
        datos[['L', 'V']] = datos['Ubicacion'].str.split(' ', expand=True)
        return datos

        # Leemos los datos del archivo CSV (puede ser 'agua.csv' o 'tierra.csv')
        archivo_csv = 'agua.csv'  # Cambia a 'tierra.csv' según sea necesario
        columnas_requeridas = ['AF']  # Lista de columnas requeridas
        datos = leer_datos_csv(archivo_csv, columnas_requeridas)

        # Creamos las listas de los datos a evaluar
        semanas = np.array(datos['Semana'])
        areafoliar = np.array(datos['AF'])

        # Calculamos la curva polinómica de grado 4 que se ajusta a los datos
        x = semanas
        y = areafoliar
        p4 = np.poly1d(np.polyfit(x, y, 3))

        # Pintamos la muestra y la función polinómica en rojo para ver cómo se ajusta
        xp = np.linspace(min(semanas), max(semanas), 100)
        plt.scatter(x, y)
        plt.plot(xp, p4(xp), c='r')
        plt.xlabel('Semana')
        plt.ylabel('Crecimiento (AF)')
        plt.title('Curva Polinómica Ajustada al Crecimiento de Plantas en Agua')
        plt.grid(True)
        plt.show()

        # Imprimimos la ecuación
        print("El polinomio que se obtiene es:")
        print(p4)

        # Medimos el error cuadrático medio
        r2 = r2_score(y, p4(x))
        print("El error cuadrático del ajuste es:")
        print(r2)


