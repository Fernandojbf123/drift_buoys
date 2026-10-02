import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel
from services.timestamp_a_texto_espanol import *


# def validate_dataframe(df: pd.DataFrame, required_columns: list[str] | None = None, date_columns: list[str] | None = None, min_rows: int = 1) -> list[str]:
#     """Valida un DataFrame y devuelve una lista con mensajes de error.

#     - Comprueba que `df` sea un DataFrame y no esté vacío (si `min_rows` > 0).
#     - Verifica que existan las columnas en `required_columns`.
#     - Para cada columna en `date_columns` intenta parsear con formato DD/MM/YYYY y reporta filas con formato inválido.

#     Uso recomendado desde los getters:
#         errores = validate_dataframe(df, required_columns=[...], date_columns=[...])
#         if errores:
#             raise ValueError("; ".join(errores))
#     """
#     errors: list[str] = []
#     if not isinstance(df, pd.DataFrame):
#         errors.append("El objeto proporcionado no es un DataFrame")
#         return errors

#     if min_rows > 0 and df.shape[0] < min_rows:
#         errors.append(f"DataFrame tiene menos de {min_rows} filas (actual: {df.shape[0]})")

#     if required_columns:
#         for col in required_columns:
#             if col not in df.columns:
#                 errors.append(f"Falta la columna requerida: {col}")

#     if date_columns:
#         for col in date_columns:
#             if col not in df.columns:
#                 errors.append(f"Falta la columna de fecha: {col}")
#                 continue
#             parsed = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")
#             invalid_idx = parsed[parsed.isna()].index.tolist()
#             if len(invalid_idx) > 0:
#                 sample = invalid_idx[:5]
#                 errors.append(f"Formato de fecha inválido en columna '{col}' en filas: {sample} (se encontraron {len(invalid_idx)} entradas inválidas)")

#     return errors

def get_datos_de_despliegue(ruta_al_excel_de_despliegue: str, nombre_de_hoja: str, ):
    df_datos_despliegue = leer_excel(ruta_al_excel_de_despliegue, nombre_de_hoja=nombre_de_hoja, header=0)
    return df_datos_despliegue

def filtrar_df_datos_despliegue_por_orden_de_servicio(df_datos_despliegue: pd.DataFrame, orden_de_servicio: str, columna: str) -> pd.DataFrame:
    """ Filtra la orden de servicio en el DataFrame de datos de despliegue """
    
    if not orden_de_servicio:
        raise ValueError("No hay una orden de servicio configurada")
    
    df_datos_despliegue[columna] = df_datos_despliegue[columna].astype(str).str.strip().str.removesuffix(".0")
    df_filtrado = df_datos_despliegue[df_datos_despliegue[columna] == orden_de_servicio]
    return df_filtrado

def get_seriales_de_sondas(df_despliegue_filtrado: pd.DataFrame) -> list[str]:
    if df_despliegue_filtrado.empty:
        raise ValueError("El DataFrame filtrado está vacío, no se pueden obtener seriales de sondas")
    seriales_de_sondas = df_despliegue_filtrado["serial_de_sonda"].astype(str).str.strip().tolist()
    return seriales_de_sondas






def get_fecha_de_solicitud(df_despliegue_filtrado: pd.DataFrame):
    fecha_de_solicitud = df_despliegue_filtrado["fecha_de_solicitud"].iloc[0]
    return fecha_de_solicitud

def filtrar_df_datos_despliegue_por_orden_de_servicio_103(df_datos_despliegue: pd.DataFrame) -> pd.DataFrame:
    orden_de_servicio = get_orden_de_servicio_103()
    errores = validate_dataframe(df_datos_despliegue, required_columns=["OS_103"], min_rows=0)
    if errores:
        raise ValueError("Errores en DataFrame antes de filtrar por orden de servicio: " + "; ".join(errores))
    if not orden_de_servicio:
        raise ValueError("No hay una orden de servicio configurada")
    os_103 = df_datos_despliegue["OS_103"].astype("string").str.strip().str.removesuffix(".0")
    return df_datos_despliegue.loc[os_103 == orden_de_servicio].copy()

def get_numero_de_sondas(df_datos_despliegue: pd.DataFrame) -> int:
    numero_de_sondas = len(df_datos_despliegue)
    return numero_de_sondas

def get_fecha_inicio_vigencia(df_datos_despliegue: pd.DataFrame) -> pd.Timestamp:
    """Obtiene la fecha de inicio de vigencia como Timestamp."""
    fecha_inicio_vigencia = df_datos_despliegue["fecha_inicio_vigencia"].iloc[0]
    fecha_inicio_vigencia = pd.to_datetime(fecha_inicio_vigencia, format="%d/%m/%Y", errors="coerce")
    return fecha_inicio_vigencia

def get_fecha_inicio_vigencia_texto(df_datos_despliegue: pd.DataFrame) -> str:
    """Obtiene la fecha de inicio de vigencia en texto español."""
    fecha_inicio_vigencia = get_fecha_inicio_vigencia(df_datos_despliegue)
    return timestamp_a_texto_espanol(fecha=fecha_inicio_vigencia,mes_y_anio=False)

def get_dia_inicio_vigencia(df_datos_despliegue: pd.DataFrame) -> int:
    """Obtiene únicamente el día de la fecha de inicio de vigencia."""
    fecha_inicio_vigencia = get_fecha_inicio_vigencia(df_datos_despliegue)
    return fecha_inicio_vigencia.day

def get_fecha_final_vigencia(df_datos_despliegue: pd.DataFrame) -> str:
    fecha_inicio_vigencia = df_datos_despliegue["fecha_inicio_vigencia"].iloc[0]
    fecha_inicio_vigencia = pd.to_datetime(fecha_inicio_vigencia, format= "%d/%m/%Y", errors='coerce')
    fecha_final_vigencia = fecha_inicio_vigencia + pd.offsets.MonthEnd(0)
    fecha_final_vigencia = timestamp_a_texto_espanol(fecha = fecha_final_vigencia, mes_y_anio=False)
    return fecha_final_vigencia

def get_fecha_entrega(df_datos_despliegue: pd.DataFrame) -> str:
    
    fecha_inicio_vigencia = df_datos_despliegue["fecha_inicio_vigencia"].iloc[0]
    fecha_inicio_vigencia = pd.to_datetime(fecha_inicio_vigencia, format= "%d/%m/%Y", errors='coerce')
    fecha_entrega = fecha_inicio_vigencia + pd.DateOffset(months=1)
    fecha_entrega = timestamp_a_texto_espanol(fecha = fecha_entrega, mes_y_anio=False)
    return fecha_entrega

def get_fecha_inicio_vigencia_portada(
    df_datos_despliegue: pd.DataFrame
) -> str:
    fecha = get_fecha_inicio_vigencia(df_datos_despliegue)

    texto = timestamp_a_texto_espanol(
        fecha=fecha,
        mes_y_anio=False
    )

    # "01 de junio de 2026" -> "01 de junio"
    return texto.rsplit(" de ", 1)[0]

def get_mes_anio_portada(
    df_datos_despliegue: pd.DataFrame
) -> str:
    """
    Devuelve el mes y año de la fecha de inicio de vigencia en formato:
    'junio 2026'
    """

    fecha = get_fecha_inicio_vigencia(df_datos_despliegue)

    return timestamp_a_texto_espanol(fecha=fecha, mes_y_anio=True).replace(" de ", " ", 1).capitalize()

