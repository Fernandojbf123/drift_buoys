"""Script para diagnosticar los estilos disponibles en la plantilla de Word"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from docx import Document
from crear_documentos.configs.manager_doc_config import get_ruta_a_la_plantilla_de_word
from crear_documentos.services.word_template_writer.schemas_helpers import get_estilos_disponibles

# Abrir la plantilla
ruta_plantilla = get_ruta_a_la_plantilla_de_word()
doc = Document(ruta_plantilla)

print("=" * 60)
print("ESTILOS DISPONIBLES EN LA PLANTILLA")
print("=" * 60)

# Usar la función refactorizada para obtener estilos
estilos_disponibles = get_estilos_disponibles(doc)

# Listar todos los estilos de párrafo
print(f"\n--- ESTILOS DE PÁRRAFO (Total: {len(estilos_disponibles)}) ---")
for style_name in estilos_disponibles:
    print(f"  '{style_name}'")

print("\n" + "=" * 60)
print("BUSCANDO ESTILOS ESPECÍFICOS")
print("=" * 60)

# Buscar los estilos que necesitamos
estilos_buscar = ["Car_centrado", "Car_justificado", "Figura", "texto_tablas_centrado", "texto_tablas_justificado"]
for estilo_nombre in estilos_buscar:
    if estilo_nombre in estilos_disponibles:
        print(f"✓ '{estilo_nombre}' - ENCONTRADO")
        # Obtener detalles adicionales del estilo
        try:
            estilo = doc.styles[estilo_nombre]
            if hasattr(estilo, 'style_id'):
                print(f"    style_id: '{estilo.style_id}'")
        except KeyError:
            pass
    else:
        print(f"✗ '{estilo_nombre}' - NO ENCONTRADO")
    print()
