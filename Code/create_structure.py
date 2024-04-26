import os.path
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

# Dictionary with the predefined datatypes
predefined_datatypes = {
    'owl:rational':'',
    'http://www.w3.org/2002/07/owl#rational':'',
    'owl:real':'',
    'http://www.w3.org/2002/07/owl#real':'',
    'rdf:langString':'',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString':'',
    'rdf:PlainLiteral':'',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral':'',
    'rdf:XMLLiteral':'',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral':'',
    'rdfs:Literal':'',
    'http://www.w3.org/2000/01/rdf-schema#Literal':'',
    'xsd:anyURI':'',
    'xsd:base64Binary':'',
    'xsd:boolean':'',
    'xsd:byte':'',
    'xsd:dateTime':'',
    'xsd:dateTimeStamp':'',
    'xsd:decimal':'',
    'xsd:double':'',
    'xsd:float':'',
    'xsd:hexBinary':'',
    'xsd:int':'',
    'xsd:integer':'',
    'xsd:language':'',
    'xsd:long':'',
    'xsd:Name':'',
    'xsd:NCName':'',
    'xsd:negativeInteger':'',
    'xsd:NMTOKEN':'',
    'xsd:nonNegativeInteger':'',
    'xsd:nonPositiveInteger':'',
    'xsd:normalizedString':'',
    'xsd:positiveInteger':'',
    'xsd:short':'',
    'xsd:string':'',
    'xsd:token':'',
    'xsd:unsignedByte':'',
    'xsd:unsignedInt':'',
    'xsd:unsignedLong':'',
    'xsd:unsignedShort':''
    }

# Dictionary to store the ontology triples whose:
#   - key: subject of a triple
#   - value: dictionary to store the "predicate" and "object" of triples with the same "subject" whose:
#       - key: triple predicate whose subject is the key of the above dictionary
#       - value: a list which represents the "object" of triples with the same "subject" and "predicate"
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

# Function to create the files in which the results are going to be written
def create_files(structure_csv_path, structure_type_path, structure_name_path):
    global structure_csv, structure_type, structure_name

    # Create a new file in which to write the number of structures found per ontology 
    structure_csv = open(structure_csv_path, 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_csv.truncate()
    # Naming the columns
    structure_csv.write("Ontology;Number of structures;\n")

    # Create a new file in which to write the type of the structures found 
    # (writing the type of the terms)
    structure_type = open(structure_type_path, 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_type.truncate()

    # Create a new file in which to write the type of the structures found 
    # (writing the URI of the terms)
    structure_name = open(structure_name_path, 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    structure_name.truncate()

# Function which creates the structures found in each ontology
def create_structure(ontology_path, error_log, flatten, structure_csv_path, structure_type_path, structure_name_path):
    # Create the files in which the results are going to be written
    create_files(structure_csv_path, structure_type_path, structure_name_path)
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
        # Optional print to see from the terminal what is happening
        print(f'Loading ontology {ont_name}')

        # Is there not an error in the ontology file?
        if ontology_path_error(ont_path, error_log):
            
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
                        structure_id = iterate_class_axiom(s, "rdfs:subClassOf", structure_id, ont_name, error_log, flatten)

                    # Is there a "owl:equivalentClass" "predicate" for that "subject"?
                    if "owl:equivalentClass" in subjects[s]:
                        structure_id = iterate_class_axiom(s, "owl:equivalentClass", structure_id, ont_name, error_log, flatten)
                    
                    # Is there a "owl:disjointWith" "predicate" for that "subject"?
                    if "owl:disjointWith" in subjects[s]:
                        structure_id = iterate_class_axiom(s, "owl:disjointWith", structure_id, ont_name, error_log, flatten)

                # Write the number of structures found for each ontology 
                structure_csv.write(f'{ont_prefix};{structure_id};\n')  
                # Optional print to see from the terminal what is happening      
                print(f"{ont_prefix} - {structure_id}")

            except:
                error_log.write(f'An unexpected error occurs parsing {ont_name}\n')
    
    # Write and empty line which indicates the end of the file
    structure_type.write('\n')
    structure_name.write('\n')
    # Close files
    structure_csv.close()
    structure_type.close()
    structure_name.close()

# This function iterates the triples whose predicate represents a class axiom (e.g. rdfs:subClassOf, etc).
# Moreover, just the triples whose object represents a blank node are going to be iterate.
def iterate_class_axiom(s, class_axiom, structure_id, ont_name, error_log, flatten):
     # Iterate the "object" for that "subject" and "predicate"
    for o in sorted(subjects[s][class_axiom]):

        # Does the "object" represents an anonymous class?
        if o in subjects and "Blank node" in o:
            # New structure found
            structure_id += 1

            # Write the structure (writing the URI of the terms)
            structure_name.write("\n")
            structure_name.write(f'Ontology: {ont_name}\n')
            structure_name.write(f'Structure: {ont_name}-{structure_id}\n')
            structure_name.write(f'{s}\n')
            structure_name.write(f'  |{class_axiom}\n')

            # Write the structure (writing the type of the terms)
            structure_type.write("\n")
            structure_type.write(f'Ontology: {ont_name}\n')
            structure_type.write(f'Structure: {ont_name}-{structure_id}\n')

            try:
                # Write the type of the triple subject
                term_type = get_type(s, error_log)
                structure_type.write(f"{term_type}\n")

            except:
                error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')

            structure_type.write(f'  |{class_axiom}\n')
            # Write the URI and the type of the triple object
            term_name, term_type = write_object(o, error_log)
            structure_name.write(f'{"  |  |"}{term_name}\n')
            structure_type.write(f'{"  |  |"}{term_type}\n')
            # Iterate the triples from which the blank node (the object of this triple) is the subject
            aux_name, aux_type, blank_found = iterate_structure(o, "  |  |", error_log, [], flatten)
            structure_name.write(aux_name)
            structure_type.write(aux_type)
        
    return structure_id

# Function to write the URI and the type of the "predicate" and "object" of triples whose
# "subject" is an anonymous class.
def iterate_structure(term, text, error_log, already_visited, flatten):
    aux_name = ''
    aux_type = ''
    list_found = False
    blank_found = False
    # Has the term been visited before?
    if term not in already_visited:
        already_visited.append(term)

        # Iterate the "predicate" for the triples in which the term is the "subject"
        for p in sorted(subjects[term].keys()):

            # Skip "rdf:type" predicates
            if p!="rdf:type" and (p.startswith("rdf:") or p.startswith("rdfs:") or p.startswith("owl:") or p.startswith("xsd:")):
                 
                # Iterate in alphabetical order the "objects" for that "subject" and "predicate"
                for o in sorted(subjects[term][p]):
                    # Write the URI of the "predicate"
                    aux_name += f'{text}  |{p}\n'
                    aux_type += f'{text}  |{p}\n'
                    """structure_name.write(f'{text}  |{p}\n')
                    structure_type.write(f'{text}  |{p}\n')"""

                    # Has the user indicated to flatten the lists?
                    if flatten and p == 'owl:oneOf':
                        # In this case the flatten flag is active and the terms which are involved in and enumeration are
                        # not going to be written
                        continue

                    # Does the predicate represent the origin of a list?
                    if p == 'owl:intersectionOf' or p == 'owl:unionOf' or p == 'owl:withRestrictions' or p == 'owl:oneOf':
                        list_found = True
                        blank_found = True

                    # Does the predicate represent the next element of a list?
                    elif p == 'rdf:rest':

                        # Is there another element in the list?
                        if o != 'rdf:nil':
                            # Declare the beginning of another element in the list
                            aux_name += f'{text}  |  |rdf:List\n'
                            aux_type += f'{text}  |  |rdf:List\n'
                        
                        else:
                            # In this case the end of the list have been reached
                            # Declare the ending of the list
                            aux_name += f'{text}  |  |rdf:nil\n'
                            aux_type += f'{text}  |  |rdf:nil\n'
                    
                    else:
                        # Write the type and the URI of the "object"
                        term_name, term_type = write_object(o, error_log)
                        aux_name += f'{text}  |  |{term_name}\n'
                        aux_type += f'{text}  |  |{term_type}\n'
                        blank_found = blank_found or "Blank node" in o

                    # Is the object of the triple an anonymous class?
                    if o in subjects and o != term and "Blank node" in o:
                        # Iterate the triples from which the blank node (the object of this triple) is the subject
                        aux_name2, aux_type2, blank_found2 = iterate_structure(o, f'{text}  |  |', error_log, already_visited, flatten)

                        if list_found:

                            if flatten:
                                list_found = False

                                if not blank_found2:
                                    continue
                            
                            else:
                                # Declare the beginning of a list
                                aux_name += f'{text}  |  |rdf:List\n'
                                aux_type += f'{text}  |  |rdf:List\n'                    
                        
                        blank_found = blank_found or blank_found2
                        aux_name += aux_name2
                        aux_type += aux_type2    
    
    return aux_name, aux_type, blank_found

# This function writes the URI and the type of a term which is the object of a triple.
# One file just contains the URI of the terms. However, if the term represents a blank node, it does not have an URI defined.
# In this case, the type of the blank node (what it represents) is written. 
# If the blank node does not have a type defined, its type is generalized to "Blank node"
def write_object(o, error_log):

    try:
        # Get the type of the term
        term_type = get_type(o, error_log)

        # Does the term represent a blank node?
        if "Blank node" in o:
            # In this case the term does not have an URI

            # Has the type of the blank node been identified? 
            if term_type != '#Unknown':
                # Write the type of the blank node
                term_name = term_type
            
            else:
                # Write that the blank node does not have a type defined
                term_name = 'Blank node'
        
        else:
            term_name = o
            # In this case the term has an URI
        
    except:
        # In this case the type of the term has not been obtained
        # This case should not happens
        error_log.write(f'Error in the ontology {ont_prefix} trying to obtain the type of {o}\n')

        # Does the term represent a blank node?
        if "Blank node" in o:
            # Write that the blank node does not have a type defined
            term_name = 'Blank node'
            term_type = 'Blank node'
        
        else:
            # In this case the term has an URI
            term_name = o
            term_type = '#Unknown'
    
    return term_name, term_type

# Function to get the type of a term
def get_type(term, error_log):

    # Is the type of the element defined in the ontology?
    if term in subjects and 'rdf:type' in subjects[term]:
        # Get the "objects" of the triples whose "predicate" is "rdf:type"
        types = subjects[term]["rdf:type"]
        # Cast list to string
        term_type = alphabetical_order(types)

    else:
        # In this case we are reading:
        #   - a term which does not need a declaration (e.g. a data value)
        #   - a reused term (soft or hard reuse)
        #   - a term wrongly declare (e.g. the user forgot to declare the type of the term)

        # Is it an anonymous class?
        if "Blank node" in term:
            term_type = 'Blank node'
        
        # Is it a Data value?
        elif "Data value" in term:
            term_type = 'Data value'

        # Is it a datatype?
        elif term in predefined_datatypes:
            term_type = 'rdfs:Datatype'

        # Is it a class?
        elif 'owl:Thing' == term:
            term_type = 'owl:Class'

        else:
            # In this case the term may be reused from another ontology
            types = term_reuse(term, error_log)

            # Does the term has been defined in another ontology?
            if types:
                # Cast list to string
                term_type = alphabetical_order(types)

            else:
                # The type of the term has not been obtained
                # In this case the term may have been wrongly declared (e.g. the user forgot to declare the type of the term)
                # may be wrongly reused (e.g. the owl:imports which should import the term has failed)
                term_type = '#Unknown'
    
    return term_type

# Function to write in alphabetical order the types of a term.
# There are types which are restrictive, i.e. the information provided by the additional types is not useful
def alphabetical_order(types):

    # Is the term an individual?
    if 'owl:NamedIndividual' in types:
        # This is a special type because we want to skip the class membership
        types_order = 'owl:NamedIndividual'

    # Is the term a restriction?
    elif 'owl:Restriction' in types:
        # This is a special type because we want to skip the aditional types
        # (e.g. some users declare the restriction also as an owl:Class)
        types_order = 'owl:Restriction'

    # Is the term a class?
    elif 'owl:Class' in types or 'rdfs:Class' in types:
        # This is a special type because we want to skip the aditional types
        # (e.g. some users declare the owl:Class also as rdfs:Class)
        types_order = 'owl:Class'
        
    
    else:
        # Write alphabetically the types of the term
        types.sort()
        # List to string
        types_order = ", ".join(types)
    
    return types_order

# Function to get the types of a term which is defined in another ontology
def term_reuse(term, error_log):
    # List to store the types of the term
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

# Function to obtain the prefix of an URI (the part of the URI which is before the last '#' or '/').
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

    return term_uri[0:last_hash_or_slash]

# Function to store the namespaces, which are definined in an ontology, in a dictionary called "namespaces".
def get_namespaces(g_namespaces):

    # Iterate the namespaces defined in the ontology
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
            tag = f'Blank node{anonimizador}'
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
        tag = f"Data value [{term_name}]"

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

        """import pprint
        for stm in g:
            pprint.pprint(stm)"""
    
    except:
        error_log.write(f'Error parsing the ontology: {ont_path}\n')
        print(f'Error parsing the ontology: {ont_path}')
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

    # Is not a file path?
    if not os.path.isfile(ont_path):
        error_log.write(f'Error loading the path {ont_path}. It is not an ontology\n')
    
    else:
        return True
    
    return False