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
aux_g = ''

# Create a new file in which to write the number of structures found per ontology 
structure_csv = ''

# Create a new file in which to write the type of the structures found 
# (writing the type of the terms)
structure_type = ''

# Create a new file in which to write the type of the structures found 
# (writing the URI of the terms)
structure_name = ''

def create_files():
    global structure_csv, structure_type, structure_name

    # Create a new file in which to write the number of structures found per ontology 
    structure_csv = open("Structure.csv", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_csv.truncate()
    # Naming the columns
    structure_csv.write("Ontology;Number of structures;\n")

    # Create a new file in which to write the type of the structures found 
    # (writing the type of the terms)
    structure_type = open("Structure_term_type.txt", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_type.truncate()

    # Create a new file in which to write the type of the structures found 
    # (writing the URI of the terms)
    structure_name = open("Structure_term_name.txt", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_name.truncate()

def create_structure(ontology_path, error_log):
    create_files()
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

        # Is there not an error in the ontology file?
        if ontology_path_error(ont_path, error_log):
            # Optional print to see from the terminal what is happening
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

                # Variable which is used to create an unique identifier per structure
                structure_id = 0

                # Iterate in alphabetical order the terms that are the "subject" of a triple
                for s in sorted(subjects.keys()):

                    # Is there a "rdfs:subclassOf" "predicate" for that "subject"?
                    if "rdfs:subClassOf" in subjects[s]:

                        # Iterate the "object" for that "subject" and "predicate"
                        for o in sorted(subjects[s]["rdfs:subClassOf"]):

                            # Does the "object" represents an anonymous class?
                            if o in subjects and "Anonymous" in o:
                                # New structure found
                                structure_id += 1

                                # Write the structure (writing the URI of the terms)
                                structure_name.write("\n")
                                structure_name.write(f'Ontology: {ont_name}\n')
                                structure_name.write(f'Structure: {ont_name}-{structure_id}\n')
                                structure_name.write(f'{s}\n')
                                structure_name.write("  |rdfs:subClassOf\n")
                                structure_name.write(f'  |  |{o}\n')

                                # Write the structure (writing the type of the terms)
                                structure_type.write("\n")
                                structure_type.write(f'Ontology: {ont_name}\n')
                                structure_type.write(f'Structure: {ont_name}-{structure_id}\n')

                                try:
                                    # Write the type of the "subject"
                                    write_type(s, "", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')

                                structure_type.write("  |rdfs:subClassOf\n")

                                try:
                                    # Write the type of the "object"
                                    write_type(o, "  |  |", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_name} trying to obtain the type of {o}\n')
                                
                                iterate_structure(o, "  |  |", error_log, [])

                    # # Is there a "owl:equivalentClass" "predicate" for that "subject"?
                    if "owl:equivalentClass" in subjects[s]:

                        # Iterar los objetos para ese sujeto y predicado
                        for o in sorted(subjects[s]["owl:equivalentClass"]):

                            # El objeto representa una clase anonima?
                            if o in subjects and "Anonymous" in o:
                                # New structure found
                                structure_id += 1

                                # Write the structure (writing the URI of the terms)
                                structure_name.write("\n")
                                structure_name.write(f'Ontology: {ont_prefix}\n')
                                structure_name.write(f'Structure: {ont_prefix}-{structure_id}\n')
                                structure_name.write(f'{s}\n')
                                structure_name.write("  |owl:equivalentClass\n")
                                structure_name.write(f'  |  |{o}\n')

                                # Write the structure (writing the type of the terms)
                                structure_type.write("\n")
                                structure_type.write(f'Ontology: {ont_prefix}\n')
                                structure_type.write(f'Structure: {ont_prefix}-{structure_id}\n')

                                try:
                                    # Write the type of the "subject"
                                    write_type(s, "", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')

                                structure_type.write("  |owl:equivalentClass\n")

                                try:
                                    # Write the type of the "object"
                                    write_type(o, "  |  |", error_log)

                                except:
                                    error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')
                                
                                iterate_structure(o, "  |  |", error_log, [])

                # Write the number of structures found for each ontology 
                structure_csv.write(f'{ont_prefix};{structure_id};\n')        
                print(f"{ont_prefix} - {structure_id}")

            except:
                error_log.write(f'An unexpected error occurs parsing {ont_name}\n')
    
    # Close files
    structure_csv.close()
    structure_type.close()
    structure_name.close()

# Function to write the URI and the type of the "predicate" and "object" of triples whose
# "subject" is an anonymous class.
def iterate_structure(term, text, error_log, already_visited):

    # Has the term been visited before?
    if term not in already_visited:
        already_visited.append(term)

        # Iterate the "predicate" for the triples in which the term is the "subject"
        for p in sorted(subjects[term].keys()):

            # Skip "rdf:type" predicates
            if p!="rdf:type":
                 
                # Iterate in alphabetical order the "objects" for that "subject" and "predicate"
                for o in sorted(subjects[term][p]):
                    # Write the URI of the "predicate" and the "object"
                    structure_name.write(f'{text}  |{p}\n')
                    structure_name.write(f'{text}  |  |{o}\n')

                    # Write the type of the "predicate" and the "object"
                    try:
                        structure_type.write(text+"  |"+p+"\n")
                        write_type(o, f'{text}  |  |', error_log)
                        
                    except:
                        error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')

                    # Is the object of the triple an anonymous class?
                    if o in subjects and o != term and "Anonymous" in o:
                        iterate_structure(o, f'{text}  |  |', error_log, already_visited)

# Function to write the type of a term
def write_type(o, text, error_log):

    # Is the type of the element defined in the ontology?
    if o in subjects and 'rdf:type' in subjects[o]:
        # Get the "objects" of the triples whose "predicate" is "rdf:type"
        types = subjects[o]["rdf:type"]
        alphabetical_order(types, text)

    else:
        # In this case we are reading:
        #   - a term which does not need a declaration (anonymous class or a dataype)
        #   - a reused term

        # Is it an anonymous class?
        if "Anonymous" in o: 
            structure_type.write(f'{text}owl:Class\n')
        
        # Is it a literal?
        elif "Literal" in o:
            structure_type.write(f'{text}Literal\n')

        # Is it a datatype?
        elif 'xsd' in o:
            structure_type.write(f'{text}Datatype\n')

        # Is it a class?
        elif 'owl:Thing' == o:
            structure_type.write(f'{text}owl:Class\n')

        else:
            # In this case the term may be reused from another ontology
            types = term_reuse(o, error_log)

            # Does the term has been defined in another ontology?
            if types:
                alphabetical_order(types, text)

            else:
                # The type of the term has not been obtained
                structure_type.write(f'{text}#Unknown\n')

# Function to write in alphabetical order the types of a term
def alphabetical_order(types, text):
    # Is the term an individual?
    if 'owl:NamedIndividual' in types:
        # This is a special type because we want to skip the class membership
        structure_type.write(f'{text}owl:NamedIndividual\n')
    
    else:
        # Write alphabetically the types of the term
        types.sort()
        structure_type.write(f'{text}{", ".join(types)}\n')

# Function to get the types of a term which is defined in another ontology
def term_reuse(term, error_log):
    # Array to store the types of the term
    types = []
    # Variable to store the term URI (without namespace)
    term_uri = term

    # Is the term URI defined through a namespace? (i.e. "prefix:suffix")
    if term[0] != '<' and term[-1] != '>':
        # Get the prefix and the suffix
        prefix, suffix = term.split(':', 1)
        # We know that the prefix has been defined in the ontology (otherwise rdflib would not have defined
        # the URI through a namespace). For that reason, the namespace is obtained.
        ns = namespaces[prefix]
        # Define the term URI without namespace
        term_uri = f'{ns}{suffix}'
        # Parse the ontology
        parse_ontology_soft_reuse(ns, error_log)

    else:
        # In this case the term URI has been defined without a namespace (there is not a prefix defined 
        # in the ontology). It is neccesary to obtain the part of the URI which refers to the ontology where the
        # term is defined.

        # In rdflib if no namespace has been defined for that URI, the URI is between '<' and '>'
        term_uri = term_uri[1:-1]
        # Get the part of the URI which refers to the ontology
        ns = get_prefix(term_uri)
        # Parse the ontology
        parse_ontology_soft_reuse(ns, error_log)

    # Write the URI in rdflib format
    uri_ref = URIRef(term_uri)

    # Get the triples where the "subject" is the term and the "predicate" is "rdf:type"
    for o2 in aux_g.objects(uri_ref, RDF.type):
        types.append(o2.n3(aux_g.namespace_manager))

    return types

# Function to parse the ontologies of terms which are used in a soft reuse
def parse_ontology_soft_reuse(ns, error_log):
    
    try:

        # Has the ontology been imported?
        if ns not in ont_import:
            ont_import [ns] = 0
            # Parse the ontology
            aux_g.parse(ns)
            
    except:
        error_log.write(f'Failure in the ontology {ont_prefix} loading the soft reuse of a term of the ontology {ns}\n')

# Function to obtain the prefix of an URI (the part of the URI which is before the last
# '#' or '/').
def get_prefix(term_uri):
    # Variable to store the position of the last '#' or '/'
    last_hash_or_slash = len(term_uri) - 1

    # Iterate the URI in reversed way
    for i in range(last_hash_or_slash, -1, -1):
        # Get the char which is stored in the position i
        char = term_uri[i]

        # Is the char an '/' or an '#'?
        if char == '/' or char == '#':
            last_hash_or_slash = i
            break


    """# Iterate the URI in reverse way
    for i in reversed(term_uri):

        if i == '/' or i == '#':
            last_hash_or_slash = True

        if last_hash_or_slash:
            prefix = i + prefix"""

    return term_uri[0:last_hash_or_slash]

# Function to store the namespaces, which are definined in an ontology, in a dictionary
# called "namespaces".
def get_namespaces(g_namespaces):

    for prefix, suffix in g_namespaces:
        namespaces[prefix] = suffix

# This function get the URI of the terms which have been identified by rdflib. There are three cases:
#   - URI: the term represents an URI
#   - Anonymous class: the term represents an anonymous class
#   - Data value: the term represents a data value
def tag(term_type, term_name, error_log):
    global anonimizador
    # Variable to store the URI of the term
    tag=""

    # Is the term an anonymous class?
    if "BNode" in term_type:

        # Has been this anonymous class been visited before?
        if term_name not in anonymous:
            # Create an unique identifier for that anonymous classS
            tag = f'Anonymous{anonimizador}'
            # Store the unique identifier of that anonymous class
            anonymous[term_name] = tag
            anonimizador += 1

        else:
            # Get the unique identifier of that anonymous class
            tag = anonymous[term_name]

    # Is the term an URI?
    elif "Ref" in term_type:
        tag = term_name

    # Is the term a data value?
    elif "Literal" in term_type:
        tag = f"Literal [{term_name}]"

    # Was it possible to identify what the term represent?
    if tag == "":
        # This case should not happen
        tag = "None"
        error_log.write(f"A None has been identified in the ontology {ont_prefix} in the term {term_name}-{term_type}\n")

    return (tag)

# Function to parse the triples of the ontology into a dictionary called "subjects"
def parse_ontology(ont_path, error_log):

    try:
        # Parsing the ontology into a graph
        g = Graph()
        g.parse(ont_path)
    
    except:
        error_log.write(f'Error parsing the ontology: {ont_path}\n')
        return

    # Load ontology namespaces
    get_namespaces(g.namespaces())
    # Parse ontology owl:imports
    parse_imports(g, error_log)

    # Iterate ontology triples
    for triple in g:

        # Is it really a triple?
        if len(triple) == 3:

            # Get the URI of the "subject"
            tag1 = tag(str(type(triple[0])), triple[0].n3(g.namespace_manager), error_log)
            # Get the URI of the "predicate"
            tag2 = tag(str(type(triple[1])), triple[1].n3(g.namespace_manager), error_log)
            # Get the URI of the "object"
            tag3 = tag(str(type(triple[2])), triple[2].n3(g.namespace_manager), error_log)

        # Have the elements of the triple been correctly identified?
        if tag1 != "None" and tag2 != "None" and tag3 != "None":
            # Store the triple in the subjects dictionary

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
                # Parse the imported ontology
                aux_g.parse(o)       
        
        except:
            error_log.write(f'Failure in the ontology {ont_prefix} loading the owl:imports {o}\n')

# Function to check if the path to the ontology is really a file
def ontology_path_error(ont_path, error_log):

    # Is a file path?
    if not os.path.isfile(ont_path):
        error_log.write(f'Error loading the path {ont_path}. It is not an ontology\n')
    
    else:
        return True
    
    return False