import argparse
import sys
import os.path
from Code.download_ontology import download_ontologies
from Code.create_structure import create_structure
from Code.identify_patterns import identify_patterns
from Code.infer_types import infer_types

def main(ontology_path, csv_path, patterns_type, app_directory):
    # Create a new file in which to write the logs 
    error_log = open("error_log.txt" , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    error_log.truncate()
    # Get the path to the application directory
    app_directory = os.path.dirname(app_directory)

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

    create_structure(ontology_path, error_log)
    infer_types()

    # Has the user specified that the patterns are going to be created from the type of the terms?
    if patterns_type == 'type':
        identify_patterns('Structure_term_type.txt', 'Patterns_type')
    
    # Has the user specified that the patterns are going to be created from the name of the terms?
    elif patterns_type == 'name':
        identify_patterns('Structure_term_name.txt', 'Patterns_name')
    
    else:
        identify_patterns('Structure_term_type.txt', 'Patterns_type')
        identify_patterns('Structure_term_name.txt', 'Patterns_name')

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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Identify patterns from a set of ontologies')
    parser.add_argument('-ontology', '--ontology_path', 
                        type=str, 
                        help='Path to a folder where the ontologies are going to be downloaded. The patterns are going to be identified using the ontologies stored in this folder')
    parser.add_argument('-csv', '--csv_path', 
                        type=str, 
                        help='Path to the csv file indicating what ontologies are going to be downloaded',
                        default='')
    parser.add_argument('-patterns', '--patterns_type', 
                        type=str, 
                        help='Flag to indicate if the patterns are going to be created from the type of the terms or from the name of the terms or from both',
                        choices=['type', 'name', 'both'],
                        default='type')
    
    args = parser.parse_args()
    main(args.ontology_path, args.csv_path, args.patterns_type, sys.argv[0])