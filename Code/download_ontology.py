import requests
import os.path

# Dictionary whose:
#   key: ontology prefix (it is going to be the named of the local files)
#   value: ontology URI (unchanged)
ontologies = {}

# Function to parse the csv into a dictionary.
def load_otologies_dictionary(csv_path, error_log):
    # Open the csv file where the prefix and the uri of the ontologies 
    # which are going to be downloaded are stored.
    ontology_csv = open(csv_path, "r", encoding='utf-8')
    # Skip the first line (it just represents the name of the columns)
    ontology_csv.readline()
    # Read the second line (already contains data)
    line = ontology_csv.readline()

    # Iterate the lines of the csv
    while(line):

        try:
            # Split the line into columns
            columns = line.split(";")
            # Create dictionary entries for that ontology
            ontologies[columns[0]] = columns[1].strip()
            # Read the next line
            line = ontology_csv.readline()
        
        except:
            error_log.write(f'Error reading the line {line} of the csv. The line must has the following format: prefix;URI\n')

    # Close the csv file.
    ontology_csv.close()

# Function to download the ontologies into the "ontology_path" directory.
def download_ontology(ontology_path, error_log):

    # Iterate ontology prefix and ontology URI
    for ont_prefix, ont_uri in ontologies.items():

        try:
            # Request get to the ontology code
            req = requests.get(ont_uri, timeout=5, headers={'Accept': 'application/rdf+xml; charset=utf-8'})
            # Adquirir el estado de la petición get
            req_status = req.status_code

        except:
            req_status = 504

        # Has the get request been accepted?
        if req_status == 200 :

            # Store ontology code locally
            name = os.path.join(ontology_path, f'{ont_prefix}.rdf')
            name= f"{ontology_path}/{ont_prefix}.rdf"
            with open(name, mode = 'w', encoding = req.apparent_encoding) as f:
                f.write(req.text)

        else:
            error_log.write(f'Error downloading the ontology {ont_uri}. The request status is {req_status}\n')

def download_ontologies(csv_path, ontology_path, error_log):
    load_otologies_dictionary(csv_path, error_log)
    download_ontology(ontology_path, error_log)