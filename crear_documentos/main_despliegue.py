######################################### NO TOCAR ##########################################
import os
import sys

# Agrega la ruta raíz del proyecto si no está
# Usa __file__ para calcular la ruta desde la ubicación del script
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.orquestador import *
    
##############################################################################################

def main():
    crear_documento_de_despliegue()
        
if __name__ == "__main__":
    main()