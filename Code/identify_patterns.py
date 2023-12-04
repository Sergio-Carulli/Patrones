# Dictionary whose:
#   - key : structure detected in a ontology
#   - value: dictionary in which the following elements are stored:
#       - times: Number of times this pattern is repeated in all ontologies
#       - est_name: Array with the name of the detected structures
#       - ont_con: Number of different ontologies in which this pattern appears
#       - ont_name: Dictionary whose:
#           - key: name of the ontology in which the pattern has been found
#           - value: number of times the pattern has been found in that ontology
patterns = {}

def identify_patterns(input_path, output_path):
    global patterns
    patterns = {}
    load_structures(input_path)
    write_pattern(output_path)

# This function iterate the structures in order to identify patterns
def load_structures(input_path):
    # Variable that will store the structure being read
    structure_line = ""
    # Variable that indicates wether the line with the name of the ontology is being read
    ont_line = True
    # Variable that indicates wether the line with the name of the structure is being read
    est_line = True

    # Open the file with the detected structures
    structure = open(input_path , "r", encoding='utf-8')
    # Skip the first line (it is a white line)
    line = structure.readline()
    # Read the second line (already contains data)
    line = structure.readline()

    # Iterate the lines of the txt file
    while(line):

        # Is the ontology name being read?
        if ont_line:
            ont_line = False
            # The ontology prefix is being read as "Ontology: name\n"
            # Get the "name" part of the line
            ont_prefix = line.split(":",1)[1].strip()

        # Is the structure name being read?
        elif est_line:
            est_line = False
            # The ontology prefix is being read as "Structure: name\n"
            # Get the "name" part of the line
            est_name = line.split(":",1)[1].strip()

        # Is a structure line being read?
        elif len(line) > 1:
            # Add structure line
            structure_line += line

        else:
            # In this case a blank line is being read
            # This blank line indicates the end of a structure
            add_pattern(structure_line, est_name, ont_prefix)
            
            # Reset the variables for the next structure
            structure_line = ""
            ont_line = True
            est_line = True

        # Read the next line
        line = structure.readline()

    # Close the csv file
    structure.close()

# This function add a pattern to the dictionary called "patterns"
def add_pattern(structure_line, est_name, ont_prefix):

    # Is the first time that the structure has been identified?
    if structure_line not in patterns: 
        # Create a new pattern
        patterns[structure_line] = {"times": 0,
                        "est_name": [],
                        "ont_name": {},
                        "ont_con": 0}
        
    # Indicate that the pattern has been detected one more time
    patterns[structure_line]["times"] += 1
    # Add the name of the structure
    patterns[structure_line]["est_name"].append(est_name)

    # Is not the first time that the pattern has been detected in the ontology?
    if ont_prefix in patterns[structure_line]["ont_name"]:
        # Indicate that the pattern has been detected one more time in the ontology
        patterns[structure_line]["ont_name"][ont_prefix] += 1
    
    else:
        # Indicate that the pattern has been detected in the ontology
        patterns[structure_line]["ont_name"][ont_prefix] = 1
        # Indicate that the pattern has been detected for the first time in an ontology
        patterns[structure_line]["ont_con"] += 1

def write_pattern(output_path):
    # Create a new file in which to write the patterns
    patterns_file = open(f"{output_path}.txt" , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    patterns_file.truncate()
    # Create a new file in which to write for each pattern:
    #   - Number of times that pattern appears in all the ontologies
    #   - Number of different ontologies in which that pattern appears
    #   - The structures from which the pattern has been identified
    patterns_csv = open(f"{output_path}.csv" , "w", encoding='utf-8')
    # Empty the file (in case the program has been run before)
    patterns_csv.truncate()
    # Naming the columns
    patterns_csv.write("Pattern;Times;Ontologies;Structures\n")

    # Variable which is used to create an unique identifier per pattern
    pattern_id = 1

    # Iterate the patterns
    for pattern in patterns.keys():

        # A structure is considered a pattern if it is repeated at least twice
        if patterns[pattern]['times'] > 1:
            # Write the pattern name
            patterns_file.write(f'Pattern {pattern_id}\n')
            # Write the number of times the pattern appears
            patterns_file.write(f"Times {patterns[pattern]['times']}\n")
            # Write the number of different ontologies on which the pattern appears
            patterns_file.write(f'Different ontologies {patterns[pattern]["ont_con"]}\n')
            # Write how many times a pattern appears in each ontology
            text = ontology_count(patterns[pattern]['ont_name'])
            patterns_file.write(f'Ontologies in which it appears {text}\n')
            # Write the pattern
            patterns_file.write(f"{pattern}\n")

            # Get the name of the structures from which the pattern has been identified
            text = ';'.join(patterns[pattern]["est_name"])
            # Write a new line in the csv
            patterns_csv.write(f'Pattern {pattern_id};{patterns[pattern]["times"]};{patterns[pattern]["ont_con"]};{text}\n')

            pattern_id += 1

    # Close files
    patterns_file.close()
    patterns_csv.close()

# Function to obtain for each ontology the number of times a pattern appears.
# The format is the following: "Ontology (number of times the pattern appears in that ontology)"
def ontology_count(ont_name):
    text = ''

    # Iterate the ontology and the number of time the pattern appears in that ontology
    for ont_prefix, times in ont_name.items():
        text += f'{ont_prefix} ({times}); '
    
    return text