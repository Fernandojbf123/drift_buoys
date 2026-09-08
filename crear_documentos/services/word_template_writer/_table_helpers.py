"""
Internal helper functions for table manipulation in Word templates.

This module contains low-level functions for filling Word tables with DataFrame data,
including support for MultiIndex DataFrames, merged cells, and flexible styling.

Private module - Not intended for direct external use.
Import from the public API in api.py instead.
"""

from copy import deepcopy
from matplotlib import table
import pandas as pd
from typing import Union, Optional, Dict, List, Tuple
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from .schemas_helpers import EstilosTabla, OpcionesTabla
from ._table_styling import apply_cell_style, apply_row_height, apply_table_borders
from docx.oxml import OxmlElement


# ===== NORMALIZATION FUNCTIONS =====

def _normalize_input_to_dataframe(datos: Union[pd.DataFrame, dict]) -> pd.DataFrame:
    """
    Normaliza la entrada a DataFrame.
    
    Args:
        datos: DataFrame o diccionario de columnas
    
    Returns:
        DataFrame normalizado
    
    Raises:
        ValueError: Si los datos están vacíos o no son válidos
    """
    if isinstance(datos, pd.DataFrame):
        df = datos
    elif isinstance(datos, dict):
        df = pd.DataFrame(datos)
    else:
        raise ValueError(
            f"datos debe ser DataFrame o diccionario. Recibido: {type(datos)}"
        )
    
    if df.empty:
        raise ValueError("El DataFrame está vacío. No hay datos para insertar.")
    
    return df


def _normalize_config_estilos(config_estilos: Union[EstilosTabla, dict, None], doc) -> dict:
    """
    Normaliza la configuración de estilos a diccionario.
    
    Args:
        config_estilos: Objeto EstilosTabla, dict, o None
        doc: Objeto Document (para crear EstilosTabla por defecto si es None)
    
    Returns:
        Diccionario de configuración normalizado
    """
    if config_estilos is None:
        # Crear EstilosTabla por defecto
        config_obj = EstilosTabla(doc)
        return config_obj.to_dict()
    elif isinstance(config_estilos, EstilosTabla):
        return config_estilos.to_dict()
    elif isinstance(config_estilos, dict):
        # Validar estructura básica del diccionario
        required_keys = ["por_defecto", "por_columna", "por_fila", "por_celda"]
        if not all(key in config_estilos for key in required_keys):
            raise ValueError(
                f"Diccionario config_estilos debe contener las claves: {required_keys}"
            )
        return config_estilos
    else:
        raise ValueError(
            f"config_estilos debe ser EstilosTabla, dict o None. Recibido: {type(config_estilos)}"
        )


def _normalize_opciones_tabla(opciones_tabla: Union[OpcionesTabla, dict, None]) -> dict:
    """
    Normaliza las opciones de tabla a diccionario.
    
    Args:
        opciones_tabla: Objeto OpcionesTabla, dict, o None
    
    Returns:
        Diccionario de opciones normalizado
    """
    if opciones_tabla is None:
        # Crear OpcionesTabla por defecto
        opciones_obj = OpcionesTabla()
        return opciones_obj.to_dict()
    elif isinstance(opciones_tabla, OpcionesTabla):
        return opciones_tabla.to_dict()
    elif isinstance(opciones_tabla, dict):
        # Agregar valores por defecto para claves faltantes
        defaults = OpcionesTabla().to_dict()
        return {**defaults, **opciones_tabla}
    else:
        raise ValueError(
            f"opciones_tabla debe ser OpcionesTabla, dict o None. Recibido: {type(opciones_tabla)}"
        )


# ===== TABLE SEARCH FUNCTIONS =====

def _find_table_with_marker(doc, nombre_marcador: str) -> Tuple[object, int, int]:
    """
    Busca una tabla que contenga el marcador especificado.
    
    Args:
        doc: Objeto Document
        nombre_marcador: Marcador a buscar (ej: "<<table_sondas>>")
    
    Returns:
        Tupla (tabla, fila_marcador, columna_marcador)
    
    Raises:
        ValueError: Si no se encuentra el marcador
    """
    for table in doc.tables:
        # Buscar en todas las celdas de la tabla
        for row_idx, row in enumerate(table.rows):
            for col_idx, cell in enumerate(row.cells):
                if nombre_marcador in cell.text:
                    return (table, row_idx, col_idx)
    
    raise ValueError(
        f"No se encontró el marcador '{nombre_marcador}' en ninguna tabla del documento."
    )


def _disable_row_header_repeat(row):
    """
    Desactiva la propiedad de repetición de encabezado en una fila.
    
    En Word, las filas de encabezado tienen la propiedad tblHeader que hace
    que se repitan en cada salto de página. Esta función elimina esa propiedad.
    
    Args:
        row: Objeto Row de python-docx
    """
    tr = row._element
    trPr = tr.get_or_add_trPr()
    
    # Buscar y eliminar el elemento tblHeader si existe
    tblHeader = trPr.find(qn('w:tblHeader'))
    if tblHeader is not None:
        trPr.remove(tblHeader)


def _delete_row(table, row_idx: int):
    """
    Elimina una fila de la tabla manipulando el XML directamente.
    
    python-docx no proporciona una API directa para eliminar filas,
    por lo que se debe manipular el XML.
    
    Args:
        table: Objeto Table de python-docx
        row_idx: Índice de la fila a eliminar (0-based)
    """
    tbl = table._element
    tr = table.rows[row_idx]._element
    tbl.remove(tr)


# ===== STYLE MERGING FUNCTIONS =====

def _merge_style_config(config: dict, row_idx: int, col_idx: int) -> dict:
    """
    Combina la configuración de estilos para una celda específica.
    
    Resuelve la jerarquía: celda > fila > columna > defecto
    
    Args:
        config: Diccionario de configuración completo
        row_idx: Índice de fila (0-based)
        col_idx: Índice de columna (0-based)
    
    Returns:
        Diccionario con configuración mergeada para esta celda
    """
    merged = {}
    
    # 1. Aplicar configuración por defecto
    if "por_defecto" in config:
        merged.update(config["por_defecto"])
    
    # 2. Aplicar configuración de columna (sobrescribe defecto)
    if "por_columna" in config and col_idx in config["por_columna"]:
        merged.update(config["por_columna"][col_idx])
    
    # 3. Aplicar configuración de fila (sobrescribe columna y defecto)
    if "por_fila" in config and row_idx in config["por_fila"]:
        merged.update(config["por_fila"][row_idx])
    
    # 4. Aplicar configuración de celda (sobrescribe todo)
    if "por_celda" in config and (row_idx, col_idx) in config["por_celda"]:
        merged.update(config["por_celda"][(row_idx, col_idx)])
    
    return merged


# ===== MULTIINDEX FLATTENING FUNCTIONS =====

def _flatten_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplana un DataFrame con MultiIndex en filas o columnas.
    
    Args:
        df: DataFrame potencialmente con MultiIndex
    
    Returns:
        DataFrame aplanado con índice simple
    """
    df_flat = df.copy()
    
    # Aplanar MultiIndex en filas (índice)
    if isinstance(df_flat.index, pd.MultiIndex):
        df_flat = df_flat.reset_index()
    
    # Aplanar MultiIndex en columnas
    if isinstance(df_flat.columns, pd.MultiIndex):
        # Unir niveles con '_'
        df_flat.columns = ['_'.join(map(str, col)).strip('_') for col in df_flat.columns]
    
    return df_flat


# ===== MERGED CELLS FUNCTIONS =====

def _detect_merge_regions_vertical(
    df: pd.DataFrame,
    columnas_para_merge: Optional[List[int]]
) -> List[Tuple[int, int, int]]:
    """
    Detecta regiones de celdas a combinar verticalmente.
    
    Busca valores consecutivos repetidos en columnas especificadas.
    
    Args:
        df: DataFrame con los datos
        columnas_para_merge: Lista de índices de columnas o None (todas)
    
    Returns:
        Lista de tuplas (fila_inicio, fila_fin, columna)
    """
    regions = []
    
    # Determinar qué columnas analizar
    if columnas_para_merge is None:
        cols_to_check = range(len(df.columns))
    else:
        cols_to_check = columnas_para_merge
    
    for col_idx in cols_to_check:
        if col_idx >= len(df.columns):
            continue  # Saltar si el índice está fuera de rango
        
        col_name = df.columns[col_idx]
        values = df[col_name].tolist()
        
        # Detectar secuencias de valores repetidos
        start_idx = 0
        while start_idx < len(values):
            current_value = values[start_idx]
            end_idx = start_idx
            
            # Contar cuántas filas consecutivas tienen el mismo valor
            while end_idx + 1 < len(values) and values[end_idx + 1] == current_value:
                end_idx += 1
            
            # Si hay al menos 2 celdas consecutivas con el mismo valor, agregar región
            if end_idx > start_idx:
                regions.append((start_idx, end_idx, col_idx))
            
            start_idx = end_idx + 1
    
    return regions


def _apply_merged_cells_vertical(table, regions: List[Tuple[int, int, int]], fila_inicio_datos: int):
    """
    Aplica merged cells verticales a la tabla.
    
    Args:
        table: Objeto Table de python-docx
        regions: Lista de tuplas (fila_inicio, fila_fin, columna)
        fila_inicio_datos: Índice de la fila donde inician los datos (después del marcador)
    """
    for start_row, end_row, col in regions:
        # Ajustar índices de fila para la tabla real (sumar fila_inicio_datos)
        table_start_row = fila_inicio_datos + start_row
        table_end_row = fila_inicio_datos + end_row
        
        try:
            # Obtener celdas a combinar
            cell_start = table.cell(table_start_row, col)
            cell_end = table.cell(table_end_row, col)
            
            # Combinar celdas
            cell_start.merge(cell_end)
        except Exception as e:
            # Si falla el merge, continuar con las demás (no es crítico)
            print(f"Advertencia: No se pudo combinar celdas ({start_row}-{end_row}, {col}): {e}")


# ===== MAIN FILL TABLE FUNCTION =====

def fill_table(
    doc,
    nombre_marcador: str,
    datos: Union[pd.DataFrame, dict],
    config_estilos: Union[EstilosTabla, dict, None] = None,
    opciones_tabla: Union[OpcionesTabla, dict, None] = None
):
    """
    Rellena una tabla dinámicamente buscando un marcador e insertando datos de un DataFrame.
    
    Esta es la función principal refactorizada que orquesta todo el proceso.
    
    Args:
        doc: Objeto Document de python-docx
        nombre_marcador: Marcador a buscar en la tabla (ej: "<<table_sondas>>")
        datos: DataFrame o diccionario con los datos a insertar
        config_estilos: Configuración de estilos (objeto EstilosTabla, dict, o None)
        opciones_tabla: Opciones de tabla (objeto OpcionesTabla, dict, o None)
    
    Returns:
        Objeto Document modificado
    
    Raises:
        ValueError: Si hay errores en la configuración o datos
    
    Flujo:
        1. Normalizar inputs (DataFrame, config, opciones)
        2. Buscar tabla con marcador
        3. Aplanar DataFrame si tiene MultiIndex
        4. Insertar datos fila por fila
        5. Detectar y aplicar merged cells (si está activado)
        6. Aplicar estilos a cada celda
        7. Eliminar fila marcador (si está activado)
    """
    # ===== PASO 1: NORMALIZAR INPUTS =====
    df = _normalize_input_to_dataframe(datos)
    config = _normalize_config_estilos(config_estilos, doc)
    opciones = _normalize_opciones_tabla(opciones_tabla)
    
    # ===== PASO 2: BUSCAR TABLA CON MARCADOR =====
    table, fila_marcador, col_marcador = _find_table_with_marker(doc, nombre_marcador)
    apply_table_borders(table)
   

    # ===== BUG FIX 1: DESACTIVAR REPETICIÓN DE ENCABEZADO EN FILA MARCADOR =====
    # La fila del marcador puede tener la propiedad tblHeader (encabezado repetible)
    # que hace que se repita en cada salto de página. Debemos desactivarla.
    _disable_row_header_repeat(table.rows[fila_marcador])
    
    # ===== PASO 3: APLANAR DATAFRAME SI TIENE MULTIINDEX =====
    if opciones["aplanar_multiindex"]:
        if isinstance(df.index, pd.MultiIndex) or isinstance(df.columns, pd.MultiIndex):
            df = _flatten_dataframe(df)
    else:
        # Si no se debe aplanar y tiene MultiIndex, lanzar error
        if isinstance(df.index, pd.MultiIndex) or isinstance(df.columns, pd.MultiIndex):
            raise ValueError(
                "El DataFrame tiene MultiIndex pero 'aplanar_multiindex' está desactivado. "
                "Active la opción o aplane el DataFrame manualmente con df.reset_index()."
            )
    
    # ===== PASO 4: VALIDAR QUE HAY SUFICIENTES COLUMNAS =====
    num_cols_df = len(df.columns)
    num_cols_table = len(table.columns)
    if num_cols_df > num_cols_table:
        raise ValueError(
            f"El DataFrame tiene {num_cols_df} columnas pero la tabla solo tiene {num_cols_table}. "
            "Ajuste la plantilla o el DataFrame."
        )
    
    # ===== PASO 5: AGREGAR FILAS NECESARIAS =====
    # Calcular cuántas filas necesitamos agregar
    # Si eliminamos el marcador: usamos esa fila + las que siguen
    # Si NO eliminamos: necesitamos todas las filas de datos desde el marcador
    filas_necesarias = len(df)
    filas_actuales_disponibles = len(table.rows) - fila_marcador  # Incluye fila marcador
    
    if filas_necesarias > filas_actuales_disponibles:
        # Agregar solo las filas faltantes (BUG FIX 2: cálculo corregido)
        filas_a_agregar = filas_necesarias - filas_actuales_disponibles
        for _ in range(filas_a_agregar):
            table.add_row()
    
    # ===== PASO 6: DETECTAR REGIONES DE MERGE (antes de insertar datos) =====
    # BUG FIX 3: Detectar merge ANTES de insertar texto para evitar duplicados
    merge_regions = []
    if opciones["detectar_merge"]:
        merge_regions = _detect_merge_regions_vertical(df, opciones["columnas_para_merge"])
    
    # Crear un set de celdas que NO deben recibir texto (segunda celda en adelante de merge)
    celdas_merged_secundarias = set()
    for start_row, end_row, col in merge_regions:
        # Agregar todas las celdas excepto la primera de cada región
        for row_idx in range(start_row + 1, end_row + 1):
            celdas_merged_secundarias.add((row_idx, col))
    
    # ===== PASO 7: INSERTAR DATOS FILA POR FILA =====
    # Siempre empezamos a escribir desde la fila del marcador
    fila_inicio_datos = fila_marcador
    
    for df_row_idx, (_, df_row) in enumerate(df.iterrows()):
        # Índice de fila en la tabla (después del marcador)
        table_row_idx = fila_inicio_datos + df_row_idx
        
        # Insertar datos en cada columna
        for df_col_idx, col_name in enumerate(df.columns):
            # BUG FIX 3: No escribir en celdas secundarias de regiones mergeadas
            if (df_row_idx, df_col_idx) not in celdas_merged_secundarias:
                cell = table.cell(table_row_idx, df_col_idx)
                cell.text = str(df_row[col_name])
    
    # ===== PASO 8: APLICAR MERGED CELLS =====
    if opciones["detectar_merge"]:
        _apply_merged_cells_vertical(table, merge_regions, fila_inicio_datos)
    
    # ===== PASO 9: APLICAR ESTILOS A CADA CELDA =====
    for df_row_idx in range(len(df)):
        table_row_idx = fila_inicio_datos + df_row_idx
        row = table.rows[table_row_idx]
        
        # Aplicar altura de fila
        altura_fila = config["por_defecto"].get("altura_fila")
        if altura_fila:
            apply_row_height(row, altura_fila)
        
        # Aplicar estilos a cada celda
        # BUG FIX 3: Solo aplicar estilos a celdas que no son secundarias en merge
        for df_col_idx in range(len(df.columns)):
            if (df_row_idx, df_col_idx) not in celdas_merged_secundarias:
                cell = table.cell(table_row_idx, df_col_idx)
                merged_config = _merge_style_config(config, df_row_idx, df_col_idx)
                apply_cell_style(cell, doc, config, df_row_idx, df_col_idx, merged_config)
    
    # ===== PASO 10: ELIMINAR FILAS SOBRANTES AL FINAL =====
    # BUG FIX 2: Eliminar filas vacías que puedan quedar al final de la tabla
    # Esto puede ocurrir si la plantilla tiene filas preexistentes o si add_row()
    # creó filas de más
    ultima_fila_con_datos = fila_inicio_datos + len(df) - 1
    total_filas = len(table.rows)
    
    # Eliminar todas las filas después de la última fila con datos
    # Nota: Eliminamos de atrás hacia adelante para evitar problemas de índices
    for row_idx in range(total_filas - 1, ultima_fila_con_datos, -1):
        _delete_row(table, row_idx)
    
    
    return doc


def aux_insertar_tabla_con_titulo(paragraph, numero="1", titulo="Relación de equipos", bookmark_name="_Ref_Tabla_1"):
    """
    Crea una línea tipo:
    Tabla 1. Relación de equipos

    con el numero 1 dentro de un bookmark para referencia cruzada.
    """
    # Texto fijo
    paragraph.add_run("Tabla ")

    # Bookmark alrededor del número
    bookmark_start = OxmlElement("w:bookmarkStart")
    bookmark_start.set(qn("w:id"), "1")
    bookmark_start.set(qn("w:name"), bookmark_name)
    paragraph._element.append(bookmark_start)

    paragraph.add_run(numero)

    bookmark_end = OxmlElement("w:bookmarkEnd")
    bookmark_end.set(qn("w:id"), "1")
    paragraph._element.append(bookmark_end)

    paragraph.add_run(f". {titulo}")
    
def aux_insertar_referencia_tabla(paragraph, bookmark_name="_Ref_Tabla_1"):
    run = paragraph.add_run()
    fldChar_begin = OxmlElement("w:fldChar")
    fldChar_begin.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = f" REF {bookmark_name} \\h "

    fldChar_separate = OxmlElement("w:fldChar")
    fldChar_separate.set(qn("w:fldCharType"), "separate")

    text_run = OxmlElement("w:r")
    text_elem = OxmlElement("w:t")
    text_elem.text = "XX"
    text_run.append(text_elem)

    fldChar_end = OxmlElement("w:fldChar")
    fldChar_end.set(qn("w:fldCharType"), "end")

    run._element.append(fldChar_begin)
    run._element.append(instrText)
    run._element.append(fldChar_separate)
    run._element.append(text_run)
    run._element.append(fldChar_end)
    
    from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def agregar_campo_word(parrafo, instruccion):
    """
    Inserta un campo de Word.

    Ejemplos:
        { SEQ Tabla \\* ARABIC }
        { REF tabla_1 }
    """

    run = parrafo.add_run()

    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")

    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = f" {instruccion} "

    fld_separate = OxmlElement("w:fldChar")
    fld_separate.set(qn("w:fldCharType"), "separate")

    # Valor provisional que Word puede mostrar antes de actualizar campos
    run_resultado = OxmlElement("w:r")
    texto_resultado = OxmlElement("w:t")
    texto_resultado.text = "1"
    run_resultado.append(texto_resultado)

    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr_text)
    run._r.append(fld_separate)
    run._r.append(run_resultado)
    run._r.append(fld_end)

    return run


def activar_actualizacion_de_campos(doc):
    """
    Hace que Word actualice los campos al abrir el documento.
    """

    settings = doc.settings.element

    update_fields = settings.find(qn("w:updateFields"))

    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)

    update_fields.set(qn("w:val"), "true")

def insertar_caption_tabla(
    parrafo,
    bookmark,
    texto_titulo,
    bookmark_id
):
    """
    Inserta:

        Tabla { SEQ Tabla }: texto...

    y crea un bookmark sobre "Tabla {SEQ Tabla}".
    """

    # "Tabla "
    parrafo.add_run("Tabla ")

    # El bookmark debe contener solo el número, igual que en las figuras.
    bookmark_start = OxmlElement("w:bookmarkStart")
    bookmark_start.set(qn("w:id"), str(bookmark_id))
    bookmark_start.set(qn("w:name"), bookmark)
    parrafo._p.append(bookmark_start)

    # { SEQ Tabla }
    agregar_campo_word(
        parrafo,
        r"SEQ Tabla \* ARABIC"
    )

    # Bookmark END
    bookmark_end = OxmlElement("w:bookmarkEnd")
    bookmark_end.set(qn("w:id"), str(bookmark_id))

    parrafo._p.append(bookmark_end)

    # Texto del título
    parrafo.add_run(f". {texto_titulo}")


def reemplazar_titulo_tabla_en_run(
    parrafo,
    run,
    marcador,
    bookmark,
    texto_titulo,
    bookmark_id
):
    """Inserta un caption donde está el marcador sin borrar el párrafo."""
    texto = run.text or ""
    posicion = texto.find(marcador)
    if posicion == -1:
        return False

    texto_antes = texto[:posicion]
    texto_despues = texto[posicion + len(marcador):]
    run.text = texto_antes

    parrafo_temporal = OxmlElement("w:p")
    parrafo_caption = Paragraph(parrafo_temporal, parrafo._parent)
    insertar_caption_tabla(
        parrafo=parrafo_caption,
        bookmark=bookmark,
        texto_titulo=texto_titulo,
        bookmark_id=bookmark_id
    )

    elementos_caption = list(parrafo_temporal)
    ancla = run._r
    for elemento in elementos_caption:
        ancla.addnext(elemento)
        ancla = elemento

    if texto_despues:
        run_despues = OxmlElement("w:r")
        if run._r.rPr is not None:
            run_despues.append(deepcopy(run._r.rPr))
        texto_despues_xml = OxmlElement("w:t")
        texto_despues_xml.text = texto_despues
        run_despues.append(texto_despues_xml)
        ancla.addnext(run_despues)

    return True
    
def insertar_referencia_tabla(parrafo, bookmark):
    run_referencia = parrafo.add_run("Tabla ")
    run_campo = agregar_campo_word(
        parrafo,
        f"REF {bookmark} \\h"
    )

    # Mantener el prefijo y el campo REF en un único run permite moverlos
    # juntos a la posición exacta del marcador original.
    for elemento in list(run_campo._r):
        run_referencia._r.append(elemento)
    run_campo._r.getparent().remove(run_campo._r)

    return run_referencia


def reemplazar_referencia_tabla_en_run(parrafo, run, marcador, bookmark):
    """Inserta el campo REF en la posición exacta del marcador dentro del run."""
    texto = run.text
    posicion = texto.find(marcador)
    if posicion == -1:
        return False

    texto_antes = texto[:posicion]
    texto_despues = texto[posicion + len(marcador):]
    run.text = texto_antes

    run_referencia = insertar_referencia_tabla(
        parrafo=parrafo,
        bookmark=bookmark
    )
    run._r.addnext(run_referencia._r)

    if texto_despues:
        run_despues = parrafo.add_run(texto_despues)
        run_referencia._r.addnext(run_despues._r)

    return True


def reemplazar_referencia_tabla_en_parrafo(parrafo, marcador, bookmark):
    """Reemplaza una referencia aunque el marcador cruce varios runs."""
    runs = parrafo.runs
    texto_completo = "".join(run.text or "" for run in runs)
    inicio = texto_completo.find(marcador)
    if inicio == -1:
        return False

    fin = inicio + len(marcador)
    posiciones = []
    offset = 0

    for indice, run_actual in enumerate(runs):
        texto_run = run_actual.text or ""
        siguiente_offset = offset + len(texto_run)
        if siguiente_offset > inicio and offset < fin:
            posiciones.append((indice, offset, siguiente_offset))
        offset = siguiente_offset

    primer_indice, primer_offset, _ = posiciones[0]
    ultimo_indice, _, ultimo_fin = posiciones[-1]
    primer_run = runs[primer_indice]
    ultimo_run = runs[ultimo_indice]

    texto_antes = (primer_run.text or '')[:inicio - primer_offset]
    inicio_ultimo = ultimo_fin - len(ultimo_run.text or '')
    texto_despues = (ultimo_run.text or '')[fin - inicio_ultimo:]

    if primer_indice == ultimo_indice:
        primer_run.text = texto_antes
    else:
        primer_run.text = texto_antes
        for indice, _, _ in posiciones[1:-1]:
            runs[indice].text = ''
        ultimo_run.text = texto_despues

    run_referencia = insertar_referencia_tabla(
        parrafo=parrafo,
        bookmark=bookmark
    )
    primer_run._r.addnext(run_referencia._r)

    if primer_indice == ultimo_indice and texto_despues:
        run_despues = OxmlElement("w:r")
        if primer_run._r.rPr is not None:
            run_despues.append(deepcopy(primer_run._r.rPr))
        texto_despues_xml = OxmlElement("w:t")
        texto_despues_xml.text = texto_despues
        run_despues.append(texto_despues_xml)
        run_referencia._r.addnext(run_despues)

    return True

def obtener_todos_los_parrafos(doc):
    """
    Devuelve todos los párrafos del documento,
    incluyendo los que están dentro de tablas.
    """

    # Párrafos normales
    for parrafo in doc.paragraphs:
        yield parrafo

    # Párrafos dentro de tablas
    for tabla in doc.tables:
        yield from obtener_parrafos_de_tabla(tabla)

    # Párrafos dentro de cuadros de texto
    partes_vistas = set()
    partes = [doc.element]

    for section in doc.sections:
        partes.extend([
            section.header._element,
            section.footer._element
        ])

    for part in doc.part.package.parts:
        elemento = getattr(part, "_element", None)
        if elemento is not None:
            partes.append(elemento)

    for parte in partes:
        identificador = id(parte)
        if identificador in partes_vistas:
            continue
        partes_vistas.add(identificador)

        for nodo in parte.iter():
            if nodo.tag.split("}")[-1] != "txbxContent":
                continue

            for nodo_parrafo in nodo.iter():
                if nodo_parrafo.tag.split("}")[-1] == "p":
                    yield Paragraph(nodo_parrafo, nodo)


def obtener_parrafos_de_tabla(tabla):
    """
    Recorre recursivamente una tabla y devuelve
    los párrafos de sus celdas, incluyendo tablas
    anidadas.
    """

    for fila in tabla.rows:

        for celda in fila.cells:

            for parrafo in celda.paragraphs:
                yield parrafo

            # Tablas anidadas
            for tabla_anidada in celda.tables:
                yield from obtener_parrafos_de_tabla(tabla_anidada)


def limpiar_parrafo(parrafo):
    """
    Elimina todos los runs del párrafo.
    """

    for run in list(parrafo.runs):
        run._element.getparent().remove(run._element)


def procesar_titulos_y_referencias(
    doc,
    diccionario_de_reemplazos):
    """Procesa:
        <<titulo_tabla_1>>
        <<ref_tabla_1>>
    creando campos SEQ, REF y bookmarks de Word.
    """
    bookmark_id = 1000

    for variable, config in diccionario_de_reemplazos.items():
        # =====================================================
        # TÍTULOS
        # =====================================================
        if variable.startswith("<<titulo_tabla_"):
            numero = (
                variable
                .replace("<<titulo_tabla_", "")
                .replace(">>", "")
            )

            bookmark = f"tabla_{numero}"

            texto_titulo = config["texto"]

            encontrado = False

            for parrafo in obtener_todos_los_parrafos(doc):

                if variable in parrafo.text:
                    for run in parrafo.runs:
                        if reemplazar_titulo_tabla_en_run(
                            parrafo=parrafo,
                            run=run,
                            marcador=variable,
                            bookmark=bookmark,
                            texto_titulo=texto_titulo,
                            bookmark_id=bookmark_id
                        ):
                            bookmark_id += 1
                            encontrado = True
                            break
                    if encontrado:
                        break

            if not encontrado:
                print(
                    f"ADVERTENCIA: no se encontró "
                    f"'{variable}' en la plantilla."
                )

        # =====================================================
        # REFERENCIAS
        # =====================================================

        elif variable.startswith("<<ref_tabla_"):

            numero = (
                variable
                .replace("<<ref_tabla_", "")
                .replace(">>", "")
            )

            bookmark = f"tabla_{numero}"

            encontrado = False

            for parrafo in obtener_todos_los_parrafos(doc):

                if variable in parrafo.text:

                    if reemplazar_referencia_tabla_en_parrafo(
                        parrafo=parrafo,
                        marcador=variable,
                        bookmark=bookmark
                    ):
                        encontrado = True
            if not encontrado:
                print(
                    f"ADVERTENCIA: no se encontró "
                    f"'{variable}' en la plantilla."
                )

    activar_actualizacion_de_campos(doc)
