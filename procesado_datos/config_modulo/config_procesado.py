
config_modulo_procesado = {
    
    # Para cálculos
    "cantidad_de_decimales": 4,  # Cantidad de decimales a los que se redondearán los datos
    "delta_tiempo": "0.5h", # cada cuanto tiempo debe medir y enviar información la sonda. Opciones: "1h", "0.5h"
    
    # Datos de la base de datos de despliegue de sondas
    "ruta_al_excel_de_despliegue_de_sondas": "/Med_2025-2026/General/base_de_datos_planes_de_crucero_y_doris.xlsx", # Ruta al archivo excel con información de las sondas
    "nombre_de_la_hoja_con_informacion_de_sondas": "despliegue_doris",
    
    
    # Ruta a los datos de batimetría del GOM
    "ruta_a_datos_batimetria": "C:\\programacion\\codigos_python\\bases_de_datos\\batimetria_GEBCO_GOM_2023.nc",
     # Ruta a los datos de topografía ETOPO1_Ice_g_gmt4 (se usan para dar los colores de tierra)
    "ruta_a_datos_topografia": "C:\\programacion\\codigos_python\\bases_de_datos\\topografia_ETOPO1_Ice_g_gmt4.nc",
    
    # Figuras
    "formato_de_figuras": "png",  # Opciones: 'png', 'jpg', 'svg', 'pdf'
    "resolucion_de_figuras": 300,  # en dpi
    "origen_de_los_datos": "REALT",  # Opciones: 'REALT', 'MEM'
    "decimales_en_figuras": 2,  # Cantidad de decimales a mostrar en las figuras
    "tipo_de_letra": "Arial",  # Opciones: 'Arial', 'Times New Roman', 'Calibri'
    "tamanio_de_letra": 12,  # Tamaño de letra en las figuras
    "numero_de_bins_histograma": 30,  # Número de bins en los histogramas
    

    "curvas_de_batimetria": [-2000, -1000, -500, -100, -25],  # en metros
}