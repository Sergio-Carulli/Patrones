import os.path
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

# Function which creates the structures found in each ontology
def identify_reuse(ontology_path, reuse_log):
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
        reuse_log.write(f'Loading ontology {ont_name}\n')

        # Is there not an error in the ontology file?
        if ontology_path_error(ont_path, reuse_log):
            
            try:
                # Emptying dictionaries
                namespaces = {}
                ont_import = {}

                # Parse ontology
                parse_ontology(ont_path, reuse_log)

            except:
                reuse_log.write(f'An unexpected error occurs parsing {ont_name}\n')

def parse_ontology(ont_path, reuse_log):

    try:
        # Parsing the ontology into a graph
        g = Graph()
        g.parse(ont_path)
    
    except:
        reuse_log.write(f'Error parsing the ontologyww: {ont_path}\n')
        print(f'Error parsing the ontology: {ont_path}')

    try:
        ont_uris = {}
        hard_reuse = {}
        soft_reuse = {}
        ont_ann = {}
        print('Hola')
        ont_uri = ""
        # Get the ontology uri
        for s in g.subjects(RDF.type, URIRef('http://www.w3.org/2002/07/owl#Ontology')):
            print(s.strip())
            ont_uri = s.strip()

        print('Hola')
        # Get the owl:imports
        for o in g.objects(None, URIRef('http://www.w3.org/2002/07/owl#imports'), None):
            print(o)
            hard_reuse[o.strip()] = 0

        # Get the annotation properties
        for s in g.subjects(None, URIRef('http://www.w3.org/2002/07/owl#AnnotationProperty')):
            print(s)
            ont_ann[s] = 0

        for s, p, o in g:

            if s.strip() != ont_uri and s not in ont_ann:
                check_uri(s, ont_uris)

                if p not in ont_ann:
                    check_uri(p, ont_uris)
                    check_uri(o, ont_uris)
        
        for k in ont_uris:
            check_reuse(k, reuse_log, ont_uri, hard_reuse, soft_reuse)

        for k, v in hard_reuse.items():
            reuse_log.write(f'Hard reuse: {k} utilizado {v}\n')
        
        for k, v in soft_reuse.items():

            if k != 'http://www.w3.org/2000/01/rdf-schema#':

                if k != 'http://www.w3.org/2002/07/owl#':

                    if k != 'http://www.w3.org/2001/XMLSchema#':

                        if k != 'http://www.w3.org/1999/02/22-rdf-syntax-ns#':
                            reuse_log.write(f'Soft reuse: {k} utilizado {v}\n')
    
    except:
        reuse_log.write(f'Error parsing the ontology: {ont_path}\n')
        print(f'Error parsing the ontology: {ont_path}')

def check_reuse(term, reuse_log, ont_uri, hard_reuse, soft_reuse):

    prefix = get_prefix(term).strip()
    if prefix == ont_uri:
        return
    
    elif prefix in hard_reuse:
        hard_reuse[prefix] += 1
    
    elif prefix in soft_reuse:
        soft_reuse[prefix] += 1

    else:
        soft_reuse[prefix] = 1

def check_uri(term, ont_uris):

    if "<class 'rdflib.term.URIRef'>" == str(type(term)):
        ont_uris[str(term).strip()] = 0

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

    return term_uri[0:last_hash_or_slash + 1]

def ontology_path_error(yes, no):
    return True

