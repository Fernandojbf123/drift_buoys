from genericpath import exists

from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

from services.insertar_documentos_externos import insertar_documentos_externos


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
    """Crea un párrafo con pie de figura válido para Word con estilo, campo SEQ y bookmark.
    
    Args:
        parent: El elemento padre XML donde insertar
        indice: Posición donde insertar
        titulo: Texto descriptivo de la figura
        bookmark_name: Nombre del bookmark para referencias cruzadas (opcional, se genera automático si None)
    
    Returns:
        Tupla (elemento XML del párrafo creado, nombre del bookmark)
    
    Estilos aplicados:
        - Si longitud total < 115 caracteres: usa estilo "Car_centrado" (style_id: 'Carcentrado')
        - Si longitud total >= 115 caracteres: usa estilo "Car_justificado" (style_id: 'Carjustificado')
        - Longitud total = "Figura XXX. " + titulo (estimado ~13 + len(titulo))
    
    Bookmark:
        El bookmark se crea alrededor del NÚMERO únicamente, no incluye "Figura" ni el título.
        Estructura: "Figura " [bookmark_start] "8" [bookmark_end] ". Título"
        Esto permite que las referencias cruzadas muestren solo el número.
    """
    cantidad_de_caracteres = 115 # Umbral para decidir entre centrado o justificado (ajustar según necesidades)
    
    # Generar nombre de bookmark si no se proporciona
    if bookmark_name is None:
        # Usar los primeros 30 caracteres del título, reemplazando espacios y caracteres especiales
        bookmark_name = f"_Ref_Fig_{titulo[:30].replace(' ', '_').replace(',', '').replace('.', '')}"
    
    # Generar ID único para el bookmark basado en el hash del nombre
    bookmark_id = str(abs(hash(bookmark_name)) % 1000000)
    
    # Crear párrafo con estilo
    nuevo_p = OxmlElement('w:p')
    
    # Determinar qué estilo usar según la longitud del título
    # Estimamos "Figura XXX. " = ~13 caracteres + titulo
    longitud_estimada = 13 + len(titulo)
    # IMPORTANTE: Usar style_id de la plantilla, no el nombre visible
    estilo_titulo = 'Carcentrado' if longitud_estimada < cantidad_de_caracteres else 'Carjustificado'
    
    # Propiedades del párrafo
    pPr = OxmlElement('w:pPr')
    
    # Aplicar estilo según longitud
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), estilo_titulo)
    pPr.append(pStyle)
    
    nuevo_p.append(pPr)
    
    # Run para "Figura " (fuera del bookmark)
    run1 = OxmlElement('w:r')
    text1 = OxmlElement('w:t')
    text1.set(qn('xml:space'), 'preserve')  # Preservar el espacio al final
    text1.text = 'Figura '
    run1.append(text1)
    nuevo_p.append(run1)
    
    # IMPORTANTE: Agregar bookmark start AQUÍ (antes del número, después de "Figura ")
    # Esto hace que el bookmark solo incluya el número "X" y no "Figura X"
    bookmark_start = OxmlElement('w:bookmarkStart')
    bookmark_start.set(qn('w:id'), bookmark_id)
    bookmark_start.set(qn('w:name'), bookmark_name)
    nuevo_p.append(bookmark_start)
    
    # Campo SEQ para numeración automática
    # Nota: Los campos complejos en Word requieren la siguiente estructura:
    # 1. fldChar begin (en su propio run)
    # 2. instrText (en su propio run)
    # 3. fldChar separate (en su propio run)
    # 4. texto del resultado (en su propio run)
    # 5. fldChar end (en su propio run)
    
    # Run para inicio del campo
    run_begin = OxmlElement('w:r')
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    run_begin.append(fldChar_begin)
    nuevo_p.append(run_begin)
    
    # Run para la instrucción SEQ
    run_instr = OxmlElement('w:r')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' SEQ Figura \\* ARABIC '
    run_instr.append(instrText)
    nuevo_p.append(run_instr)
    
    # Run para el separador
    run_separate = OxmlElement('w:r')
    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    run_separate.append(fldChar_separate)
    nuevo_p.append(run_separate)
    
    # Run para el texto del resultado (placeholder que Word actualizará)
    run_result = OxmlElement('w:r')
    text_result = OxmlElement('w:t')
    text_result.text = '1'  # Placeholder que Word actualizará
    run_result.append(text_result)
    nuevo_p.append(run_result)
    
    # Run para fin del campo
    run_end = OxmlElement('w:r')
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    run_end.append(fldChar_end)
    nuevo_p.append(run_end)
    
    # IMPORTANTE: Agregar bookmark end AQUÍ (después del número, antes del título)
    # Esto hace que el bookmark solo incluya "Figura X" y no el título completo
    bookmark_end = OxmlElement('w:bookmarkEnd')
    bookmark_end.set(qn('w:id'), bookmark_id)
    nuevo_p.append(bookmark_end)
    
    # Run para el texto descriptivo (fuera del bookmark)
    run2 = OxmlElement('w:r')
    text2 = OxmlElement('w:t')
    text2.set(qn('xml:space'), 'preserve')
    text2.text = f'. {titulo}'
    run2.append(text2)
    nuevo_p.append(run2)
    
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
            # Aplicar estilo "Figura" al párrafo actual
            p_element = paragraph._element
            pPr = p_element.find(qn('w:pPr'))
            if pPr is None:
                pPr = OxmlElement('w:pPr')
                p_element.insert(0, pPr)
            # Aplicar estilo Figura
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is None:
                pStyle = OxmlElement('w:pStyle')
                pPr.insert(0, pStyle)
            pStyle.set(qn('w:val'), 'Figura')
            
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
            if exists(ruta):
                run.add_picture(ruta, width=Inches(ancho))
            offset = 1
        else:
            # Crear nuevo párrafo para imagen con estilo "Figura"
            nuevo_p_img = OxmlElement('w:p')
            # Propiedades del párrafo
            pPr_img = OxmlElement('w:pPr')
            pStyle_img = OxmlElement('w:pStyle')
            pStyle_img.set(qn('w:val'), 'Figura')
            pPr_img.append(pStyle_img)
            nuevo_p_img.append(pPr_img)
            
            parent.insert(indice_base + offset, nuevo_p_img)
            # Convertir a Paragraph para poder agregar imagen
            para_img = Paragraph(nuevo_p_img, paragraph._parent)
            if exists(ruta):
                para_img.add_run().add_picture(ruta, width=Inches(ancho))
            offset += 1
        
        # Salto de línea después de cada imagen
        # nuevo_p_salto = OxmlElement('w:p')
        # parent.insert(indice_base + offset, nuevo_p_salto)
        # offset += 1
    
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
            # Aplicar estilo "Figura" al párrafo actual
            p_element = paragraph._element
            pPr = p_element.find(qn('w:pPr'))
            if pPr is None:
                pPr = OxmlElement('w:pPr')
                p_element.insert(0, pPr)
            # Aplicar estilo Figura
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is None:
                pStyle = OxmlElement('w:pStyle')
                pPr.insert(0, pStyle)
            pStyle.set(qn('w:val'), 'Figura')
            
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
            if exists(ruta):
                run.add_picture(ruta, width=Inches(ancho))
            offset = 1
        else:
            # Crear nuevo párrafo para imagen con estilo "Figura"
            nuevo_p_img = OxmlElement('w:p')
            # Propiedades del párrafo
            pPr_img = OxmlElement('w:pPr')
            pStyle_img = OxmlElement('w:pStyle')
            pStyle_img.set(qn('w:val'), 'Figura')
            pPr_img.append(pStyle_img)
            nuevo_p_img.append(pPr_img)
            
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


def aux_reemplazar_multiples_variables_en_parrafo(paragraph, lista_variables):
    """Reemplaza múltiples marcadores de posición en un párrafo de Word de una sola vez.
    
    Args:
        paragraph: El párrafo donde buscar los marcadores.
        lista_variables: Lista de tuplas (key, value) con los marcadores y sus valores.
                        Ejemplo: [("<<orden_de_servicio>>", "202"), ("<<numero_de_sondas>>", 5)]
    
    Esta función reemplaza todas las variables en un solo paso, evitando problemas
    de estado cuando hay múltiples variables en el mismo párrafo.
    """
    # Obtener el texto completo del párrafo
    full_text = "".join(run.text for run in paragraph.runs)
    
    # Reemplazar todas las variables en el texto completo
    texto_reemplazado = full_text
    for key, value in lista_variables:
        if key in texto_reemplazado:
            # Convertir value a string
            new_value = str(value[0]) if isinstance(value, list) else str(value)
            # Reemplazar todas las ocurrencias de esta variable
            texto_reemplazado = texto_reemplazado.replace(key, new_value)
    
    # Si no hubo cambios, retornar
    if texto_reemplazado == full_text:
        return paragraph
    
    # Limpiar todos los runs excepto el primero
    primer_run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    primer_run.text = texto_reemplazado
    
    # Limpiar el resto de runs
    for i in range(1, len(paragraph.runs)):
        paragraph.runs[i].text = ""
    
    return paragraph


def aux_reemplazar_texto_en_parrafo(paragraph, key, value):
    """Reemplaza un marcador de posición en un párrafo de Word PRESERVANDO el formato.
    
    Args:
        paragraph: El párrafo donde buscar el marcador.
        key: El marcador de posición a buscar (por ejemplo, "<<orden_de_servicio>>").
        value: El texto que lo reemplazará (i.e., 100).
    
    NOTA: Esta función es mantenida por compatibilidad, pero se recomienda usar
    aux_reemplazar_multiples_variables_en_parrafo para mejor manejo de múltiples variables.
    """
    # Usar la nueva función con una sola variable
    aux_reemplazar_multiples_variables_en_parrafo(paragraph, [(key, value)])
    return paragraph


############### SOLO INSERTAR REFERENCIAS CRUZADAS A FIGURAS ANTES SE DEBIÓ EJECUTAR LA INSERSIÓN DE FIGURAS ########################
def insertar_referencias_cruzadas_en_plantilla(doc, diccionario_de_reemplazos: dict):
    """Reemplaza marcadores <<ref_*>> con referencias cruzadas a figuras.
    
    Args:
        doc: Objeto Document de python-docx
        diccionario_de_reemplazos: Diccionario retornado por insertar_figuras_en_plantilla
                                  Formato: {"<<ref_demo>>": ["_Ref_Fig_Mapa1", "_Ref_Fig_Temp"], ...}
    
    Comportamiento:
        - Busca variables que empiecen con "<<ref_" en los párrafos
        - Si la lista tiene 1 bookmark: inserta "Figura X"
        - Si la lista tiene 2+ bookmarks: inserta "Figura X a la Y"
        - X e Y son referencias cruzadas reales (campos REF) que muestran solo el número
        - Procesa TODOS los marcadores de un párrafo en una sola pasada
    
    Nota importante:
        Los bookmarks creados por crear_pie_de_figura solo incluyen el número de la figura,
        no el texto "Figura" ni el título. Por eso las referencias muestran solo el número.
    
    Ejemplo:
        Entrada en plantilla: "De la <<ref_demo_con_titulo>> se muestra el poder."
        Salida: "De la Figura 8 a la 10 se muestra el poder."
                (donde "8" y "10" son campos REF clickeables que muestran solo el número)
    """
    # Filtrar solo variables con bookmarks válidos
    variables_validas = {k: v for k, v in diccionario_de_reemplazos.items() 
                        if v is not None and len(v) > 0 and k.startswith("<<ref_")}
    
    # Para cada párrafo
    for parrafo in doc.paragraphs:
        full_text = "".join(run.text for run in parrafo.runs)
        
        # Encontrar TODOS los marcadores <<ref_*>> en este párrafo
        marcadores_en_parrafo = []
        for variable_ref, lista_bookmarks in variables_validas.items():
            if variable_ref in full_text:
                # Encontrar todas las ocurrencias del marcador en el párrafo
                pos = full_text.find(variable_ref)
                if pos != -1:
                    marcadores_en_parrafo.append((pos, variable_ref, lista_bookmarks))
        
        # Si no hay marcadores en este párrafo, continuar al siguiente
        if not marcadores_en_parrafo:
            continue
        
        # Ordenar marcadores por posición (de izquierda a derecha)
        marcadores_en_parrafo.sort(key=lambda x: x[0])
        
        # print(f"Párrafo con {len(marcadores_en_parrafo)} marcadores: {[m[1] for m in marcadores_en_parrafo]}")
        
        # Limpiar todos los runs del párrafo
        for run in parrafo.runs:
            run.text = ""
        
        # Reconstruir el párrafo procesando todos los marcadores
        pos_actual = 0
        
        for pos_marcador, variable_ref, lista_bookmarks in marcadores_en_parrafo:
            # Agregar texto antes del marcador
            if pos_marcador > pos_actual:
                texto_antes = full_text[pos_actual:pos_marcador]
                parrafo.add_run(texto_antes)
            
            # Insertar la referencia cruzada
            primer_bookmark = lista_bookmarks[0]
            ultimo_bookmark = lista_bookmarks[-1]
            
            # print(f"  Procesando: {variable_ref} con bookmarks: {lista_bookmarks}")
            
            if len(lista_bookmarks) == 1:
                # Caso: Solo una figura - "Figura X"
                insertar_referencia_cruzada(parrafo, primer_bookmark, texto_antes="Figura", mostrar_numero=True)
            else:
                # Caso: Múltiples figuras - "Figura X a la Y"
                insertar_referencia_cruzada(parrafo, primer_bookmark, texto_antes="Figura", mostrar_numero=True)
                parrafo.add_run(" a la ")
                insertar_referencia_cruzada(parrafo, ultimo_bookmark, texto_antes="", mostrar_numero=True)
            
            # Avanzar posición actual
            pos_actual = pos_marcador + len(variable_ref)
        
        # Agregar texto después del último marcador
        if pos_actual < len(full_text):
            texto_despues = full_text[pos_actual:]
            parrafo.add_run(texto_despues)

    msg = "Referencias cruzadas insertadas."
    print(msg)



############## SOLO INSERTAR FIGURAS ########################
def insertar_figuras_en_plantilla(doc, diccionario_de_reemplazos: dict):
    """Inserta todas las figuras definidas en el diccionario en la plantilla de Word.
        y muta el diccionario de entrada al unirlo con la información de los bookmarks 
        creados para referencias cruzadas.
        
    Args:
        doc: Objeto Document de python-docx
        diccionario_de_reemplazos: Diccionario donde las claves que comienzan con "<<fig_" 
                                   contienen listas de figuras a insertar.
    
    Returns:
        dict: Diccionario con los marcadores procesados y sus bookmarks creados.
              Formato: {"<<ref_ejecucion>>": ["_Ref_Fig_Mapa1", "_Ref_Fig_Temp1"], ...}
              Nota: Las keys cambian de "<<fig_*>>" a "<<ref_*>>" automáticamente.
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
        
        # Paso 1: Insertar las figuras
        bookmarks_info = insertar_figuras_en_plantilla(doc, diccionario)
        # Retorna: {
        #     "<<ref_mapas>>": ["_Ref_Mapa1", "_Ref_Temp"],
        #     "<<ref_fotos>>": None
        # }
        
        # Paso 2: Insertar referencias cruzadas (si hay marcadores <<ref_*>> en la plantilla)
        # Ejemplo: "De la <<ref_mapas>> se observa..." → "De la Figura 1 a la 2 se observa..."
        insertar_referencias_cruzadas_en_plantilla(doc, bookmarks_info)
        
        doc.save('documento_con_figuras.docx')
    """
    bookmarks_info = {}
    
    if diccionario_de_reemplazos is None:
        raise ValueError("El diccionario de reemplazos no puede ser None.")
    
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
                
                variable_ref_key = variable.replace("fig","ref") # Sirve para crear un key asociado al nombre de la variable para usar la referencia en el word y poder hacer párrafos del tipo "de la Figura X a la Figura Y"
                
                if not tiene_titulo:
                    # Caso 1: Figuras SIN título (no Caption, no bookmark)
                    resultado = aux_insertar_figura_sin_titulo(parrafo, variable, datos_figuras)
                    if resultado:
                        bookmarks_info[variable_ref_key] = None  # Sin bookmarks para figuras sin título
                        break  # Ya se insertó, pasar a la siguiente variable
                else:
                    # Caso 2: Figuras CON título (Caption + SEQ + Bookmarks)
                    bookmarks_creados = aux_insertar_figuras_con_titulo(parrafo, variable, datos_figuras)
                    if bookmarks_creados:
                        bookmarks_info[variable_ref_key] = bookmarks_creados
                        break  # Ya se insertó, pasar a la siguiente variable
    
    diccionario_de_reemplazos.update(bookmarks_info)
    msg = f"Figuras insertadas y bookmarks creados para referencias cruzadas"
    print(msg)



################ SOLO REEMPLAZAR TEXTOS #########################
def reemplazar_texto_en_word(doc, diccionario_de_reemplazos):
    """Reemplaza los marcadores de posición en un documento de Word utilizando un diccionario de reemplazos.
    doc es el documento de Word (objeto Document).
    diccionario_de_reemplazos es un diccionario donde las claves son los marcadores de posición a buscar
    (por ejemplo, "<<orden_de_servicio>>") y los valores son los textos que los reemplazarán (i.e., 100).
    
    Para las figuras, el valor debe ser una lista de diccionarios:
    - Lista con un solo elemento: inserta la figura SIN título
    - Lista con varios elementos: inserta las figuras CON sus títulos
    
    Cada diccionario debe tener las keys: "ruta", "titulo", "tamanio", "bookmark" (opcional)
    """
    # Filtrar solo variables que NO son figuras
    variables_texto = {k: v for k, v in diccionario_de_reemplazos.items() 
                      if "fig" not in k and "ref" not in k and "ruta_plan_de_crucero" not in k}
    
    # Para cada párrafo, procesar TODAS las variables de texto de una sola vez
    for parrafo in doc.paragraphs:
        # Encontrar todas las variables que están en este párrafo
        variables_en_parrafo = []
        for variable, dato in variables_texto.items():
            if variable in parrafo.text:
                variables_en_parrafo.append((variable, dato))
        
        # Si hay variables en este párrafo, reemplazarlas todas de una vez
        if variables_en_parrafo:
            aux_reemplazar_multiples_variables_en_parrafo(parrafo, variables_en_parrafo)
    
    msg = f"Se agregaron los textos al documento."
    print(msg)



################## INSERTA EL(LOS) PLAN(ES) DE CRUCERO(S) #########################
def insertar_plan_de_crucero_en_word(doc, diccionario_de_reemplazos):
    """Reemplaza los marcadores de posición en un documento de Word utilizando un diccionario de reemplazos.
    doc es el documento de Word (objeto Document).
    diccionario_de_reemplazos es un diccionario donde las claves son los marcadores de posición a buscar
    (por ejemplo, "<<orden_de_servicio>>") y los valores son los textos que los reemplazarán (i.e., 100).
    
    Para las figuras, el valor debe ser una lista de diccionarios:
    - Lista con un solo elemento: inserta la figura SIN título
    - Lista con varios elementos: inserta las figuras CON sus títulos
    
    Cada diccionario debe tener las keys: "ruta", "titulo", "tamanio", "bookmark" (opcional)
    """
    # Para cada párrafo en el documento, reemplaza los marcadores de posición utilizando el diccionario
    dato = diccionario_de_reemplazos["<<ruta_plan_de_crucero>>"]
    for parrafo in doc.paragraphs:
        if "<<ruta_plan_de_crucero>>" in parrafo.text:
            insertar_documentos_externos(parrafo, "<<ruta_plan_de_crucero>>", dato, doc)
            msg = f"Plan de crucero insertado"
            if len(dato) > 1:
                msg = f"Planes de crucero insertados"
                print(msg)
                break
            # return doc