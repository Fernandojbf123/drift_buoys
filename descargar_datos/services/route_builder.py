
import os
import dotenv
import configs.hashes as hashes

dotenv.load_dotenv()

def get_user():
    user = os.getenv("USER", None)
    if user is None:
        raise ValueError("No se encontró la variable de entorno USER. Asegúrate de que esté definida en el archivo .env.")
    return user

def get_password():
    password = os.getenv("PASSWORD", None)
    if password is None:
        raise ValueError("No se encontró la variable de entorno PASSWORD. Asegúrate de que esté definida en el archivo .env.")
    return password

def get_web():
    web = os.getenv("WEB", None)
    if web is None:
        raise ValueError("No se encontró la variable de entorno WEB. Asegúrate de que esté definida en el archivo .env.")
    return web


def get_hash(doris_serial_number):
    hash = hashes.doris_hashes.get(doris_serial_number, None)
    if hash is None:
        print(f"No se encontró un hash para el número de serie {doris_serial_number}.")
        print("Asegúrate de que el número de serie esté en el archivo descargar_datos/configs/hashes.py.")
        print("Si no está, agrega el hash correspondiente al número de serie en ese archivo.")
        raise ValueError(f"No se encontró un hash para el número de serie {doris_serial_number}.")
    
    return hash

def build_download_url(doris_serial_number):
    user = get_user()
    password = get_password()
    web = get_web()
    hash = get_hash(doris_serial_number)
    url = f"{web}&user={user}&psw={password}&hash={hash}"
    return url