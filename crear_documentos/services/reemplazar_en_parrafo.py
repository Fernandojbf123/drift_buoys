from genericpath import exists

from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


"""
Este módulo contiene funciones para reemplazar marcadores de posición en párrafos de Word, incluyendo la inserción de imágenes con o sin títulos.
Conceptos clave:
paragraph - Un párrafo en Word, que puede contener múltiples runs.
run - Es un fragmento de texto dentro de un párrafo que comparte el mismo formato.
Un párrafo puede tener múltiples runs con diferentes formatos.
ejemplo: "El valor es <<valor>>" podría estar dividido en 3 runs: ["El valor es ", "<<valor>>", ""]

"""

def insertar_parrafo_despues(paragraph, texto="", centrado=False):
    """Inserta un nuevo párrafo después del párrafo dado usando manipulación XML.
    
    Args:
        paragraph: El párrafo después del cual insertar.
        texto: El texto del nuevo párrafo (opcional).
        centrado: Si True, centra el texto del párrafo.
    
    Returns:
        El elemento XML del nuevo párrafo creado.
    """
    # Obtener el elemento del párrafo actual
    p_element = paragraph._element
    # Obtener el elemento padre
    parent = p_element.getparent()
    # Crear un nuevo elemento de párrafo
    nuevo_p = OxmlElement('w:p')
    
    # Si necesita estar centrado
    if centrado:
        pPr = OxmlElement('w:pPr')
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'center')
        pPr.append(jc)
        nuevo_p.append(pPr)
    
    # Si hay texto, agregarlo
    if texto:
        run = OxmlElement('w:r')
        text_elem = OxmlElement('w:t')
        text_elem.text = texto
        run.append(text_elem)
        nuevo_p.append(run)
    
    # Insertar el nuevo párrafo después del actual
    parent.insert(parent.index(p_element) + 1, nuevo_p)
    
    return nuevo_p


def crear_pie_de_figura(parent, indice, titulo, bookmark_name=None):
    """Crea un párrafo con pie de figura válido para Word con estilo Caption, campo SEQ y bookmark.
    
    Args:
        parent: El elemento padre XML donde insertar
        indice: Posición donde insertar
        titulo: Texto descriptivo de la figura
        bookmark_name: Nombre del bookmark para referencias cruzadas (opcional, se genera automático si None)
    
    Returns:
        Tupla (elemento XML del párrafo creado, nombre del bookmark)
    """
    # Generar nombre de bookmark si no se proporciona
    if bookmark_name is None:
        # Usar los primeros 30 caracteres del título, reemplazando espacios y caracteres especiales
        bookmark_name = f"_Ref_Fig_{titulo[:30].replace(' ', '_').replace(',', '').replace('.', '')}"
    
    # Generar ID único para el bookmark basado en el hash del nombre
    bookmark_id = str(abs(hash(bookmark_name)) % 1000000)
    
    # Crear párrafo con estilo Caption
    nuevo_p = OxmlElement('w:p')
    
    # Propiedades del párrafo (centrado + estilo Caption)
    pPr = OxmlElement('w:pPr')
    
    # Aplicar estilo "Caption"
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), 'Caption')
    pPr.append(pStyle)
    
    # Centrado
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    
    nuevo_p.append(pPr)
    
    # Agregar bookmark start al inicio del párrafo
    bookmark_start = OxmlElement('w:bookmarkStart')
    bookmark_start.set(qn('w:id'), bookmark_id)
    bookmark_start.set(qn('w:name'), bookmark_name)
    nuevo_p.append(bookmark_start)
    
    # Run para "Figura "
    run1 = OxmlElement('w:r')
    text1 = OxmlElement('w:t')
    text1.text = 'Figura '
    run1.append(text1)
    nuevo_p.append(run1)
    
    # Campo SEQ para numeración automática
    run_seq = OxmlElement('w:r')
    
    # Inicio del campo
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    run_seq.append(fldChar_begin)
    
    # Instrucción SEQ
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' SEQ Figura \\* ARABIC '
    run_seq.append(instrText)
    
    # Fin del campo
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    run_seq.append(fldChar_end)
    
    nuevo_p.append(run_seq)
    
    # Run para el texto descriptivo
    run2 = OxmlElement('w:r')
    text2 = OxmlElement('w:t')
    text2.set(qn('xml:space'), 'preserve')
    text2.text = f'. {titulo}'
    run2.append(text2)
    nuevo_p.append(run2)
    
    # Agregar bookmark end al final del párrafo
    bookmark_end = OxmlElement('w:bookmarkEnd')
    bookmark_end.set(qn('w:id'), bookmark_id)
    nuevo_p.append(bookmark_end)
    
    # Insertar en el documento
    parent.insert(indice, nuevo_p)
    
    return nuevo_p, bookmark_name


def insertar_referencia_cruzada(paragraph, nombre_bookmark, texto_antes="Figura", mostrar_numero=True):
    """Inserta una referencia cruzada a una figura en un párrafo.
    
    Args:
        paragraph: El párrafo donde insertar la referencia (objeto Paragraph)
        nombre_bookmark: Nombre del bookmark de la figura a referenciar
        texto_antes: Texto a mostrar antes del número (default: "Figura")
        mostrar_numero: Si True, muestra el número de la figura; si False, solo el bookmark
    
    Ejemplo de uso:
        # Para: "Como se muestra en la Figura 3"
        p = doc.add_paragraph("Como se muestra en la ")
        insertar_referencia_cruzada(p, "_Ref_Fig_Mi_Figura", "Figura")
    """
    # Agregar texto antes si se proporciona
    if texto_antes:
        run_texto = paragraph.add_run(texto_antes + " ")
    
    # Crear el run para el campo REF
    run = paragraph.add_run()
    
    # Crear el campo REF para la figura
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    # \r muestra solo el número de secuencia (SEQ), \h hace el campo clickable (hyperlink)
    if mostrar_numero:
        instrText.text = f' REF {nombre_bookmark} \\h '
    else:
        instrText.text = f' REF {nombre_bookmark} \\r \\h '
    
    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    
    # Texto por defecto (se actualizará en Word con F9)
    text_run = OxmlElement('w:r')
    text_elem = OxmlElement('w:t')
    text_elem.text = "XX"  # Placeholder que Word actualizará
    text_run.append(text_elem)
    
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    
    # Agregar elementos al run
    run._element.append(fldChar_begin)
    run._element.append(instrText)
    run._element.append(fldChar_separate)
    run._element.append(text_run)
    run._element.append(fldChar_end)


def aux_insertar_figura_sin_titulo(paragraph, key, lista_figuras):
    """Inserta imágenes en un párrafo de Word SIN título/Caption.
    
    Args:
        paragraph: El párrafo del documento Word donde se buscará el marcador.
        key: El marcador de posición a buscar (por ejemplo, "<<fig_ejecucion_campania>>").
        lista_figuras: Lista de diccionarios con keys "ruta", "titulo", "tamanio", "bookmark".
                      Para figuras sin título, titulo y bookmark deben ser "".
    
    Returns:
        True si se insertaron las imágenes, False si no se encontró el marcador.
        
    Ejemplo de uso:
        lista_figuras = [
            {"ruta": "img1.png", "titulo": "", "tamanio": 6, "bookmark": ""},
            {"ruta": "img2.png", "titulo": "", "tamanio": 5, "bookmark": ""}
        ]
    """
    full_text = "".join(run.text for run in paragraph.runs)
    
    if key not in full_text:
        return False
    
    # Limpiar el párrafo (borrar todos los runs)
    for run in paragraph.runs:
        run.text = ""
    
    # Obtener referencias para inserción
    p_element = paragraph._element
    parent = p_element.getparent()
    indice_base = parent.index(p_element)
    
    # Insertar todas las figuras sin título
    offset = 0
    for idx, item in enumerate(lista_figuras):
        ruta = item.get("ruta", "")
        ancho = item.get("tamanio", 6)
        
        # Si es la primera imagen, usar el párrafo actual
        if offset == 0:
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
            if exists(ruta):
                run.add_picture(ruta, width=Inches(ancho))
            offset = 1
        else:
            # Crear nuevo párrafo para imagen
            nuevo_p_img = OxmlElement('w:p')
            parent.insert(indice_base + offset, nuevo_p_img)
            # Convertir a Paragraph para poder agregar imagen
            para_img = Paragraph(nuevo_p_img, paragraph._parent)
            if exists(ruta):
                para_img.add_run().add_picture(ruta, width=Inches(ancho))
            offset += 1
        
        # Salto de línea después de cada imagen
        nuevo_p_salto = OxmlElement('w:p')
        parent.insert(indice_base + offset, nuevo_p_salto)
        offset += 1
    
    return True


def aux_insertar_figuras_con_titulo(paragraph, key, lista_figuras):
    """Inserta MÚLTIPLES imágenes con pies de figura válidos (Caption + SEQ + Bookmarks).
    
    Args:
        paragraph: El párrafo del documento Word donde se buscará el marcador.
        key: El marcador de posición a buscar (por ejemplo, "<<fig_ejecucion_campania>>").
        lista_figuras: Lista de diccionarios con keys "ruta", "titulo", "tamanio", "bookmark" (opcional).
    
    Returns:
        Lista de nombres de bookmarks creados si se insertaron las imágenes, False si no se encontró el marcador.
        
    Ejemplo de uso:
        lista_figuras = [
            {"ruta": "img1.png", "titulo": "Mapa de ubicación", "tamanio": 6, "bookmark": "_Ref_Mapa1"},
            {"ruta": "img2.png", "titulo": "Temperatura del agua", "tamanio": 5}
        ]
    """
    full_text = "".join(run.text for run in paragraph.runs)
    
    if key not in full_text:
        return False
    
    # Limpiar el párrafo (borrar todos los runs)
    for run in paragraph.runs:
        run.text = ""
    
    # Obtener referencias para inserción
    p_element = paragraph._element
    parent = p_element.getparent()
    indice_base = parent.index(p_element)
    
    # Lista para almacenar los bookmarks creados
    bookmarks_creados = []
    
    # Insertar todas las figuras con sus títulos
    offset = 0
    for idx, item in enumerate(lista_figuras):
        ruta = item.get("ruta", "")
        titulo = item.get("titulo", f"Figura {idx + 1}")
        ancho = item.get("tamanio", 6)
        bookmark = item.get("bookmark", None)  # Bookmark personalizado opcional
        
        # Si es la primera imagen, usar el párrafo actual
        if offset == 0:
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
            if exists(ruta):
                run.add_picture(ruta, width=Inches(ancho))
            offset = 1
        else:
            # Crear nuevo párrafo para imagen
            nuevo_p_img = OxmlElement('w:p')
            parent.insert(indice_base + offset, nuevo_p_img)
            # Convertir a Paragraph para poder agregar imagen
            para_img = Paragraph(nuevo_p_img, paragraph._parent)
            if exists(ruta):
                para_img.add_run().add_picture(ruta, width=Inches(ancho))
            offset += 1
        
        # *** CAMBIO IMPORTANTE: Usar crear_pie_de_figura con bookmark ***
        nuevo_p_caption, bookmark_name = crear_pie_de_figura(
            parent, 
            indice_base + offset, 
            titulo,
            bookmark_name=bookmark
        )
        bookmarks_creados.append(bookmark_name)
        offset += 1
        
        # Salto de línea
        nuevo_p_salto = OxmlElement('w:p')
        parent.insert(indice_base + offset, nuevo_p_salto)
        offset += 1
    
    return bookmarks_creados


def aux_reemplazar_variable_en_parrafo(paragraph, key, value):
    """Reemplaza un marcador de posición en un párrafo de Word PRESERVANDO el formato.
    
    Args:
        paragraph: El párrafo donde buscar el marcador.
        key: El marcador de posición a buscar (por ejemplo, "<<orden_de_servicio>>").
        value: El texto que lo reemplazará (i.e., 100).
    
    Esta función preserva el formato del run donde EMPIEZA el marcador.
    Maneja tanto marcadores dentro de un solo run como divididos entre múltiples runs.
    """
    # Unir todo el texto del párrafo para verificar si este tiene al marcador
    full_text = "".join(run.text for run in paragraph.runs)
    if key not in full_text:
        return paragraph
    
    # Convertir value a string
    new_value = str(value[0]) if isinstance(value, list) else str(value)
    
    # CASO 1: Intentar el caso simple primero (todo en un run)
    for irun, run in enumerate(paragraph.runs):
        if key in run.text:
            run.text = run.text.replace(key, new_value)
        
        elif "<<" in run.text: # Si el marcador está dividido
            variable_word = "".join([paragraph.runs[irun].text, paragraph.runs[irun+1].text, paragraph.runs[irun+2].text])
            if key in variable_word:
                paragraph.runs[irun].text = variable_word.replace(key, new_value)
                paragraph.runs[irun+1].text = ""
                paragraph.runs[irun+2].text = ""
                return paragraph


def insertar_figuras_en_plantilla(doc, diccionario_de_reemplazos):
    """Inserta todas las figuras definidas en el diccionario en la plantilla de Word.
    
    Args:
        doc: Objeto Document de python-docx
        diccionario_de_reemplazos: Diccionario donde las claves que comienzan con "<<fig_" 
                                   contienen listas de figuras a insertar.
    
    Returns:
        dict: Diccionario con los marcadores procesados y sus bookmarks creados.
              Formato: {"<<fig_ejecucion>>": ["_Ref_Fig_Mapa1", "_Ref_Fig_Temp1"], ...}
              Para figuras sin título, el valor es None.
    
    Casos soportados:
        - Caso 1: Figuras SIN título - titulo="" y bookmark=""
                 Se insertan imágenes sin Caption, numeración ni bookmarks
        - Caso 2: Figuras CON título - titulo y bookmark con contenido
                 Se crean pies de figura con estilo Caption, campo SEQ y bookmarks
    
    Estructura esperada del diccionario:
        {
            # Caso 1: Figuras SIN título
            "<<fig_fotos>>": [
                {"ruta": "foto1.png", "titulo": "", "tamanio": 6, "bookmark": ""},
                {"ruta": "foto2.png", "titulo": "", "tamanio": 5, "bookmark": ""}
            ],
            
            # Caso 2: Figuras CON título
            "<<fig_mapas>>": [
                {"ruta": "mapa1.png", "titulo": "Mapa de ubicación", "tamanio": 6, "bookmark": "_Ref_Mapa1"},
                {"ruta": "mapa2.png", "titulo": "Temperatura del agua", "tamanio": 5, "bookmark": "_Ref_Temp"}
            ],
            
            "<<orden_servicio>>": "12345",  # Variables no-figura se ignoran aquí
        }
    
    Ejemplo de uso:
        doc = Document('plantilla.docx')
        diccionario = {
            "<<fig_mapas>>": [
                {"ruta": "mapa1.png", "titulo": "Ubicación sondas", "tamanio": 6, "bookmark": "_Ref_Mapa1"},
                {"ruta": "mapa2.png", "titulo": "Temperatura", "tamanio": 5, "bookmark": "_Ref_Temp"}
            ],
            "<<fig_fotos>>": [
                {"ruta": "foto1.png", "titulo": "", "tamanio": 4, "bookmark": ""}
            ]
        }
        bookmarks_info = insertar_figuras_en_plantilla(doc, diccionario)
        # Retorna: {
        #     "<<fig_mapas>>": ["_Ref_Mapa1", "_Ref_Temp"],
        #     "<<fig_fotos>>": None
        # }
        doc.save('documento_con_figuras.docx')
    """
    bookmarks_info = {}
    
    # Filtrar solo las variables que son figuras (comienzan con "<<fig_")
    variables_figuras = {k: v for k, v in diccionario_de_reemplazos.items() if k.startswith("<<fig_")}
    
    # Procesar cada variable de figura
    for variable, datos_figuras in variables_figuras.items():
        if not isinstance(datos_figuras, list):
            print(f"Advertencia: La variable '{variable}' no contiene una lista. Se omite.")
            continue
        
        if len(datos_figuras) == 0:
            print(f"Advertencia: La variable '{variable}' contiene una lista vacía. Se omite.")
            continue
        
        # Determinar si son figuras CON o SIN título
        # Caso 1: Figuras SIN título - todos los títulos están vacíos
        tiene_titulo = any(item.get("titulo", "") != "" for item in datos_figuras)
        
        # Buscar el marcador en todos los párrafos del documento
        for parrafo in doc.paragraphs:
            if variable in parrafo.text:
                
                if not tiene_titulo:
                    # Caso 1: Figuras SIN título (no Caption, no bookmark)
                    resultado = aux_insertar_figura_sin_titulo(parrafo, variable, datos_figuras)
                    if resultado:
                        bookmarks_info[variable] = None  # Sin bookmarks para figuras sin título
                        break  # Ya se insertó, pasar a la siguiente variable
                else:
                    # Caso 2: Figuras CON título (Caption + SEQ + Bookmarks)
                    bookmarks_creados = aux_insertar_figuras_con_titulo(parrafo, variable, datos_figuras)
                    if bookmarks_creados:
                        bookmarks_info[variable] = bookmarks_creados
                        break  # Ya se insertó, pasar a la siguiente variable
    
    return bookmarks_info


# def reemplazar_en_word(doc, diccionario_de_reemplazos):
#     """Reemplaza los marcadores de posición en un documento de Word utilizando un diccionario de reemplazos.
#     doc es el documento de Word (objeto Document).
#     diccionario_de_reemplazos es un diccionario donde las claves son los marcadores de posición a buscar
#     (por ejemplo, "<<orden_de_servicio>>") y los valores son los textos que los reemplazarán (i.e., 100).
    
#     Para las figuras, el valor debe ser una lista de diccionarios:
#     - Lista con un solo elemento: inserta la figura SIN título
#     - Lista con varios elementos: inserta las figuras CON sus títulos
    
#     Cada diccionario debe tener las keys: "ruta", "titulo", "tamanio", "bookmark" (opcional)
#     """
#     # Para cada párrafo en el documento, reemplaza los marcadores de posición utilizando el diccionario
#     for variable, dato in diccionario_de_reemplazos.items():
#         for parrafo in doc.paragraphs:
#             if variable in parrafo.text:
                
#                 if "fig" not in variable: # Si el marcador no es de figura, reemplazo normal
#                     aux_reemplazar_variable_en_parrafo(parrafo, variable, dato)
                
#                 # if "fig" in variable: # Si el marcador es de figura
#                 #     if isinstance(dato, list):
#                 #         if len(dato) == 1: # Una sola figura SIN título
#                 #             item = dato[0]
#                 #             ruta = item.get("ruta", "")
#                 #             ancho = item.get("tamanio", 6)
#                 #             aux_insertar_figura_sin_titulo(parrafo, variable, ruta, ancho)
#                 #         else: # Varias figuras CON títulos
#                 #             aux_insertar_figuras_con_titulo(parrafo, variable, dato)
#                 # else: # No es un marcador de figura, reemplazo normal
#                 #     aux_reemplazar_en_parrafo(parrafo, variable, dato)
    
#     # Retornar el documento modificado
#     return doc