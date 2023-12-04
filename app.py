import argparse
import sys
import os.path
from Code.download_ontology import download_ontologies
from Code.create_structure import create_structure
from Code.identify_patterns import identify_patterns

def main(csv_path, ontology_path, app_directory):
    # Create a new file in which to write the logs 
    error_log = open("error_log.txt" , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    error_log.truncate()
    # Get the path to the application directory
    app_directory = os.path.dirname(app_directory)

    # Is there an error in the csv file?
    if(check_csv_error(csv_path, error_log) and check_ontology_error(ontology_path, error_log)):
        #download_ontologies(csv_path, ontology_path, error_log)
        create_structure(ontology_path, error_log)
        identify_patterns('Structure_term_type.txt', 'Patterns_type')
        identify_patterns('Structure_term_name.txt', 'Patterns_name')

    error_log.close()

# Function to check if the path to the csv is really a csv file.
def check_csv_error(csv_path, error_log):

    # Is a file path?
    if not os.path.isfile(csv_path):
        error_log.write(f'The path {csv_path} is not a file\n')
        print(f'The path {csv_path} is not a file\n')
    
    # Is a csv path?
    elif not csv_path.endswith('.csv'):
        error_log.write(f'The path {csv_path} is not a csv\n')
        print(f'The path {csv_path} is not a csv\n')
    
    else:
        return True
    
    return False

# Function to check if the path to the directory where the ontologies are going to be downloaded
# is really a directory.
def check_ontology_error(ontology_path, error_log):

    # Is a directory path?
    if not os.path.isdir(ontology_path):
        error_log.write(f'The path {ontology_path} is not a directory\n')
        print(f'The path {ontology_path} is not a directory\n')
    
    else:
        return True
    
    return False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Identify patterns from a set of ontologies")
    parser.add_argument("csv_path", type=str, help="the path where the csv is located")
    parser.add_argument("ontology_path", type=str, help="the desired location where the ontologies are going to be downloaded")
    args = parser.parse_args()
    main(args.csv_path, args.ontology_path, sys.argv[0])