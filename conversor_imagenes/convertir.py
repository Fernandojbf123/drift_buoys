import os
from PIL import Image
from pillow_heif import register_heif_opener

# Habilitar lectura de archivos HEIC
register_heif_opener()

def convertir(directorio_raiz):

    for ruta_actual, _, archivos in os.walk(directorio_raiz):
        print(f"Explorando: {ruta_actual}")
        for archivo in archivos:

            if archivo.lower().endswith(".heic"):
                print(f"Encontrado: {archivo}")
                ruta_heic = os.path.join(ruta_actual, archivo)

                nombre_base = os.path.splitext(archivo)[0]
                ruta_png = os.path.join(ruta_actual, f"{nombre_base}.png")

                try:
                    imagen = Image.open(ruta_heic)

                    # Convertir a RGB por compatibilidad
                    if imagen.mode != "RGB":
                        imagen = imagen.convert("RGB")

                    imagen.save(ruta_png, "PNG")

                    print(f"Convertido: {ruta_heic}")
                    print(f"Guardado:   {ruta_png}")

                except Exception as e:
                    print(f"Error en {ruta_heic}: {e}")
                    
import os
ruta = r"\\Mediciones_2025\DORIS_BOYAS_DERIVA\2026\Doris_Isla_Aguada_26mayo2026"
print("Existe:", os.path.exists(ruta))
contador = 0
for carpeta, _, archivos in os.walk(ruta):
    print("Carpeta:", carpeta)

    for archivo in archivos:
        if archivo.lower().endswith((".heic", ".heif")):
            contador += 1
            print("HEIC:", os.path.join(carpeta, archivo))

print("Total HEIC encontrados:", contador)