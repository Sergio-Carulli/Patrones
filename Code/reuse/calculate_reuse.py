import argparse
import os.path

from identify_reuse import identify_reuse

def main(ontology_path):
    # Create a new file in which to write the logs 
    reuse_log = open("reuse_log.txt" , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    reuse_log.truncate()

    # Is there an error in the path to the folder with the ontologies?    
    if check_ontology_error(ontology_path, reuse_log):
        reuse_log.close()
        exit(-1)
    
    identify_reuse(ontology_path, reuse_log)
    return

# Function to check if the path to the directory where the ontologies are going to be downloaded
# is really a directory.
def check_ontology_error(ontology_path, error_log):

    # Is a directory path?
    if not os.path.isdir(ontology_path):
        error_log.write(f'The path --ontology_path {ontology_path} is not a directory\n')
        print(f'The path --ontology_path {ontology_path} is not a directory\n')
        return True
    
    else:
        return False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Visualize an ontology pattern using Chowlk notation')
    parser.add_argument('-ontology', '--ontology_path', 
                        type=str, 
                        help='Path to a folder where the ontologies are going to be downloaded. The patterns are going to be identified using the ontologies stored in this folder')
    
    args = parser.parse_args()
    main(args.ontology_path)