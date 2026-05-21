"""
Word Template Writer Module
===========================

Módulo para manipular plantillas de Word (.docx) con funciones de alto nivel
para insertar figuras, referencias cruzadas, texto, documentos externos y tablas.

API Pública (en español):
    - insertar_figuras_en_plantilla: Inserta imágenes con o sin títulos/captions
    - insertar_referencias_cruzadas_en_plantilla: Crea referencias cruzadas a figuras
    - reemplazar_texto_en_plantilla: Reemplaza variables de texto en la plantilla
    - insertar_documento_externo_en_plantilla: Inserta documentos Word externos
    - rellenar_tablas_en_plantilla: Rellena tablas con datos de DataFrames
    
Utilidades:
    - insert_line_feed: Inserta nuevos párrafos usando XML

Uso típico:
    from word_template_writer import insertar_figuras_en_plantilla, reemplazar_texto_en_plantilla
    from docx import Document
    
    doc = Document('plantilla.docx')
    diccionario = {
        "<<orden_servicio>>": "12345",
        "<<fig_mapas>>": [
            {"ruta": "mapa1.png", "titulo": "Mapa", "tamanio": 6, "bookmark": "_Ref_Mapa1"}
        ]
    }
    
    reemplazar_texto_en_plantilla(doc, diccionario)
    insertar_figuras_en_plantilla(doc, diccionario)
    doc.save('resultado.docx')

Dependencias:
    - python-docx
    - pandas (solo para rellenar_tablas_en_plantilla)
"""

# Funciones principales del orquestador (API pública en español)
from .api import (
    insertar_figuras_en_plantilla,
    insertar_referencias_cruzadas_en_plantilla,
    reemplazar_texto_en_plantilla,
    insertar_documento_externo_en_plantilla,
    rellenar_tablas_en_plantilla,
)

# Utilidades genéricas públicas
from .utils import insert_line_feed

__all__ = [
    # API principal (5 funciones orquestadoras)
    'insertar_figuras_en_plantilla',
    'insertar_referencias_cruzadas_en_plantilla',
    'reemplazar_texto_en_plantilla',
    'insertar_documento_externo_en_plantilla',
    'rellenar_tablas_en_plantilla',
    # Utilidades
    'insert_line_feed',
]

__version__ = '1.0.0'
__author__ = 'Drift Buoys Team'
