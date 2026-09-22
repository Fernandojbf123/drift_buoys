import os
import dotenv
from src.leer_excel import leer_excel

def revisor_de_doris_duplicadas(config):
    # Cargar variables de entorno
    dotenv.load_dotenv()
    
    # leer el archivo excel con la información de las sondas
    nas = ""
    ruta_al_excel_de_despliegue = config.ruta_al_excel_de_despliegue_de_sondas
    if config.usar_NAS:
        nas = os.getenv("ruta_al_NAS")
        
    ruta_al_excel_de_despliegue = os.path.join(nas, ruta_al_excel_de_despliegue)

    hoja = config.nombre_de_la_hoja_con_informacion_de_sondas
    df = leer_excel(ruta_al_archivo = ruta_al_excel_de_despliegue, nombre_de_hoja=hoja, header=0)
    if df.empty:
        raise ValueError("Ocurrió un problema al cargar la base de datos de DORIS")
        
     
    # obtener seriales que se desean verificar
    seriales = config.seriales_de_sondas
    # crear el array con los nuevos nombres de seriales (inicialmente vacio)
    nuevos_seriales = []
        
    # obtener la lista de seriales ya registrados en la base de datos
    seriales_originales = list(df["serial_original"])
    seriales_en_la_web = list(df["serial_de_sonda"])
        
    
    print("****** LISTADO DE SERIALES A VERIFICAR *******")    
    seriales_dict = verificar_seriales_nuevos_vs_registrados(seriales, seriales_originales)
    notificador(seriales_dict, columna="serial_original")
    
    # Si un serial es nuevo se agrega; si el serial existe (es usado), se debe cambiar y se debe verificar que ese cambio sea único en la columna de serial_de_sonda
    for serial, existe in seriales_dict.items():
        if not existe:
            nuevos_seriales.append(serial)
        else:
            nuevo_serial = cambia_el_serial(serial)
            while nuevo_serial in seriales_en_la_web:
                nuevo_serial = cambia_el_serial(nuevo_serial)
            nuevos_seriales.append(nuevo_serial)


    print("****** LISTADO DE NOMBRES SUGERIDOS *******")   
    seriales_dict_web = verificar_seriales_nuevos_vs_registrados(nuevos_seriales, seriales_en_la_web)
    notificador(seriales_dict_web, columna="serial_de_sonda")
    
    print("****** COMPARATIVA DE SERIALES *******")   
    print(f"Seriales originales {seriales}")
    print(f"Nuevos seriales     {nuevos_seriales}")


def verificar_seriales_nuevos_vs_registrados(seriales_a_verificar: list, seriales_registrados: list):
    """
    seriales_a_verificar = lista de seriales de configuracion
    seriales_registrados = lista de seriales que ya están registrados en la base de datos
    
    devuelve un diccionario cuyo key es el serial_original y el value es True si es un serial ya registrado, False si es nuevo.
    
    """
    seriales_dict = {}
    
    for serial in seriales_a_verificar:
        existe = False
        for serial_registrado in seriales_registrados:
            # Asegurar que serial_registrado sea de tipo str
            serial_registrado = str(serial_registrado)
            if serial == serial_registrado.split("-")[-1]:
                existe = True
                break
        
        if existe:
            seriales_dict[serial] = True
        else:
            seriales_dict[serial] = False

    return seriales_dict


def notificador(seriales_dict: dict, columna: str):
    """
    Notifica cuáles seriales son nuevos y cuáles ya están registrados en la columna especificada.
    
    seriales_dict = diccionario cuyo key es el serial_original y el value es True si es un serial ya registrado, False si es nuevo.
    """
    for serial, existe in seriales_dict.items():
        if existe:
            print(f"El serial {serial} ya está registrado en la columna {columna}.")
        else:
            print(f"El serial {serial} es nuevo en la columna {columna}.")
            
            
def cambia_el_serial(serial: str):
    serial = str(serial)
    serial = serial.split("-")[-1]
    numeros = list(serial)
    primer_numero = numeros[0]
    if primer_numero == "4":
        numeros[0] = numeros[0].replace("4","9")
    elif primer_numero == "9":
        numeros[0] = numeros[0].replace("9","10")
    elif primer_numero == "1":
        segundo_numero = int(numeros[1])
        if segundo_numero == 9:
            numeros[0] = numeros[0].replace("1","2")
            numeros[1] = numeros[1].replace("9", "0")
        else:
            numeros[1] = numeros[1].replace(str(segundo_numero), str(int(segundo_numero)+1))
        
    return "".join(numeros)
    
    