from rdflib import Graph

# Diccionario cuyo:
#   key: URI de los terminos seleccionados
#   value: un 0 (no se modifica)
filtro={}

# Diccionario cuyo:
#   key: URI de los terminos de lov
#   value: Un array de tres posiciones [s, p, o] (que se reinicia cada vez que se carga una nueva ontología).
#     Las posiciones representan:
#       - s indica cuantas veces aparece dicho termino en la ontología como sujeto
#       - p indica cuantas veces aparece dicho termino en la ontología como predicado
#       - o indica cuantas veces aparece dicho termino en la ontología como objeto
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
    filtro[term_uri] = 0
    etiquetas[term_uri] = [0,0,0]
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
    etiquetas[term_uri] = [0,0,0]
    etiqueta[term_uri] = f'{columna[0]}:{columna[1]}'

    # Leer siguiente linea
    linea=datos.readline()

# Cerrar Terms.csv 
datos.close

# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
resultados = open("ParseoFiltradoRDFV2.csv", "w", encoding='utf-8')
resultados_log = open("ParseoFiltradoRDFV2_log.txt", "w", encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
resultados.truncate()
resultados_log.truncate()
# Dar nombre a las columnas (las que aparecen en la siguiente fila y tambien el "prefijo:uri"
# de los terminos seleccionados)
text = "Vocabulario;Tuplas;Etiquetas;Repeticiones;"

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
        # Reiniciar los contadores de apariciones en la ontología
        etiquetas[term_uri][0] = 0
        etiquetas[term_uri][1] = 0
        etiquetas[term_uri][2] = 0

    # Número de apariciones de los términos seleccionados en la ontología
    con = 0
    # Número de términos seleccionados distintos que aparecen en la ontología en posiciones distintas
    # Por ejemplo, si un termino aparece como sujeto, predicado y objeto en triples en ese caso cuenta tres veces.
    # Sin embargo, si un termino aparece 2 veces como sujeto, en ese caso solo cuenta una vez.
    relativo = 0
    
    # Prefijo de la ontología ; numero de tripletas de la ontología
    text = f'{ont_prefix};{len(g)};'

    # Iterar las tripletas de la ontología
    for triple in g:

        # Esta la tripleta entera?
        if len(triple)==3:
            # Dividir la tripleta en sujeto predicado objecto
            subject = str(triple[0])
            predicate = str(triple[1])
            object = str(triple[2])
            
            # Es el sujeto uno de los terminos seleccionados?
            if subject in filtro:
                etiquetas[subject][0] += 1
                con += 1

                # Es la primera vez que se encuentra dicho termino en la ontología como sujeto?
                if etiquetas[subject][0] == 1: 
                    relativo += 1

            # Es el predicado uno de los terminos seleccionados?
            if predicate in filtro:
                etiquetas[predicate][1] += 1
                con += 1

                # Es la primera vez que se encuentra dicho termino en la ontología como predicado?
                if etiquetas[predicate][1] == 1: 
                    relativo += 1

            # Es el objeto uno de los terminos seleccionados?
            if object in filtro:
                etiquetas[object][2] += 1
                con += 1

                # Es la primera vez que se encuentra dicho termino en la ontología como objeto?
                if etiquetas[object][2] == 1:
                    relativo += 1   

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

resultados.close()
resultados_log.close()
print("Resultados guardados en csv")
