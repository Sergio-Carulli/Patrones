
# Diccionario cuyo:
#   - key : es una estructura detectada en la ontología
#   - value: Es un diccionario en el que se almacenan los siguientes elementos:
#       - valor: Número de veces que se repite dicho patrón en todas las ontologías
#       - est_name: Array con el nombre de las estructuras detectadas
#       - ont_con: Numero de ontologias distintas en las que aparece dicho patron
#       - ont_name: Es un diccionario cuyo:
#           - key: prefijo de la ontología en el que se ha encontrado el patron
#           - value: numero de veces que se ha encontrado el patron en la ontología
patrones = {}

# Contador para crear identificadores unicos para los patrones
contador = 1

# Leer excel con las estructuras generadas
datos = open("Tipos.txt" , "r", encoding='utf-8')
# Saltar la primera linea (es una linea en blanco)
linea = datos.readline()
# Leer segunda linea (ya contiene datos)
linea = datos.readline()

# Variable que guarda la estructura que se esta leyendo
texto = ""

# Variable que indica si se esta leyendo la linea que indica la ontología desde la que se ha
# detectado una estructura
ont_line = True

# Variable que indica si se esta leyendo la linea que indica el nombre de la estructura que se esta leyendo
est_line = True

# Iterar el txt
while(linea):
    
    # Se esta leyendo el prefijo de la ontología?
    if ont_line:
        ont_line = False
        # El prefijo de la ontología se esta leyendo como "Ontología: prefijo\n" 
        # y solo nos interesa el prefijo.
        ont_prefix = linea.split(":",1)[1].strip()

    # Se esta leyendo el nombre de la estructura?
    elif est_line:
        est_line = False
        # El nombre de la estructura se esta leyendo como "Estructura: nombre\n"
        # y solo nos interesa el nombre.
        est_name = linea.split(":",1)[1].strip()

    # Se esta leyendo una linea con texto?
    elif len(linea) > 1: 
        texto += linea

    else:
        # En este caso se esta leyendo una linea en blanco que indica el fin de una estructura.

        # Es la primera vez que se identifica esta estructura?
        if texto not in patrones: 
            # Crear un nuevo patron
            patrones[texto] = {"valor": 0,
                               "est_name": [],
                               "ont_name": {},
                               "ont_con": 0}

        # Indicar que el patron ha sido detectado una vez mas
        patrones[texto]["valor"] += 1

        # Añadir el nombre de la estructura
        patrones[texto]["est_name"].append(est_name)

        # No es la primera vez que se ha detectado dicho patron en la ontología?
        if ont_prefix in patrones[texto]["ont_name"]:
            # Indicar el número de veces que se ha detectado dicho patron en la ontología
            patrones[texto]["ont_name"][ont_prefix] += 1
        
        else:
            # Indicar el número de veces que se ha detectado dicho patron en la ontología
            patrones[texto]["ont_name"][ont_prefix] = 1
            # Indicar el número de ontologías distintas en las que se ha detectado dicho patron
            patrones[texto]["ont_con"] += 1

        # Reiniciar el texto para la siguiente estructura
        texto = ""
        ont_line = True
        est_line = True

    # Leer siguiente linea del excel
    linea = datos.readline()

# Cerrar Tipos.txt
datos.close()

# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
resultados = open("Patrones.txt" , "w", encoding='utf-8')
resultados_csv = open("Patrones.csv" , "w", encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
resultados.truncate()
resultados_csv.truncate()

# Dar nombre a las columnas
resultados_csv.write("Patron;Repeticiones;Aparicion;Estructuras\n")

def contar(ont_name):
    texto = ''

    for ont_prefix, num_apariciones in ont_name.items():
        texto += f'{ont_prefix} ({num_apariciones}); '
    
    return texto

# Iterar los patrones encontrados
for patron in patrones.keys():

    # Una estructura se considera un patron si se repite como mínimo 2 veces
    if patrones[patron]['valor'] > 1:
        # Escribir nombre del patron
        resultados.write(f'Patron {contador}\n')
        # Escribir el número total de veces que se repite
        resultados.write(f"Repeticiones {patrones[patron]['valor']}\n")
        # Escribir el número de ontologias distintas en los que aparece el patron
        resultados.write(f'Ontologias distintas {patrones[patron]["ont_con"]}\n')
        # Escribir cuantas veces aparece el patron en cada ontología
        texto = contar(patrones[patron]['ont_name'])
        resultados.write(f'Ontologías en las que aparece {texto}\n')
        # Escribir patron
        resultados.write(f"{patron}\n")

        # Obtener el nombre de las estructuras en las que se ha detectado el patron
        texto = ';'.join(patrones[patron]["est_name"])
        # Escribir fila en el csv
        resultados_csv.write(f'Patron {contador};{patrones[patron]["valor"]};{patrones[patron]["ont_con"]};{texto}\n')

        contador += 1

resultados.close()
resultados_csv.close()
