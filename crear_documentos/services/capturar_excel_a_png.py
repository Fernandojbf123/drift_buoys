import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def capturar_excel_a_png(ruta_excel: str, nombre_archivo: str = "pruebas_de_transmision", sheet_name=None, filas: int = 20, carpeta_salida: str = ".") -> str:
    """Lee un archivo XLSX y guarda una captura de las primeras filas con encabezados en PNG.

    Parámetros:
        ruta_excel (str): Ruta al archivo .xlsx.
        nombre_archivo (str): Nombre de salida sin extensión. Por defecto 'pruebas_de_transmision'.
        sheet_name (str|int|None): Nombre o índice de la hoja a leer. Por defecto None (primera hoja).
        filas (int): Número de filas a capturar. Por defecto 20.
        carpeta_salida (str): Carpeta donde guardar el PNG. Por defecto carpeta actual.

    Retorna:
        str: Ruta completa del archivo PNG generado.
    """
    if not os.path.isfile(ruta_excel):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_excel}")

    df = pd.read_excel(ruta_excel, sheet_name=sheet_name)
    df_captura = df.head(filas).copy()

    if df_captura.empty:
        raise ValueError("El archivo Excel no contiene filas para capturar.")

    # Ajustar tamaño de figura según columnas y filas
    n_filas, n_columnas = df_captura.shape
    ancho = max(8, n_columnas * 1.2)
    alto = max(4, n_filas * 0.35 + 1.5)

    fig, ax = plt.subplots(figsize=(ancho, alto))
    ax.axis("off")

    tabla = ax.table(
        cellText=df_captura.values.tolist(),
        colLabels=df_captura.columns.tolist(),
        cellLoc="center",
        loc="center",
        colColours=["#d3d3d3"] * n_columnas,
        colWidths=[1.0 / n_columnas] * n_columnas,
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.4)

    for key, cell in tabla.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(0.5)

    ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo}.png")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida, exist_ok=True)

    fig.savefig(ruta_salida, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    return ruta_salida

#####################