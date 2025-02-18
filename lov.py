import argparse
import os.path
from Code.detectPatterns.download_ontology import download_ontologies
from Code.detectPatterns.create_structure import create_structure
from Code.detectPatterns.identify_patterns import identify_patterns
from Code.detectPatterns.infer_structures import infer_structures

def structure(ontology_path, output_path, preffix, flatten):

    error_log_path = os.path.join(output_path, 'error_log.txt')
    structure_csv_path = os.path.join(output_path, 'Structure.csv')
    structure_type_path = os.path.join(output_path, 'Structure_term_type.txt')
    structure_name_path = os.path.join(output_path, 'Structure_term_name.txt')
    inferred_type_path = os.path.join(output_path, 'Structure_term_inferred_type.txt')
    inferred_blank_nodes_path = os.path.join(output_path, 'Structure_term_inferred_blank_nodes.txt')

    # Create a new file in which to write the logs 
    error_log = open(error_log_path , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    error_log.truncate()

    flatten = True if flatten == 'flatten' else False

    create_structure(ontology_path, error_log, flatten, structure_csv_path, structure_type_path, structure_name_path, True, preffix)
    infer_structures(inferred_type_path, inferred_blank_nodes_path, structure_type_path, structure_name_path)

    error_log.close()

def patterns(inferred_type_path, inferred_blank_nodes_path, patterns_type):
    print("[")
    if patterns_type == 'type':
        identify_patterns(inferred_type_path, None, True, "type")
    
    # Has the user specified that the patterns are going to be created from the name of the terms?
    elif patterns_type == 'name':
        identify_patterns(inferred_blank_nodes_path, None, True, "name")
    
    else:
        identify_patterns(inferred_type_path, None, True, "type")
        print(",")
        identify_patterns(inferred_blank_nodes_path, None, True, "name")
    print("]")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Identify patterns from a set of ontologies')
    parser.add_argument('-t', '--type', 
                        choices=['structure', 'pattern'])
    parser.add_argument('-ontology', '--ontology_path', 
                        default='',
                        type=str)
    parser.add_argument('-p', '--preffix', 
                        default='',
                        type=str)
    parser.add_argument('-output', '--output_path',
                        type=str,
                        default='')
    parser.add_argument('-patterns', '--patterns_type', 
                        type=str, 
                        choices=['type', 'name', 'both'],
                        default='type')
    parser.add_argument('-t_p', '--type_path', 
                        type=str, 
                        nargs='+',
                        default='')
    parser.add_argument('-n_p', '--name_path', 
                        nargs='+',
                        type=str,
                        default='')
    parser.add_argument('-f', '--flatten', 
                        type=str, 
                        choices=['flatten', 'not_flatten'],
                        default='not_flatten')
    
    args = parser.parse_args()
    if args.type == 'structure':
        structure(args.ontology_path, args.output_path, args.preffix, args.flatten)
    else:
        patterns(args.type_path, args.name_path, args.patterns_type)