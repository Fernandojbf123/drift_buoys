# ¿Qué son los pipelines?
Son secuencias de llamada a los módulos y/o submódulos. Los pipelines inyectan una configuración que sobreescribe la configuración individual de cada módulo sin alterar el funcionamiento de estos (Principio de sustitución de Liskov - SOLID)

# Pipiles para DORIS
1. despliegue.py -> se encarga de ejecutar la descarga, el procesado de despliegue y generar el reporte.
Previo a correr este pipeline, tienes que tener actualizado:
- base_de_datos_planes_de_crucero_y_doris.xlsx -> tablas: campanias y despliegue_doris
- 2026_info_documentos_101.xlsx -> y tener las fotos disponibles en la carpeta
- pruebas_sat (hay que agregar ese código acá)
- esquemas de DORIS (hay que agregar ese código acá)
- 