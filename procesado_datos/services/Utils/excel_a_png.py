from pathlib import Path
import time
import gc
from PIL import ImageGrab
import win32com.client as win32
import re


def _obtener_serial_del_csv(archivo_csv):
    archivo_csv = Path(archivo_csv)

    # 1) Intentar extraerlo del nombre del archivo
    match = re.search(
        r"prueba_en_tierra[_-]*(?P<serial>.+?)(?:_TOTAL)?$",
        archivo_csv.stem,
        flags=re.I,
    )
    if match:
        return match.group("serial").strip().replace(" ", "_")

    # 2) Fallback: intentar leer el CSV y buscar una columna con "serial" o "sonda"
    try:
        import pandas as pd

        df = pd.read_csv(archivo_csv, nrows=5)
        for col in df.columns:
            nombre_col = str(col).lower()
            if "serial" in nombre_col or "sonda" in nombre_col:
                for valor in df[col].dropna().astype(str).tolist():
                    if valor:
                        return valor.strip().replace(" ", "_")
    except Exception:
        pass

    return None

def _abrir_excel(visible=False):
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = visible
    excel.DisplayAlerts = False
    excel.ScreenUpdating = False
    excel.EnableEvents = False
    return excel


def _formatear_hoja(hoja):
    hoja.Cells.Font.Name = "Calibri"
    hoja.Cells.Font.Size = 18
    hoja.Cells.HorizontalAlignment = -4108
    hoja.Cells.VerticalAlignment = -4108
    hoja.Cells.WrapText = False
    hoja.Columns.AutoFit()
    hoja.Rows.AutoFit()


def _obtener_rango_utilizado(hoja, max_filas=None):
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
    rango.CopyPicture(Appearance=1, Format=2)


def _guardar_portapapeles_png(ruta_png, espera=0.8):
    time.sleep(espera)

    imagen = ImageGrab.grabclipboard()
    if imagen is None:
        raise RuntimeError("No fue posible obtener la imagen del portapapeles.")

    ruta_png.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(ruta_png)

def lista_csv_a_png(
    lista_csv,
    carpeta_salida=None,
    visible=False,
    max_filas=None
):

    """
    Convierte una lista de CSV en PNG.

    Parameters
    ----------
    lista_csv : iterable
    carpeta_salida : str | Path | None
    visible : bool
    max_filas : int | None
    Returns
    -------
    list[Path]
    """

    resultados = []

    
    for archivo in lista_csv:
        resultados.append(csv_a_png(
        archivo,
        carpeta_salida=carpeta_salida,
        visible=visible,
        max_filas=max_filas
    )
)
    return resultados

def csv_a_png(archivo_csv, carpeta_salida=None, visible=False, max_filas=None):
    # Soporta un solo archivo o una lista de archivos
    if isinstance(archivo_csv, (list, tuple, set)):
        return lista_csv_a_png(
            list(archivo_csv),
            carpeta_salida=carpeta_salida,
            visible=visible,
            max_filas=max_filas,
        )

    archivo_csv = Path(archivo_csv)

    if carpeta_salida is None:
        carpeta_salida = archivo_csv.parent
    else:
        carpeta_salida = Path(carpeta_salida)

    carpeta_salida.mkdir(exist_ok=True, parents=True)

    serial = _obtener_serial_del_csv(archivo_csv)
    nombre_base = f"prueba_de_transmision_{serial}" if serial else f"prueba_de_transmision_{archivo_csv.stem}"
    ruta_png = carpeta_salida / f"{nombre_base}.png"

    excel = None
    libro = None
    hoja = None
    rango = None

    try:
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = visible
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False
        excel.EnableEvents = False

        libro = excel.Workbooks.Open(str(archivo_csv.resolve()))
        hoja = libro.Worksheets(1)

        hoja.Cells.Font.Name = "Calibri"
        hoja.Cells.Font.Size = 18
        hoja.Cells.HorizontalAlignment = -4108
        hoja.Cells.VerticalAlignment = -4108
        hoja.Cells.WrapText = False
        hoja.Columns.AutoFit()
        hoja.Rows.AutoFit()

        rango = hoja.UsedRange
        ultima_fila = rango.Rows.Count
        ultima_columna = rango.Columns.Count

        if max_filas is not None:
            ultima_fila = min(max_filas, ultima_fila)

        rango = hoja.Range(hoja.Cells(1, 1), hoja.Cells(ultima_fila, ultima_columna))
        rango.CopyPicture(Appearance=1, Format=2)

        time.sleep(0.8)
        imagen = ImageGrab.grabclipboard()
        if imagen is None:
            raise RuntimeError("No fue posible obtener la imagen del portapapeles.")

        ruta_png.parent.mkdir(parents=True, exist_ok=True)
        imagen.save(ruta_png)

    finally:
        try:
            if libro is not None:
                libro.Close(False)
        except Exception:
            pass

        try:
            if excel is not None:
                excel.Quit()
        except Exception:
            pass

        gc.collect()
        time.sleep(0.5)

    return ruta_png