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

# Ejecutar la verificación
verificar_duplicados("contraseñas.txt")