structure = []

def infer_types():
    # Variable to store each line of a structure
    global structure

    # Create a new file in which to write the inferred type of the structures found 
    inferred_type = open("Structure_term_inferred_type.txt", 'w', encoding='utf-8')
    # Empty the file (in case the program has been run before)
    inferred_type.truncate()
    inferred_type.write('\n')

    # Open the file with the detected structures
    term_type = open('Structure_term_type.txt' , "r", encoding='utf-8')
    # Skip the first line (it is a white line)
    term_type.readline()
    # Read the second line (already contains data)
    line = term_type.readline()

    # Iterate the lines of the txt file
    while(line):

        # Is a structure line being read?
        if len(line) > 1:
            # Add structure line
            structure.append(line)

        else:
            # In this case a blank line is being read
            # This blank line indicates the end of a structure
            infer_structure_type()
            inferred_type.writelines(structure)
            inferred_type.write('\n')

            # Reset the variables for the next structure
            structure = []
        
        # Read the next line
        line = term_type.readline()

    # Close files
    term_type.close()
    inferred_type.close()

def infer_structure_type():
    structure_len = len(structure)
    i = 0

    # Iterate the array (which contains the structure)
    while i < structure_len:
        line = structure[i]
        deep = count_vertical_bar(line)

        if 'owl:Restriction' in line:
            i = restriction(i + 1, structure_len, deep)
        
        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
            i = intersection_union(i + 1, structure_len, deep)
        
        elif 'owl:complementOf' in line:
            i += 1
            complement(i)
        
        elif 'owl:oneOf' in line:
            i = one_of(i + 1, structure_len, deep)

        else:
            i += 1

def intersection_union(i, structure_len, res_deep):

    while i < structure_len:
        line = structure[i]
        deep = count_vertical_bar(line)

        if deep <= res_deep:
            # We are out the intersection/union of class descriptions
            return i
        
        elif 'rdf:first' in line:
            i += 1
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            if 'owl:Restriction' in line:
                i = restriction(i + 1, structure_len, deep)
            
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                i = intersection_union(i + 1, structure_len, deep)
            
            elif 'owl:complementOf' in line:
                i += 1
                complement(i)

            elif 'owl:oneOf' in line:
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1
    
    return i

def one_of(i, structure_len, res_deep):

    while i < structure_len:
        line = structure[i]
        deep = count_vertical_bar(line)

        if deep <= res_deep:
            # We are out the enumeration of classes
            return i
        
        elif 'rdf:first' in line:
            i += 1
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            if 'owl:Restriction' in line:
                i = restriction(i + 1, structure_len, deep)
            
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                i = intersection_union(i + 1, structure_len, deep)
            
            elif 'owl:complementOf' in line:
                i += 1
                complement(i)

            elif 'owl:oneOf' in line:
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1
    
    return i

def complement(i):
    structure[i] = structure[i].replace('#Unknown', 'owl:Class')

def restriction(i, structure_len, res_deep):
    property = ''
    p_position = 0
    target = ''
    t_position = 0

    while i < structure_len:
        line = structure[i]
        deep = count_vertical_bar(line)

        if deep <= res_deep:
            change_restriction_type(property, p_position, target, t_position)
            return i

        if deep == res_deep + 1:
            # We are reading an element of the restriction
            # (e.g. someValuesFrom, onProperty etc)

            if 'owl:onProperty' in line:
                # We know that in the next line the type of the property is defined
                # (owl:ObjectProperty, owl:DatatypeProperty or #Unknown)
                property = structure[i + 1]
                p_position = i + 1
                i += 1
            
            elif 'owl:someValuesFrom' in line or 'owl:allValuesFrom' in line or 'owl:onClass' in line or 'owl:onDataRange' in line:
                # We know that in the next line the type of the target is defined
                # (owl:Class, rdfs:Class, datatype or #Unknown)
                target = structure[i + 1]
                t_position = i + 1
                i += 1
            
            elif 'owl:hasValue' in line:
                # We know that in the next line the type of the target is defined
                # (owl:Class, rdfs:Class, datatype or #Unknown)
                target = structure[i + 1]

                if 'Datatype' not in target and 'Literal' not in target and 'owl:Class' not in target and 'rdfs:Class' not in target:
                    structure[i + 1] = f'{"  |" * (deep + 1)}owl:Class\n'
                    target = 'owl:Class'

                t_position = i + 1
                i += 1
            
            else:
                i += 1
        
        else:

            if 'owl:Restriction' in line:
                i = restriction(i + 1, structure_len, deep)
            
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                i = intersection_union(i + 1, structure_len, deep)
            
            elif 'owl:complementOf' in line:
                i += 1
                complement(i)
            
            elif 'owl:oneOf' in line:
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1

    change_restriction_type(property, p_position, target, t_position)
    return i

def change_restriction_type(property, p_position, target, t_position):

    if '#Unknown' in property:

        if 'owl:Class' in target or 'rdfs:Class' in target or 'owl:Restriction' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:ObjectProperty')
        
        elif 'Datatype' in target or 'Literal' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:DatatypeProperty')
        
    elif '#Unknown' in target:

        if 'owl:ObjectProperty' in property:
            structure[t_position] = structure[t_position].replace('#Unknown', 'owl:Class')
        
        elif 'owl:DatatypeProperty' in property:
            structure[t_position] = structure[t_position].replace('#Unknown', 'Datatype')

# Function to count the number of times '|' appears in a line.
# This number refers to the tree deep.
def count_vertical_bar(line):
    count = 0

    # Iterate each character of the string. There are three cases:
    #   - the char is ' '. This means there is a '|' ahead.
    #   - the char is '|'.
    #   - the char is another thing. This means the tree deep has been reached
    for char in line:

        if char == ' ':
            continue

        elif char == '|':
            count += 1

        else:
            break
    
    return count