from rdflib import Graph

# Diccionario cuyo:
#   key: URI de los terminos seleccionados
#   value: numero que indica cuantas veces aparece dicho termino en todas las ontologías
filtro={}

# Diccionario cuyo:
#   key: URI de los terminos de lov
#   value: numero que indica cuantas veces aparece dicho termino en la ontología
etiquetas={}

# Diccionario cuyo:
#   key: URI de los terminos de lov
#   value: "prefijo:sufijo" de los terminos de lov (no se modifica)
etiqueta={}

# Diccionario cuyo:
#   key: prefijo de las ontologías (tambien es el nombre de los archivos guardados en local)
#   value: un 0 (no se modifica)
vocabularios={}

# Leer excel con la información de las ontologías descargadas
datos = open("VocabulariosV4.csv" , "r", encoding='utf-8')
# Saltar la primera linea (solo contiene el nombre de las columnas)
linea = datos.readline()
# Leer segunda linea (ya contiene datos)
linea = datos.readline()

# Iterar el csv
while(linea):
    # Adquirir el prefijo de la ontología (nombre del archivo que tenemos en local)
    columna = linea.split(";", 1)[0]

    # Crear entrada en el diccionario para dicha ontología
    vocabularios[columna] = 0

    # Leer siguiente linea del excel
    linea = datos.readline()

# Cerrar VocabulariosV4.csv
datos.close()

# Leer excel con la información de los términos de lov que han sido seleccionados
datos = open("Terms_selected.csv" , "r", encoding='utf-8')
# Saltar la primera linea (solo contiene el nombre de las columnas)
linea = datos.readline()
# Leer segunda linea (ya contiene datos)
linea = datos.readline()

# Iterar el csv
while(linea):
    # Dividir la linea en columnas
    columna = linea.split(";")
    # Adquirir la URI del termino
    term_uri = columna[4].replace("\n","")

    # Crear entradas en los diccionarios para dicho término
    filtro[term_uri] = 0
    etiquetas[term_uri] = 0
    etiqueta[term_uri] = f'{columna[0]}:{columna[1]}'

    # Leer siguiente linea
    linea=datos.readline()

# Cerrar Terms_selected.csv 
datos.close

# Leer excel con la información de todos los términos de lov
datos = open("Terms.csv" , "r", encoding='utf-8')
# Saltar la primera linea (solo contiene el nombre de las columnas)
linea=datos.readline()
# Leer segunda linea (ya contiene datos)
linea = datos.readline()

# Iterar el csv
while(linea):
    # Dividir la linea en columnas
    columna = linea.split(";")
    # Adquirir la uri del termino
    term_uri = columna[4].replace("\n","")

    # Crear entradas en los diccionarios para dicho término
    etiquetas[term_uri] = 0
    etiqueta[term_uri] = f'{columna[0]}:{columna[1]}'

    # Leer siguiente linea
    linea=datos.readline()

# Cerrar Terms.csv 
datos.close

# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
resultados = open("ParseoFiltradoRDF.csv", "w", encoding='utf-8')
resultados_log = open("ParseoFiltradoRDF_log.txt", "w", encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
resultados.truncate()
resultados_log.truncate()
# Dar nombre a las columnas (las que aparecen en la siguiente fila y tambien el "prefijo:uri"
# de los terminos seleccionados)
text="Vocabulario;Tuplas;Etiquetas;Repeticiones;"

# Adquirir los "prefijo:uri" de los terminos seleccionados
for term_uri in filtro.keys():
    # Añadir nombre de columna
    text += f'{etiqueta[term_uri]};'

# Escribir nombre de las columnas
text += '\n'
resultados.write(text)

# Iterar los prefijos de las ontologias
for ont_prefix in vocabularios:
    print(f'Cargando {ont_prefix}')

    # Cargar el rdf (cuyo nombre es ont_prefix)
    try:
        name = f'rdf/{ont_prefix}.rdf'
        g = Graph()
        g.parse(name)
    
    except:
        resultados_log.write(f'Error al leer RDF {ont_prefix}.rdf\n')
        print(f'Error al leer RDF {ont_prefix}.rdf')
        continue

    # Iterar la URI de los terminos de lov
    for term_uri in etiquetas.keys():
        # Reiniciar el contador de apariciones en la ontología
        etiquetas[term_uri]=0

    # Número de apariciones de los términos seleccionados en la ontología
    con=0
    # Número de términos seleccionados distintos que aparecen en la ontología
    relativo=0

    # Prefijo de la ontología ; numero de tripletas de la ontología
    text = f'{ont_prefix};{len(g)};'

    # Iterar las tripletas de la ontología
    for triple in g:

        # Esta la tripleta entera?
        if len(triple)==3:
            # Dividir la tripleta en sujeto predicado objecto
            sujeto = str(triple[0])
            predicado = str(triple[1])
            objeto=str(triple[2])

            # Es el sujeto uno de los terminos seleccionados?
            if sujeto in filtro:
                etiquetas[sujeto] += 1
                con += 1
                filtro[sujeto] += 1

                # Es la primera vez que se encuentra dicho termino en la ontología?
                if etiquetas[sujeto] == 1: 
                    relativo += 1

            # Es el predicado uno de los terminos seleccionados?
            if predicado in filtro:
                etiquetas[predicado] += 1
                con += 1
                filtro[predicado] += 1

                # Es la primera vez que se encuentra dicho termino en la ontología?
                if etiquetas[predicado] == 1: 
                    relativo += 1

            # Es el objeto uno de los terminos seleccionados?
            if objeto in filtro:
                etiquetas[objeto] += 1
                con += 1
                filtro[objeto] += 1

                # Es la primera vez que se encuentra dicho termino en la ontología?
                if etiquetas[objeto] == 1: 
                    relativo+=1
            
    text += f'{relativo};{con};'

    # Iterar las colummnas del excel que representan los "prefijo:sufijo" de los términos seleccionados
    for term_uri in filtro.keys():

        if term_uri in etiquetas:
            # Número de apariciones de dicho termino en la ontología 
            text += f'{etiquetas[term_uri]};' 
        
        else:
            # Número de apariciones de dicho termino en la ontología 
            text += '0;'

    text += '\n'
    resultados.write(text)

resultados_log.write("\nTermino = Número de apariciones en todas las ontologías cargadas\n")
for e in filtro.keys():
    resultados_log.write(f"{etiqueta[e]} = {filtro[e]}\n")

resultados.close()
resultados_log.close()
print("Resultados guardados en csv")
