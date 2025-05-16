import secrets
import random
import string
import hashlib
import requests
import bcrypt

# Funciones auxiliares
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

def cifrar_contrasena(contrasena):
    salt = bcrypt.gensalt()
    hash_cifrado = bcrypt.hashpw(contrasena.encode(), salt)
    return hash_cifrado.decode()

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
                return True, cantidad
        return False, 0
    else:
        return False, 0

def guardar_en_txt(contenido, archivo):
    with open(archivo, "a") as f:
        f.write(contenido + "\n")

def generar_y_guardar_contrasenas():
    cantidad = int(input("¿Cuántas contraseñas deseas generar? "))
    contrasenas_filtradas = 0
    contrasenas_seguras = 0
    paso_progreso = max(1, cantidad // 10)  # Evita división por cero
    
    print(f"\n▶ Iniciando generación de {cantidad} contraseñas...")
    
    for i in range(cantidad):
        nueva_contrasena = generar_contrasena()
        es_filtrada, num_filtraciones = verificar_fuga_contrasena(nueva_contrasena)
        hash_cifrado = cifrar_contrasena(nueva_contrasena)
        
        if es_filtrada:
            guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas_filtradas.txt")
            contrasenas_filtradas += 1
        else:
            guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas_seguras.txt")
            contrasenas_seguras += 1

        guardar_en_txt(f"{nueva_contrasena} | HASH: {hash_cifrado}", "contraseñas.txt")
        
        # Mostrar progreso solo en los porcentajes clave
        if (i + 1) % paso_progreso == 0:
            porcentaje = int((i + 1) / cantidad * 100)
            print(f"Progreso: {porcentaje}% completado")

    # Resumen final fuera del bucle
    print(f"\n🔐 Generación completada:")
    print(f"- Total contraseñas: {cantidad}")
    print(f"- Contraseñas seguras: {contrasenas_seguras}")
    print(f"- Contraseñas filtradas: {contrasenas_filtradas}")
    print(f"Archivos actualizados:")
    print(f"• contraseñas.txt • contraseñas_seguras.txt • contraseñas_filtradas.txt\n")

def verificar_duplicados(archivo="contraseñas.txt"):
    try:
        with open(archivo, "r") as f:
            contraseñas = [line.strip() for line in f]
        
        contraseñas_unicas = set(contraseñas)
        
        if len(contraseñas) == len(contraseñas_unicas):
            print("✅ No hay contraseñas duplicadas en el archivo.")
        else:
            print(f"⚠ Se encontraron {len(contraseñas) - len(contraseñas_unicas)} contraseñas duplicadas.")
    except FileNotFoundError:
        print("El archivo no existe.")

# Menú principal
while True:
    print("\nMENÚ PRINCIPAL")
    print("1. Generar contraseñas")
    print("2. Buscar duplicados")
    print("3. Salir")
    opcion = input("Selecciona una opción: ")
    
    if opcion == "1":
        generar_y_guardar_contrasenas()
    elif opcion == "2":
        verificar_duplicados()
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")