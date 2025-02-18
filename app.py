import argparse
import os.path
from Code.detectPatterns.download_ontology import download_ontologies
from Code.detectPatterns.create_structure import create_structure
from Code.detectPatterns.identify_patterns import identify_patterns
from Code.detectPatterns.infer_structures import infer_structures

def main(ontology_path, csv_path, output_path, patterns_type, flatten_lists):
    print(output_path)
    if output_path != '' and check_output_error(output_path):
        error_log_path = os.path.join(output_path, 'error_log.txt')
        structure_csv_path = os.path.join(output_path, 'Structure.csv')
        structure_type_path = os.path.join(output_path, 'Structure_term_type.txt')
        structure_name_path = os.path.join(output_path, 'Structure_term_name.txt')
        inferred_type_path = os.path.join(output_path, 'Structure_term_inferred_type.txt')
        inferred_blank_nodes_path = os.path.join(output_path, 'Structure_term_inferred_blank_nodes.txt')
        patterns_type_path = os.path.join(output_path, 'Patterns_type')
        patterns_name_path = os.path.join(output_path, 'Patterns_name')
    
    else:
        error_log_path = 'error_log.txt'
        structure_csv_path = 'Structure.csv'
        structure_type_path = 'Structure_term_type.txt'
        structure_name_path = 'Structure_term_name.txt'
        inferred_type_path = 'Structure_term_inferred_type.txt'
        inferred_blank_nodes_path = 'Structure_term_inferred_blank_nodes.txt'
        patterns_type_path = 'Patterns_type'
        patterns_name_path = 'Patterns_name'

    # Create a new file in which to write the logs 
    error_log = open(error_log_path , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    error_log.truncate()
    # Cast string to boolean
    flatten = True if flatten_lists == 'yes' else False

    # Is there an error in the path to the csv file?
    if csv_path != '' and check_csv_error(csv_path, error_log):
        error_log.close()
        exit(-1)

    # Is there an error in the path to the folder with the ontologies?    
    if check_ontology_error(ontology_path, error_log):
        error_log.close()
        exit(-1)

    # Has the user specified a path to a csv file with the ontologies to donwload?
    if csv_path != '':
        download_ontologies(csv_path, ontology_path, error_log)

    create_structure(ontology_path, error_log, flatten, structure_csv_path, structure_type_path, structure_name_path, False, None)
    infer_structures(inferred_type_path, inferred_blank_nodes_path, structure_type_path, structure_name_path)

    # Has the user specified that the patterns are going to be created from the type of the terms?
    if patterns_type == 'type':
        identify_patterns(inferred_type_path, patterns_type_path, False, None)
    
    # Has the user specified that the patterns are going to be created from the name of the terms?
    elif patterns_type == 'name':
        identify_patterns(inferred_blank_nodes_path, patterns_name_path, False, None)
    
    else:
        identify_patterns(inferred_type_path, patterns_type_path, False, None)
        identify_patterns(inferred_blank_nodes_path, patterns_name_path, False, None)

    error_log.close()

# Function to check if the path to the csv is really a csv file.
def check_csv_error(csv_path, error_log):

    # Is a file path?
    if not os.path.isfile(csv_path):
        error_log.write(f'The path --csv_path {csv_path} is not a file\n')
        print(f'The path --csv_path {csv_path} is not a file\n')
    
    # Is a csv path?
    elif not csv_path.endswith('.csv'):
        error_log.write(f'The path --csv_path {csv_path} is not a csv\n')
        print(f'The path --csv_path {csv_path} is not a csv\n')
    
    else:
        return False
    
    return True

# Function to check if the path to the directory where the ontologies are going to be downloaded
# is really a directory.
def check_ontology_error(ontology_path, error_log):

    # Is a directory path?
    if not os.path.isdir(ontology_path):
        error_log.write(f'The path --ontology_path {ontology_path} is not a directory\n')
        print(f'The path --ontology_path {ontology_path} is not a directory\n')
    
    else:
        return False
    
    return True

# Function to check if the path to the directory where the output is going to be stored
# is really a directory.
def check_output_error(output_path):

    # Is a directory path?
    if not os.path.isdir(output_path):
        print(f'The path --output_path {output_path} is not a directory\n')
    
    else:
        return True
    
    return False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Identify patterns from a set of ontologies')
    parser.add_argument('-ontology', '--ontology_path', 
                        type=str, 
                        help='Path to a folder where the ontologies are going to be downloaded. The patterns are going to be identified using the ontologies stored in this folder')
    parser.add_argument('-csv', '--csv_path', 
                        type=str, 
                        help='Path to the csv file indicating what ontologies are going to be downloaded',
                        default='')
    parser.add_argument('-output', '--output_path', 
                        type=str, 
                        help='Path to to a folder where the output of this application is going to be stored. If a path is not provided, the output is going to be stored in the current directory',
                        default='')
    parser.add_argument('-patterns', '--patterns_type', 
                        type=str, 
                        help='Flag to indicate if the patterns are going to be created from the type of the terms or from the name of the terms or from both',
                        choices=['type', 'name', 'both'],
                        default='type')
    parser.add_argument('-flatten', '--flatten_lists', 
                        type=str, 
                        help='Flag to indicate if the collections are going to be flatted if they just contain named classes',
                        choices=['yes', 'no'],
                        default='no')
    
    args = parser.parse_args()
    main(args.ontology_path, args.csv_path, args.output_path, args.patterns_type, args.flatten_lists)