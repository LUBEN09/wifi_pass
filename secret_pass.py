import secrets
import random
import string
import json
import csv
import hashlib
import requests
import bcrypt

# Generar una contraseña segura
def generar_contrasena():
    longitud = random.randint(4, 16)

    caracteres = string.ascii_letters + string.digits + string.punctuation
    
    while True:
        contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        if (any(c.islower() for c in contrasena) and
            any(c.isupper() for c in contrasena) and
            any(c.isdigit() for c in contrasena) and
            any(c in string.punctuation for c in contrasena)):
            return contrasena

# Cifrar una contraseña con bcrypt
def cifrar_contrasena(contrasena):
    salt = bcrypt.gensalt()
    hash_cifrado = bcrypt.hashpw(contrasena.encode(), salt)
    return hash_cifrado.decode()

# Verificar si la contraseña ha sido filtrada en Have I Been Pwned
def verificar_fuga_contrasena(contrasena):
    sha1_contrasena = hashlib.sha1(contrasena.encode()).hexdigest().upper()
    prefijo, sufijo = sha1_contrasena[:5], sha1_contrasena[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefijo}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        hashes = respuesta.text.splitlines()
        for hash in hashes:
            hash_sufijo, cantidad = hash.split(":")
            if sufijo == hash_sufijo:
                return True, cantidad  # Se encontró en una filtración
        return False, 0  # No encontrada
    else:
        return False, 0  # En caso de error en la API

# Guardar en archivos específicos
def guardar_en_txt(contenido, archivo):
    with open(archivo, "a") as f:
        f.write(contenido + "\n")

# Generar, cifrar, verificar y guardar contraseñas
def generar_y_guardar_contrasenas(cantidad=100):
    for _ in range(cantidad):
        nueva_contrasena = generar_contrasena()
        es_filtrada, cantidad = verificar_fuga_contrasena(nueva_contrasena)

        hash_cifrado = cifrar_contrasena(nueva_contrasena)

        if es_filtrada:
            print(f"⚠ {nueva_contrasena} ha sido comprometida en {cantidad} filtraciones. Guardando en 'contraseñas_filtradas.txt'")
            guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas_filtradas.txt")
        else:
            print(f"✅ {nueva_contrasena} es segura. Guardando en 'contraseñas_seguras.txt'")
            guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas_seguras.txt")

        # Guardar en archivos generales
        guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas.txt")

# Ejecutar el proceso
generar_y_guardar_contrasenas()
print("🔐 Se generaron, verificaron, cifraron y clasificaron 100 contraseñas únicas.")