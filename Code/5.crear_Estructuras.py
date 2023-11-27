from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, NamespaceManager

# Diccionario cuyo:
#   key: URI de los terminos de lov
#   value: : "prefijo:sufijo" de los terminos seleccionados (no se modifica)
etiqueta={}

# Diccionario cuyo:
#   key: "prefijo:sufijo" de los terminos seleccionados
#   value: : 0 (no se modifica)
uri={}

# Diccionario cuyo:
#   key: prefijo de las ontologías (tambien es el nombre de los archivos guardados en local)
#   value: un 0 (no se modifica)
vocabularios={}

# Las clases anonimas en rdflib aparecen solo como "BNode". Para crear identificadores únicos 
# para clases anónimas utilizamos esta variable
anonimizador=1

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
    # Adquirir el "prefijo:sufijo" del termino
    term_name = f'{columna[0]}:{columna[1]}'

    # Crear entradas en los diccionarios para dicho término
    etiqueta[term_uri] = term_name
    uri[term_name] = 0

    # Leer siguiente linea
    linea=datos.readline()

# Cerrar Terms_selected.csv 
datos.close()

# Leer excel con la información de las ontologías descargadas
datos = open("vocabulariosV4.csv" , "r", encoding='utf-8')
# Saltar la primera linea (solo contiene el nombre de las columnas)
linea = datos.readline()
# Leer segunda linea (ya contiene datos)
linea = datos.readline()

while(linea):
    # Dividir la linea en columnas
    columna = linea.split(";")

    # Crear entradas en los diccionarios para dicho término
    vocabularios[columna[0]] = 0

    # Leer siguiente linea
    linea=datos.readline()

datos.close()

# Esta función te parsea los terminos identificados por rdflib a sus respectivos "prefijo:sufijo".
# term_uri es la uri del termino, i representa si se ha encontrado en un triple como sujeto (1), predicado (2)
# u objeto (3). Tipo es el tipo que utiliza rdflib para representar el tipo de los terminos (clase, clase anonima, etc)
def tag(term_uri, i, tipo, name):
    global anonimizador
    # Esta variable va a almacenar el "prefijo:sufijo" del termino
    tag=""

    # Es un termino seleccionado?
    if term_uri in etiqueta:
        # adquirir el "prefijo:sufijo" del termino
        tag = etiqueta[term_uri]
        if(tag != name):
            prueba.write('Distintos\n')
            prueba.write(f"{tag}\n")
            prueba.write(f"{name}\n")

    else:

        # Es una clase anonima?
        if "BNode" in tipo:

            # Esta clase anonima no ha sido visitada?
            if term_uri not in anonimos:
                # Crear identificado de la clase anonima
                tag = f'Anonimo{anonimizador}'
                # Guardar identificador de la clase anonima
                anonimos[term_uri] = tag
                anonimizador += 1

            else:
                # Adquirir identificador de la clase anonima
                tag = anonimos[term_uri]

        # Es una URI?
        elif "Ref" in tipo:
            tag = name

        # Es un literal?
        elif "Literal" in tipo:
            tag = f"Literal [{term_uri}]"

    # Se ha podido identificar que representa el termino?
    if tag=="":
        # Este caso no deberia pasar
        tag="None"
        prueba.write('None')
        prueba.write(f"{i}-{term_uri}-{tipo}")

    return (tag)

def parsear(ont_prefix):

    try:
        # Cargar el rdf (cuyo nombre es ont_prefix)
        name = f'rdf/{ont_prefix}.rdf'
        g = Graph()
        g.parse(name)
    
    except:
        print(f'Error al cargar la ontología: {ont_prefix}')
        return
    
    # Cargar los import de la ontología en el grafo auxiliar
    for s, p, o in g.triples((None, URIRef('http://www.w3.org/2002/07/owl#imports'), None)):

        try:
            print(o)
            aux_g.parse(o)
        
        except:
            prueba.write(f'Fallo en la ontología {ont_prefix} en el import {o}\n')

    # Iterar los triples de la ontología
    for triple in g:

        # Esta la tripleta entera?
        if len(triple)==3:
            # Adquirir "prefijo:sufijo" del sujeto
            tag1 = tag(str(triple[0]), 1, str(type(triple[0])), triple[0].n3(g.namespace_manager))
            # Adquirir "prefijo:sufijo" del predicado
            tag2 = tag(str(triple[1]), 2, str(type(triple[1])), triple[1].n3(g.namespace_manager))
            # Adquirir "prefijo:sufijo" del objeto
            tag3 = tag(str(triple[2]), 3, str(type(triple[2])), triple[2].n3(g.namespace_manager))

        # Se ha podido identificar correctamente todos los elementos de la tripleta?
        if tag1 != "None" and tag2 != "None" and tag3 != "None":

            if tag1 not in sujetos: 
                sujetos[tag1] = {}

            if tag2 not in sujetos[tag1]: 
                sujetos[tag1][tag2] = []

            if tag3 not in sujetos[tag1][tag2]: 
                sujetos[tag1][tag2].append(tag3)

# term = "prefijo:sufijo" del termino que estamos visitando
def showReal(term, text, c):

    # No hemos visitado este termino con anterioridad?
    if term not in visitado:
        visitado.append(term)

        if c == 0: 
            resultados.write(text+term+"\n")

        # Iterar los predicados en las que el termino sea sujeto (ordenadas alfabeticamente)
        for p in sorted(sujetos[term].keys()):

            # Esto es debido a que si es una clase anonima, rdflib guarda el tipo de la clase anonima
            # (por ejemplo si es una restricción)
            if p!="rdf:type":
                 
                # Iterar los objetos para ese sujeto y predicado (ordenadas alfabeticamente)
                for o in sorted(sujetos[term][p]):

                    resultados.write(text+"  |"+p+"\n")
                    resultados.write(text+"  |  |"+o+"\n")

                    if o in sujetos and o!=term and "Anonimo" in o:
                        showReal(o, text+"  |  |", 1)

# term = "prefijo:sufijo" del termino que estamos visitando
def showTipo(term, text, c):

    # No hemos visitado este termino con anterioridad?
    if term not in visitado:
        visitado.append(term)

        if c == 0:

            try:
                resultad.write(text+sujetos[term]["rdf:type"][0]+"\n")

            except:
                print(sujetos[term])
                
                if "Anonimo" in term: 
                    resultad.write(text+"Anonimo"+"\n")

                elif "#" in term: 
                    resultad.write(text+"#Desconocido"+"\n")

                elif "Literal" in term: 
                    resultad.write(text+"Literal"+"\n")

                else: 
                    resultad.write(text+term+"\n")

        # Iterar los predicados en las que el termino sea sujeto (ordenadas alfabeticamente)
        for p in sorted(sujetos[term].keys()):

            # Esto es debido a que si es una clase anonima, rdflib guarda el tipo de la clase anonima
            # (por ejemplo si es una restricción)
            if p!="rdf:type":

                # Iterar los objetos para ese sujeto y predicado (ordenadas alfabeticamente)
                for o in sorted(sujetos[term][p]):
                    
                    try:

                        resultad.write(text+"  |"+p+"\n")

                        if o in sujetos and 'rdf:type' in sujetos[o]:
                            # Adquirir tipos para ese elemento
                            types = sujetos[o]["rdf:type"]

                            if "#" in types[0]:
                                resultad.write(text+"  |  |#Desconocido\n")

                            elif "Anonimo" in types[0]:
                                resultad.write(text+"  |  |Anonimo\n")

                            else:
                                # Ordenar alfabeticamente los tipos
                                types.sort()
                                resultad.write(text+"  |  |"+', '.join(types)+"\n")

                        else:

                            if "Anonimo" in o: 
                                resultad.write(text+"  |  |"+"Anonimo"+"\n")

                            elif 'xsd' in o:
                                resultad.write(text+"  |  |"+"Datatype"+"\n")

                            elif "Literal" in o: 
                                resultad.write(text+"  |  |"+"Literal"+"\n")

                            else: 
                                #resultad.write(text+"  |  |"+o+"\n")
                                resultad.write(text+"  |  |"+"#Desconocido"+"\n")
                        
                    except:
                        prueba.write(f'Error en {term}\n')

                    if o in sujetos and o!=term and "Anonimo" in o:
                        showTipo(o, text+"  |  |", 1)

# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
result = open("Result.csv", 'w', encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
result.truncate()
# Dar nombre a las columnas
result.write("Vocabulario;Encontrados;\n")

# Crear un nuevo fichero en los que se escriben las estructuras encontradas (sustituyendo el nombre de los
# terminos por su tipo (clase, property, etc.))
resultad = open("Tipos.txt", 'w', encoding='utf-8')
resultad.truncate()

# Crear un nuevo fichero en los que se escriben las estructuras encontradas (con el nombre de los
# terminos)
resultados = open("Original.txt", 'w', encoding='utf-8')
resultad.truncate()

prueba = open('Prueba.txt', 'w',  encoding='utf-8')
prueba.truncate()

visitado=[]

# Este diccionario guarda las tripletas encontradas en una ontología.
# Todos los elementos del diccionario representan un "prefijo:sufijo" .
# En concreto:
#   - key: sujeto de una tripleta (key1)
#   - value: diccionario que representa los "predicate object" con el mismo sujeto (representado por key). En concreto:
#       - key: predicado de la tripleta cuyo sujeto es el key1 del anterior diccionario (key2)
#       - value: un array que representa los "object" con el mismo predicado y sujeto (representado por key2)
sujetos={}

# Diccionario cuyo:
#   - key: uri de la clase anonima
#   - value: identificador creado por este programa para hacer referencia a esa clase anonima
anonimos={}

for ont_prefix in vocabularios:

    print(f'Cargando ontología {ont_prefix}')

    # Grafo auxiliar en el que cargar los import de una ontología
    aux_g = Graph()
    
    try:
        # Vaciar diccionarios
        sujetos.clear()
        anonimos.clear()

        anonimizador=1
        # Cargar ontología
        parsear(ont_prefix)

        if ont_prefix == 'w3c-ssn':
            print(sujetos)

        # Contador que indica el número de tripletas de una ontología que satisface nuestras condiciones
        # para posteriormente detectar patrones
        contador = 0

        # Iterar por oden alfabetico los terminos que se han encontrado como sujeto de una tripleta
        for s in sorted(sujetos.keys()):

            # Hay algun predicado para ese sujeto que sea "rdfs:subClassOf?"
            if "rdfs:subClassOf" in sujetos[s]:

                # Iterar los objetos para ese sujeto y predicado
                for o in sorted(sujetos[s]["rdfs:subClassOf"]):

                    # El objeto representa una clase anonima?
                    if o in sujetos and "Anonimo" in o:
                        contador += 1
                        visitado=[]

                        resultados.write("\n")
                        # Pintar de donde sale esta tripleta
                        resultados.write(f'Ontología: {ont_prefix}\n')
                        resultados.write(f'Estructura: {ont_prefix}-{contador}\n')
                        resultados.write(s+"\n")
                        resultados.write("  |rdfs:subClassOf\n")
                        showReal(o,"  |  |",0)

                        resultad.write("\n")
                        # Pintar de donde sale esta tripleta
                        resultad.write(f'Ontología: {ont_prefix}\n')
                        resultad.write(f'Estructura: {ont_prefix}-{contador}\n')
                        resultad.write("owl:Class\n")
                        resultad.write("  |rdfs:subClassOf\n")
                        visitado=[]
                        showTipo(o,"  |  |",0)

            # Hay algun predicado para ese sujeto que sea "owl:equivalentClass"?
            if "owl:equivalentClass" in sujetos[s]:

                # Iterar los objetos para ese sujeto y predicado
                for o in sorted(sujetos[s]["owl:equivalentClass"]):

                    # El objeto representa una clase anonima?
                    if o in sujetos and "Anonimo" in o:
                        contador += 1
                        visitado=[]
                        resultados.write("\n")
                        # Pintar de donde sale esta tripleta
                        resultados.write(f'Ontología: {ont_prefix}\n')
                        resultados.write(f'Estructura: {ont_prefix}-{contador}\n')
                        resultados.write(s+"\n")
                        resultados.write("  |owl:equivalentClass\n")
                        showReal(o,"  |  |",0)

                        resultad.write("\n")
                        # Pintar de donde sale esta tripleta
                        resultad.write(f'Ontología: {ont_prefix}\n')
                        resultad.write(f'Estructura: {ont_prefix}-{contador}\n')
                        resultad.write("owl:Class\n")
                        resultad.write("  |owl:equivalentClass\n")
                        visitado=[]
                        showTipo(o,"  |  |",0)

        # prefijo de la ontología; numero de tripletas de esa ontología que satisfacen las condiciones
        result.write(f'{ont_prefix};{contador};\n')        
        print(f"{ont_prefix} - {contador}")

    except:
        print('Ha ocurrido un error')


resultados.close()
resultad.close()
result.close()
prueba.close()




















