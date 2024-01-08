from Code.infer_blank_nodes import iterate_structure_blank_nodes
from Code.infer_types import infer_structure_type

# This function will read the files where the structures are written. 
# One file contains the term names and the other contains the term types.
# Both files are generated by this program and have the same number of lines.
# Moreover, each structure is generated by this program and have the same number of lines in both files.
# These structures are loaded into lists. Once a structure has been read, the inference process begins.
def infer_structures():
    # Lists to store each line of a structure. Each position of the list contains a line
    structure_name = []
    structure_type = []

    # Create a new file in which to write the inferred type of the structures found 
    inferred_type = open("Structure_term_inferred_type.txt", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    inferred_type.truncate()
    inferred_type.write('\n')

    # Create a new file in which to write the inferred blank nodes of the structures found 
    inferred_blank_nodes = open("Structure_term_inferred_blank_nodes.txt", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    inferred_blank_nodes.truncate()
    inferred_blank_nodes.write('\n')

    # Open the file with the detected structures
    term_type = open('Structure_term_type.txt' , "r", encoding='utf-8')
    # Skip the first line (it is a white line)
    term_type.readline()
    # Read the second line (already contains data)
    line_type = term_type.readline()

    # Open the file with the detected structures
    term_name = open('Structure_term_name.txt' , "r", encoding='utf-8')
    # Skip the first line (it is a white line)
    term_name.readline()
    # Read the second line (already contains data)
    line_name = term_name.readline()

    # Iterate the lines of the files where the structures are defined
    while(line_type and line_name):

        # Is a structure line being read?
        if len(line_name) > 1:
            # Add structure line
            structure_name.append(line_name)
            structure_type.append(line_type)

        else:
            # In this case a blank line is being read
            # This blank line indicates the end of a structure

            # Infer the type of the term which is on top of the structure
            infer_term_top(structure_name, structure_type)
            
            # Infer the "Blank node" types
            iterate_structure_blank_nodes(structure_name, structure_type)
            # Write results
            inferred_blank_nodes.writelines(structure_name)
            inferred_blank_nodes.write('\n')

            # Infer the "#Unknown" types
            infer_structure_type(structure_type)
            # Write results
            inferred_type.writelines(structure_type)
            inferred_type.write('\n')

            # Reset the variables for the next structure
            structure_name = []
            structure_type = []
        
        # Read the next line
        line_type = term_type.readline()
        line_name = term_name.readline()

    # Close files
    term_type.close()
    inferred_type.close()
    term_name.close()
    inferred_blank_nodes.close()

# Function to infer the type of the term which is on top of the structure.
# It is necessary to infer the type of this term before performing any other step because 
# this app goes through the structure from top to bottom applying inference from the type 
# of the terms higher up in the structure.
def infer_term_top(structure_name, structure_type):
    # Get the line which represents the term which is on top of the structure
    term_top_type = structure_type[2]

    # Is the type of the top term "#Unknown"?
    if '#Unknown' in term_top_type:
        # In this case the type of the term after the class axiom is going to be checked.
        # Remember that this term is representing a blank node
        line = structure_name[4]

        # Does the term after the class axiom represent a datatype?
        if 'rdfs:Datatype' in line:
            # Infers that the "#Unknown" type is an "rdfs:Datatype"
            structure_type[2] = structure_type[2].replace('#Unknown', 'rdfs:Datatype')
        
        # Does the term after the class axiom represent a class?
        elif 'owl:Class' in line or 'owl:Restriction' in line:
            # Infers that the "#Unknown" type is an "owl:Class"
            structure_type[2] = structure_type[2].replace('#Unknown', 'owl:Class')
        
        else:
            # In this case the term after a class axiom represent a term whose type is "Blank node"
            # Infers that the "#Unknown" type is an "owl:Class"
            structure_type[2] = structure_type[2].replace('#Unknown', 'owl:Class')