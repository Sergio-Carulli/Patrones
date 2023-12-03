import os.path
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

# Dictionary to store the ontology triples whose:
#   - key: subject of a triple
#   - value: dictionary to store the "predicate" and "object" of triples with the same "subject" whose:
#       - key: triple predicate whose subject is the key of the above dictionary
#       - value: an array which represents the "object" of triples with the same "subject" and "predicate"
subjects = {}

# Dictionary to store the rdflib URIs to identify anonymous classes whose:
#   - key: rdflib URI of the anonymous class
#   - value: identifier made by this program in order to reference the anonymous class
anonymous = {}

# Dictionary to store the namespaces declared in an ontology whose:
#   - key: namespace
#   - value: the URI associated to the namespace
namespaces = {}

# Dictionary to store the ontologies which have been imported whose:
#   - key: URI of the ontology
#   - value: 0 (unchanged)
ont_import = {}

# Variable to store the prefix of the ontology
ont_prefix = ''

# Variable used to create unique identifier for the anonymous classes
anonimizador = 1

# Auxiliary graph in which the owl:imports are going to be parsed
aux_g = Graph()

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

def create_structure(ontology_path, app_directory, error_log):
    #terms_selected_directory = os.path.join(app_directory, 'Code', 'Terms_selected.csv')

    # Obtain the name of the downloaded ontologies
    ontologies = os.listdir(ontology_path)
    # Declare global variables
    global ont_prefix, subjects, anonymous, namespaces, ont_import, aux_g, anonimizador

    # Iterate the name of the downloaded ontologies
    for ont_name in ontologies:
        # Get the path to the downloaded ontology
        ont_path = os.path.join(ontology_path, ont_name)
        # Write the global variable
        ont_prefix = ont_name

        # Is there an error in the ontology file?
        if ontology_path_error(ont_path, error_log):
            print(f'Loading ontology {ont_name}')

            try:
                # Emptying dictionaries
                subjects = {}
                anonymous = {}
                namespaces = {}
                ont_import = {}
                aux_g = Graph()
                anonimizador = 1

                # Parse ontology
                parse_ontology(ont_path, error_log)

                # Contador que indica el número de tripletas de una ontología que satisface nuestras condiciones
                # para posteriormente detectar patrones
                contador = 0

                # Iterar por oden alfabetico los terminos que se han encontrado como sujeto de una tripleta
                for s in sorted(subjects.keys()):

                    # Hay algun predicado para ese sujeto que sea "rdfs:subClassOf?"
                    if "rdfs:subClassOf" in subjects[s]:

                        # Iterar los objetos para ese sujeto y predicado
                        for o in sorted(subjects[s]["rdfs:subClassOf"]):

                            # El objeto representa una clase anonima?
                            if o in subjects and "Anonimo" in o:
                                contador += 1

                                resultados.write("\n")
                                # Pintar de donde sale esta tripleta
                                resultados.write(f'Ontología: {ont_name}\n')
                                resultados.write(f'Estructura: {ont_name}-{contador}\n')
                                resultados.write(s+"\n")
                                resultados.write("  |rdfs:subClassOf\n")
                                resultados.write(f'  |  |{o}\n')
                                show_term(o,"  |  |", [])

                                visitado=[]
                                resultad.write("\n")
                                # Pintar de donde sale esta tripleta
                                resultad.write(f'Ontología: {ont_name}\n')
                                resultad.write(f'Estructura: {ont_name}-{contador}\n')
                                resultad.write("owl:Class\n")
                                resultad.write("  |rdfs:subClassOf\n")

                                try:
                                    escribir_tipo(o, "  |  |", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_name} trying to obatin the type of {o}\n')
                                
                                showTipo(o, "  |  |")

                    # Hay algun predicado para ese sujeto que sea "owl:equivalentClass"?
                    if "owl:equivalentClass" in subjects[s]:

                        # Iterar los objetos para ese sujeto y predicado
                        for o in sorted(subjects[s]["owl:equivalentClass"]):

                            # El objeto representa una clase anonima?
                            if o in subjects and "Anonimo" in o:
                                contador += 1
                                resultados.write("\n")
                                # Pintar de donde sale esta tripleta
                                resultados.write(f'Ontología: {ont_prefix}\n')
                                resultados.write(f'Estructura: {ont_prefix}-{contador}\n')
                                resultados.write(s+"\n")
                                resultados.write("  |owl:equivalentClass\n")
                                resultados.write(f'  |  |{o}\n')
                                show_term(o,"  |  |", [])

                                visitado=[]
                                resultad.write("\n")
                                # Pintar de donde sale esta tripleta
                                resultad.write(f'Ontología: {ont_prefix}\n')
                                resultad.write(f'Estructura: {ont_prefix}-{contador}\n')
                                resultad.write("owl:Class\n")
                                resultad.write("  |owl:equivalentClass\n")

                                try:
                                    escribir_tipo(o, "  |  |", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_prefix} trying to obatin the type of {o}\n')
                                
                                showTipo(o, "  |  |")

                # prefijo de la ontología; numero de tripletas de esa ontología que satisfacen las condiciones
                result.write(f'{ont_prefix};{contador};\n')        
                print(f"{ont_prefix} - {contador}")

            except:
                error_log.write(f'An unexpected error occurs parsing {ont_name}\n')

# Function to show the name of a term
def show_term(term, text, already_visited):

    # Has the term been visited before?
    if term not in already_visited:
        already_visited.append(term)

        # Iterate the "predicate" for the triples in which the term is the "subject"
        for p in sorted(subjects[term].keys()):

            # Skip "rdf:type" predicates
            if p!="rdf:type":
                 
                # Iterar los objetos para ese sujeto y predicado (ordenadas alfabeticamente)
                for o in sorted(subjects[term][p]):

                    resultados.write(f'{text}  |{p}\n')
                    resultados.write(f'{text}  |  |{o}\n')

                    # Is the object of the triple an anonymous class?
                    if o in subjects and o != term and "Anonimo" in o:
                        show_term(o, f'{text}  |  |')

def escribir_tipo(o, text, error_log):

    if o in subjects and 'rdf:type' in subjects[o]:
        # Adquirir tipos para ese elemento
        types = subjects[o]["rdf:type"]

    
        # Es un individuo?
        if 'owl:NamedIndividual' in types:
            resultad.write(f'{text}owl:NamedIndividual\n')
        
        else:
            # Ordenar alfabeticamente los tipos
            types.sort()
            resultad.write(f'{text}{", ".join(types)}\n')

    else:

        if "Anonimo" in o: 
            resultad.write(f'{text}Anonimo\n')

        elif 'xsd' in o:
            resultad.write(f'{text}Datatype\n')

        elif "Literal" in o:
            resultad.write(f'{text}Literal\n')

        elif 'owl:Thing' == o:
            resultad.write(f'{text}owl:Class\n')

        else:
            # Ver si el termino ha sido definido en una de las ontologías importadas
            types = term_reuse(o, error_log)

            if types:

                # Es un individuo?
                if 'owl:NamedIndividual' in types:
                    resultad.write(f'{text}owl:NamedIndividual\n')
                
                else:
                    # Ordenar alfabeticamente los tipos
                    types.sort()
                    resultad.write(f'{text}{", ".join(types)}\n')
            
            else:
                resultad.write(f'{text}#Desconocido\n')

def term_reuse(term, error_log):
    types = []
    term_uri = term

    # El termino esta definido como "prefijo:sufijo"?
    if term_uri[0] != '<' and term_uri[-1] != '>':
        # Obtener el prefijo
        prefix, suffix = term.split(':', 1)
        # Sabemos que ese prefijo ha sido definido en la ontología (sino rdflib no lo dividiría en 
        # "prefijo:sufijo"). Por ello, obtenemos el namespace.
        ns = namespaces[prefix]
        term_uri = f'{ns}{suffix}'

        try:

            if ns not in ont_import:
                ont_import [ns] = 0
                aux_g.parse(ns)
                
        except:
            error_log.write(f'Failure in the ontology {ont_prefix} loading the soft reuse of a term of the ontology {ns}\n')
    
    else:
        # El termino es una URI completa (no se ha definido un prefijo en la ontologia).
        # En este caso tenemos que obtener lo que seria el prefijo para cargar la ontología a la que hace referencia.
        try:
            
            # En rdflib si no se ha definido un namespace para dicha URI, la URI esta entre '<' y '>'
            term_uri = term_uri[1:-1]

            ns = obtener_prefijo(term_uri)
            
            try:
                if ns not in ont_import:
                    ont_import [ns] = 0
                    aux_g.parse(ns)
                    
            except:
                error_log.write(f'Failure in the ontology {ont_prefix} loading the soft reuse of a term of the ontology {ns}\n')

        except:
            error_log.write(f'Failure in the ontology {ont_prefix} reading the prefix of the term {term_uri}\n')

    uri_ref = URIRef(term_uri)

    for o2 in aux_g.objects(uri_ref, RDF.type):
        types.append(o2.n3(aux_g.namespace_manager))

    return types

# Funcion para obtener el prefijo de una URI. 
# Recorremos la URI en sentido inverso hasta encontrar un '#' o un '/'.
def obtener_prefijo(term_uri):
    prefix = ''
    last_hash_or_slash = False
    for i in reversed(term_uri):

        if i == '/' or i == '#':
            last_hash_or_slash = True

        if last_hash_or_slash:
            prefix = i + prefix

    return prefix

def showTipo(a, b):
    return

# Function to store the namespaces, which are definined in an ontology, in a dicionary
# called "namespaces".
def get_namespaces(g_namespaces):

    for prefix, suffix in g_namespaces:
        namespaces[prefix] = suffix

# Esta función te parsea los terminos identificados por rdflib a sus respectivos "prefijo:sufijo".
# term_uri es la uri del termino, i representa si se ha encontrado en un triple como sujeto (1), predicado (2)
# u objeto (3). Tipo es el tipo que utiliza rdflib para representar el tipo de los terminos (clase, clase anonima, etc)
def tag(term_type, term_name, error_log):
    global anonimizador
    # Esta variable va a almacenar el "prefijo:sufijo" del termino
    tag=""

    # Es una clase anonima?
    if "BNode" in term_type:

        # Esta clase anonima no ha sido visitada?
        if term_name not in anonymous:
            # Crear identificado de la clase anonima
            tag = f'Anonimo{anonimizador}'
            # Guardar identificador de la clase anonima
            anonymous[term_name] = tag
            anonimizador += 1

        else:
            # Adquirir identificador de la clase anonima
            tag = anonymous[term_name]

    # Es una URI?
    elif "Ref" in term_type:
        tag = term_name

    # Es un literal?
    elif "Literal" in term_type:
        tag = f"Literal [{term_name}]"

    # Se ha podido identificar que representa el termino?
    if tag=="":
        # Este caso no deberia pasar
        tag="None"
        error_log.write('None')
        error_log.write(f"{term_name}-{term_type}")

    return (tag)

# Function to parse the triples of the ontology into a dictionary called "subjects".
def parse_ontology(ont_path, error_log):

    try:
        # Parsing the ontology into a graph
        g = Graph()
        g.parse(ont_path)
    
    except:
        error_log.write(f'Error parsing the ontology: {ont_path}')
        return

    # Load ontology namespaces
    get_namespaces(g.namespaces())
    # Parse ontology owl:imports
    parse_imports(g, error_log)

    # Iterate ontology triples
    for triple in g:

        # Is it really a triple?
        if len(triple) == 3:

            # Adquirir "prefijo:sufijo" del sujeto
            tag1 = tag(str(type(triple[0])), triple[0].n3(g.namespace_manager), error_log)
            # Adquirir "prefijo:sufijo" del predicado
            tag2 = tag(str(type(triple[1])), triple[1].n3(g.namespace_manager), error_log)
            # Adquirir "prefijo:sufijo" del objeto
            tag3 = tag(str(type(triple[2])), triple[2].n3(g.namespace_manager), error_log)

        # Have the elements of the triple been correctly identified?
        if tag1 != "None" and tag2 != "None" and tag3 != "None":

            if tag1 not in subjects: 
                subjects[tag1] = {}

            if tag2 not in subjects[tag1]: 
                subjects[tag1][tag2] = []

            if tag3 not in subjects[tag1][tag2]: 
                subjects[tag1][tag2].append(tag3)

    
# Function to parse the imported ontologies
def parse_imports(g, error_log):
    
    # Iterate the triples whose predicate is "owl:imports"
    for o in g.objects(None, URIRef('http://www.w3.org/2002/07/owl#imports'), None):

        try:

            # Has the ontology been imported?
            if o not in ont_import:
                ont_import[o] = 0
                aux_g.parse(o)       
        
        except:
            error_log.write(f'Failure in the ontology {ont_prefix} loading the owl:imports {o}\n')

# Function to check if the path to the ontology is really a file.
def ontology_path_error(ont_path, error_log):

    # Is a file path?
    if not os.path.isfile(ont_path):
        error_log.write(f'Error loading the path {ont_path}. It is not an ontology\n')
    
    else:
        return True
    
    return False