"""Script para diagnosticar los estilos disponibles en la plantilla de Word"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from docx import Document
from crear_documentos.configs.manager_doc_config import get_ruta_a_la_plantilla_de_word

# Abrir la plantilla
ruta_plantilla = get_ruta_a_la_plantilla_de_word()
doc = Document(ruta_plantilla)

print("=" * 60)
print("ESTILOS DISPONIBLES EN LA PLANTILLA")
print("=" * 60)

# Listar todos los estilos de párrafo
print("\n--- ESTILOS DE PÁRRAFO ---")
for style in doc.styles:
    if style.type == 1:  # 1 = PARAGRAPH
        print(f"  Nombre interno: '{style.name}'")
        # Verificar si tiene style_id diferente
        if hasattr(style, 'style_id'):
            print(f"    style_id: '{style.style_id}'")
        print()

print("\n" + "=" * 60)
print("BUSCANDO ESTILOS ESPECÍFICOS")
print("=" * 60)

# Buscar los estilos que necesitamos
estilos_buscar = ["Car_centrado", "Car_justificado", "Figura"]
for estilo_nombre in estilos_buscar:
    try:
        estilo = doc.styles[estilo_nombre]
        print(f"✓ '{estilo_nombre}' - ENCONTRADO")
        if hasattr(estilo, 'style_id'):
            print(f"  style_id: '{estilo.style_id}'")
    except KeyError:
        print(f"✗ '{estilo_nombre}' - NO ENCONTRADO")
    print()
