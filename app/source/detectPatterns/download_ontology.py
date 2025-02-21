import requests
import os.path

# Dictionary whose:
#   key: It is the ontology prefix, which will be the name of the local files created after downloading each ontology
#   value: It is the ontology URI (This value will never change)
ontologies = {}

# Function to parse the content of the CSV into a dictionary
# The CSV file has as many rows as ontologies to download
# The CSV file it is composed by just two columns:
#   - The first column represents the prefix of each ontology
#   - The second column represents the URI of each ontology
# The first row of the CSV file is the header of the columns (i.e prefix;URI)
def load_otologies_dictionary(csv_path, error_log):
    # Open the CSV file containing the prefixes and the URIs of the ontologies to be downloaded
    ontology_csv = open(csv_path, "r", encoding='utf-8')
    # Skip the first row (it just represents the name of the columns)
    ontology_csv.readline()
    # Read the second line (it already contains data)
    line = ontology_csv.readline()
    # Variable to indicate the number of the row
    row = 1

    # Iterate the lines of the CSV file
    while(line):

        try:
            # Split the row into columns
            columns = line.split(";")
            # Create an entry in the dictionary for that ontology
            ontologies[columns[0]] = columns[1].strip()
            # Read the next line
            line = ontology_csv.readline()
        
        except:
            error_log.write(f'Error reading the row {row} of the CSV file.\n\tThe content of that row is the following: {line}.\n\tIn the first column the ontolgy prefix must be specified, while in the second column the ontology URI must be specified.\n\tIn other words, the row must have the following format: prefix;URI\n')

        # Increase the row number
        row += 1

    # Close the CSV file
    ontology_csv.close()

# Function to download the ontologies to the directory specified by the user
# For each ontology, its code is downloaded via an HTTP GET request and stored in the directory 
# specified by the user with a name representing the ontology prefix.
def download_ontology(ontology_path, error_log):

    # For each ontology prefix and ontology URI
    for ont_prefix, ont_uri in ontologies.items():

        try:
            # HTTP GET request to get the ontology code
            req = requests.get(ont_uri, timeout=5, headers={'Accept': 'application/rdf+xml; charset=utf-8'})
            # Get the request status
            req_status = req.status_code

        except:
            # The HTTP GET request failed
            req_status = 504

        # Has the HTTP GET request been accepted?
        if req_status == 200 :
            # Path to where the ontology is going to be stored locally
            name = os.path.join(ontology_path, f'{ont_prefix}.rdf')
            # Store the ontology code locally
            with open(name, mode = 'w', encoding = req.apparent_encoding) as f:
                f.write(req.text)

        else:
            error_log.write(f'Error downloading the ontology whose prefix is {ont_uri}. The HTTP GET request failed with status code {req_status}\n')

# Function to download the ontologies specified in the CSV file to the directory specified by the user
def download_ontologies(csv_path, ontology_path, error_log):
    # Parse the content of the CSV file into a dictionary
    load_otologies_dictionary(csv_path, error_log)
    # Download the ontologies to the directory specidied by the user
    download_ontology(ontology_path, error_log)