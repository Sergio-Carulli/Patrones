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

# This function infers the #Unknown types inside a structure.
# A structure is written as a tree, where the number of '  |' is the deep of a tree node.
def infer_structure_type():
    structure_len = len(structure)
    i = 0

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the structure (the number of "  |")
        deep = count_vertical_bar(line)

        # Does the line represents the beggining of a restriction?
        if 'owl:Restriction' in line:
            # Get the line where the restriction ends
            i = restriction(i + 1, structure_len, deep)
        
        # Does the line reprsents the beggining of an intersection of union of classes?
        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
            # Get the line where the intersection/union ends
            i = intersection_union(i + 1, structure_len, deep)

        # Does the line represents the beggining of a complement class?
        elif 'owl:complementOf' in line:
            i += 1
            complement(i)
        
        # Does the line represents the beggining of an enumeration?
        elif 'owl:oneOf' in line:
            i = one_of(i + 1, structure_len, deep)

        else:
            i += 1

# Function to infer the #Unknown types inside an intersection or union of classes.
# RDFlib parse these blank nodes as collections. The elements involved in an intersection or union must be classes.
# Blank nodes are always recognized by RDFlib. Therefhore, the type of the terms inside an intersection 
# or union or classes must be named classes (owl:Class).
def intersection_union(i, structure_len, res_deep):

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the structure (the number of "  |")
        deep = count_vertical_bar(line)

        # Is the line outside the intersection or union of classes?
        if deep <= res_deep:
            # Return the line where the intersection/union ends
            return i
        
        # Does the line represents an element of the intersection or union of classes?
        elif 'rdf:first' in line:
            i += 1
            # Infer the type
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            # Does the line represents the beggining of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i)

            # Does the line represents the beggining of an enumeration?
            elif 'owl:oneOf' in line:
                # Get the line where the enumeration ends
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1
    
    # In this case we have reached the end of the structure
    return i

# Function to infer the #Unknown types inside an enumeration.
# RDFlib parse the enumerations as collections
# As the element from which we start is a class, the oneOf represents an enumeration of individuals.
# Therefhore, the type of the term inside a oneOf must be named individuals (owl:NamedIndividual).
def one_of(i, structure_len, res_deep):

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the structure (the number of "  |")
        deep = count_vertical_bar(line)

        # Is the line outside the enumeration?
        if deep <= res_deep:
            # Return the line where the enumeration ends
            return i
        
        # Does the line represents an element of the enumeration?
        elif 'rdf:first' in line:
            i += 1
            # Infer the type
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            # Does the line represents the beggining of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i)

            # Does the line represents the beggining of an enumeration?
            elif 'owl:oneOf' in line:
                # Get the line where the enumeration ends
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1
    
    # In this case we have reached the end of the structure
    return i

# Function to infer the #Unknown types inside a complement class.
# The element involved in a complement must be a class. Blank nodes are always recognized by RDFlib. 
# Therefhore, the type of the term inside a complement must be named classes (owl:Class).
def complement(i):
    # Infer the type
    structure[i] = structure[i].replace('#Unknown', 'owl:Class')

# Function to infer the #Unknown types inside a restriction.
# In the restrictions there are two key elements:
#   - One refers to a property.
#   - The other refers to the target of the restriction.
# If one of the type of the key elements is not #Unknown, the other type can be infer.
def restriction(i, structure_len, res_deep):
    # Variable to store the type of a property involved in a resctriction
    property = ''
    # Variable to store in which line is the property
    p_position = 0
    # Variable to store the type of the target involved in a resctriction
    target = ''
    # Variable to store in which line is the target
    t_position = 0

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the structure (the number of "  |")
        deep = count_vertical_bar(line)

        # Is the line outside the restriction?
        if deep <= res_deep:
            # Infer the type
            change_restriction_type(property, p_position, target, t_position)
            return i

        # Does the line represents an element of the restriction?
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

                if 'Datatype' not in target and 'Data value' not in target and 'owl:Class' not in target and 'rdfs:Class' not in target:
                    # In this case an individual is being readed (but its type is an specific class)
                    structure[i + 1] = f'{"  |" * (deep + 1)}owl:NamedIndividual\n'
                    target = 'owl:NamedIndividual'

                t_position = i + 1
                i += 1
            
            else:
                i += 1
        
        else:

            # Does the line represents the beggining of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure_len, deep)
            
            # Does the line represents the beggining of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i)
            
            # Does the line represents the beggining of an enumeration?
            elif 'owl:oneOf' in line:
                i = one_of(i + 1, structure_len, deep)
            
            else:
                i += 1

    # Infer the type
    change_restriction_type(property, p_position, target, t_position)
    # In this case we have reached the end of the structure
    return i

# Function to infer the types of the property and target involved in a restriction
def change_restriction_type(property, p_position, target, t_position):

    # Is the type of the property involved in a restriction #Unknown?
    if '#Unknown' in property:

        # Should the type of the property be an object property?
        if 'owl:Class' in target or 'rdfs:Class' in target or 'owl:Restriction' in target or 'owl:NamedIndividual' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:ObjectProperty')
        
        # Should the type of the property be a datatype property?
        elif 'Datatype' in target or 'Data value' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:DatatypeProperty')
    
    # Is the type of the target involved in a restriction #Unknown?
    elif '#Unknown' in target:

        # Should the type of the target be a named class?
        if 'owl:ObjectProperty' in property:
            structure[t_position] = structure[t_position].replace('#Unknown', 'owl:Class')
        
        # Should the type of the target be a datatype?
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