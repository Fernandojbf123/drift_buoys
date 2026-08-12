import os
from pathlib import Path
import time
import gc
from PIL import ImageGrab
import win32com.client as win32
import re

"""
excel_a_png.py

Convierte uno o varios archivos CSV en imágenes PNG.

Requisitos:
    pip install pywin32 pillow

Requiere Microsoft Excel instalado.
"""

# ==========================================================
# Funciones internas
# ==========================================================

def _abrir_excel(visible=False):
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = visible
    excel.DisplayAlerts = False
    return excel


def _formatear_hoja(hoja):
    """
    Ajusta formato de la hoja.
    """

    hoja.Cells.Font.Name = "Calibri"
    hoja.Cells.Font.Size = 18

    hoja.Cells.HorizontalAlignment = -4108   # xlCenter
    hoja.Cells.VerticalAlignment = -4108

    hoja.Cells.WrapText = False

    hoja.Columns.AutoFit()
    hoja.Rows.AutoFit()

def _obtener_rango_utilizado(hoja, max_filas=None):
    """
    Devuelve el rango utilizado o solo las primeras max_filas.
    """

    rango = hoja.UsedRange

    ultima_fila = rango.Rows.Count
    ultima_columna = rango.Columns.Count

    if max_filas is not None:
        ultima_fila = min(max_filas, ultima_fila)

    return hoja.Range(
        hoja.Cells(1, 1),
        hoja.Cells(ultima_fila, ultima_columna)
    )

def _copiar_rango_como_imagen(rango):
    """
    Copia el rango al portapapeles como imagen.
    """
    rango.CopyPicture(Appearance=1, Format=2)


def _guardar_portapapeles_png(ruta_png, espera=0.8):
    """
    Guarda la imagen del portapapeles.
    """

    time.sleep(espera)

    imagen = ImageGrab.grabclipboard()

    if imagen is None:
        raise RuntimeError("No fue posible obtener la imagen del portapapeles.")

    imagen.save(ruta_png)


# ==========================================================
# Funciones públicas
# ==========================================================

def csv_a_png(
    archivo_csv,
    carpeta_salida=None,
    visible=False,
    max_filas=None,
    nombre_salida=None
):
    """
    Convierte un CSV en una imagen PNG.

    Parameters
    ----------
    archivo_csv : str | Path
    carpeta_salida : str | Path | None
    visible : bool

    Returns
    -------
    Path
        Ruta del PNG creado.
    """

    archivo_csv = Path(archivo_csv)

    if carpeta_salida is None:
        carpeta_salida = archivo_csv.parent
    else:
        carpeta_salida = Path(carpeta_salida)

    carpeta_salida.mkdir(exist_ok=True, parents=True)

    ruta_png = os.path.join(carpeta_salida, nombre_salida)

    excel = _abrir_excel(visible)

    try:

        libro = excel.Workbooks.Open(str(archivo_csv.resolve()))

        hoja = libro.Worksheets(1)

        _formatear_hoja(hoja)

        rango = _obtener_rango_utilizado(
            hoja,
            max_filas=max_filas
        )
        _copiar_rango_como_imagen(rango)

        _guardar_portapapeles_png(ruta_png)

        libro.Close(False)

    finally:
        excel.Quit()

    return ruta_png


