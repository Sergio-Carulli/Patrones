

# This function receive as parameter a mutable object (a list).
# All modifications to a mutable object are applied directly to the object (instead of creating a new object).
# Therefore, changes made to the list in this class are also applied in the other class.
# A structure is written as a tree in its corresponding file, where the number of '  |' is the deep of a tree node.
# This structure has been parsed as a list where each line is stored as a different item.
# This function infers the types of terms that have been detected as "#Unknown" within a structure.
def infer_structure_type(structure):
    # Get the number of items in the list
    structure_len = len(structure)
    # This variable store the position of the list (skip the first three lines)
    i = 3

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Does the line represents the beginning of a restriction?
        if 'owl:Restriction' in line:
            # Get the line where the restriction ends
            i = restriction(i + 1, structure, structure_len, deep)
        
        # Does the line reprsents the beginning of an intersection of union of classes?
        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
            # Get the line where the intersection/union ends
            i = intersection_union(i + 1, structure, structure_len, deep)

        # Does the line represents the beginning of a complement class?
        elif 'owl:complementOf' in line:
            i += 1
            complement(i, structure)
        
        # Does the line represents the beginning of an enumeration?
        elif 'owl:oneOf' in line:
            # Get the line where the enumeration ends
            i = one_of(i + 1, structure, structure_len, deep)

        else:
            # Get the next line
            i += 1

# This function iterate the elements involved in the intersection/union in order to infer the types of the "#Unknown" elements.
# We know that an element belongs to the intersection/union if its deeper than the line which contains 'owl:intersectionOf' or 'owl:unionOf'.
# In addition, if a new anonymous class is detected, a new inference process is started in its corresponding function.
# RDFlib parse these blank nodes as collections. The elements involved in an intersection or union must be classes.
# Blank nodes are always recognized by RDFlib. Therefhore, the type of the terms inside an intersection 
# or union or classes must be named classes (owl:Class).
def intersection_union(i, structure, structure_len, res_deep):

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the intersection or union of classes?
        if deep <= res_deep:
            # Return the line where the intersection/union ends
            return i
        
        # Does the line represents an element of the intersection or union of classes?
        elif 'rdf:first' in line:
            # Get the position of the next line
            i += 1
            # Infer the "Unknown" types
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            # Does the line represents the beginning of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i, structure)

            # Does the line represents the beginning of an enumeration?
            elif 'owl:oneOf' in line:
                # Get the line where the enumeration ends
                i = one_of(i + 1, structure, structure_len, deep)
            
            else:
                # Get the position of the next line
                i += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return i

# This function iterate the elements involved in the enumeration in order to infer the types of the "#Unknown" elements.
# We know that an element belongs to the enumeration if its deeper than the line which contains 'owl:intersectionOf' or 'owl:unionOf'.
# In addition, if a new anonymous class is detected, a new inference process is started in its corresponding function.
# RDFlib parse the enumerations as collections.
# As the element from which we start is a class, the "owl:oneOf" represents an enumeration of individuals.
# Therefhore, the type of the terms inside the enumeration must be named individuals (owl:NamedIndividual).
def one_of(i, structure, structure_len, res_deep):

    # Iterate the structure
    while i < structure_len:
        # Read a line of the structure
        line = structure[i]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the enumeration?
        if deep <= res_deep:
            # Return the line where the enumeration ends
            return i
        
        # Does the line represents an element of the enumeration?
        elif 'rdf:first' in line:
            # Get the position of the next line
            i += 1
            # Infer the "Unknown" types
            structure[i] = structure[i].replace('#Unknown', 'owl:Class')

        else:

            # Does the line represents the beginning of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i, structure)

            # Does the line represents the beginning of an enumeration?
            elif 'owl:oneOf' in line:
                # Get the line where the enumeration ends
                i = one_of(i + 1, structure, structure_len, deep)
            
            else:
                # Get the position of the next line
                i += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return i

# This function just access the first element involved in the complement in order to infer its type.
# The element involved in a complement must be a class. Blank nodes are always recognized by RDFlib. 
# Therefhore, the type of the term inside a complement must be named classes (owl:Class).
def complement(i, structure):
    # Infer the "Unknown" types
    structure[i] = structure[i].replace('#Unknown', 'owl:Class')

# This function iterate the restriction elements in order to infer the types of the "#Unknown" elements.
# We know that an element belongs to the restriction if its deeper than the line which contains 'owl:Restriction'.
# In addition, if a new anonymous class is detected, a new inference process is started in its corresponding function.
# In the restrictions there are two key elements:
#   - One refers to a property.
#   - The other refers to the target of the restriction.
# If one of the type of the key elements is not "#Unknown", the other type can be infer.
def restriction(i, structure, structure_len, res_deep):
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
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the restriction?
        if deep <= res_deep:
            # Infer the "Unknown" types
            change_restriction_type(structure, property, p_position, target, t_position)
            # Return the position where the restriction ends
            return i

        # Does the line represents an element of the restriction?
        if deep == res_deep + 1:
            # We are reading an element of the restriction (e.g. someValuesFrom, onProperty etc)

            # Does the line represents the property?
            if 'owl:onProperty' in line:
                # In the next line the property type is defined (e.g. owl:ObjectProperty, #Unknown, etc)
                # Get the position of the next line
                i += 1
                # Get the property type
                property = structure[i]
                # Get the position of the line where the property type is defined
                p_position = i
            
            # Does the line represents the target?
            elif 'owl:someValuesFrom' in line or 'owl:allValuesFrom' in line or 'owl:onClass' in line or 'owl:onDataRange' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                i += 1
                # Get the target type
                target = structure[i]
                # Get the position of the line where the target type is defined
                t_position = i
            
            # Does the line represents the target?
            elif 'owl:hasValue' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                i += 1
                # Get the target type
                target = structure[i]

                # Is the target type an owl:NamedIndividual?
                if 'rdfs:Datatype' not in target and 'Data value' not in target and 'owl:Class' not in target and 'rdfs:Class' not in target:
                    # In this case an individual is being readed (but its type is an specific class)
                    structure[i] = f'{"  |" * (deep + 1)}owl:NamedIndividual\n'
                    # Get the target type
                    target = 'owl:NamedIndividual'

                # Get the position of the line where the target type is defined
                t_position = i
                
            else:
                # Get the position of the next line
                i += 1
        
        else:

            # Does the line represents the beginning of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                i = restriction(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of an intersection of union of classes?
            elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                # Get the line where the intersection/union ends
                i = intersection_union(i + 1, structure, structure_len, deep)
            
            # Does the line represents the beginning of a complement class?
            elif 'owl:complementOf' in line:
                # Get the next line of the complement. This is a special case because if there is an #Unknown
                # is because there is not a blank node. 
                i += 1
                complement(i, structure)
            
            # Does the line represents the beginning of an enumeration?
            elif 'owl:oneOf' in line:
                i = one_of(i + 1, structure, structure_len, deep)
            
            else:
                # Get the position of the next line
                i += 1

    # In this case we have reached the end of the structure
    # Infer the "Unknown" types
    change_restriction_type(structure, property, p_position, target, t_position)
    # Return a number which is greater than the number of lines in the list
    return i

# Function to infer the "#Unknown" types of the property and target involved in a restriction.
def change_restriction_type(structure, property, p_position, target, t_position):

    # Is the type of the property involved in a restriction #Unknown?
    if '#Unknown' in property:

        # Should the type of the property be an object property?
        if 'owl:Class' in target or 'rdfs:Class' in target or 'owl:Restriction' in target or 'owl:NamedIndividual' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:ObjectProperty')
        
        # Should the type of the property be a datatype property?
        elif 'rdfs:Datatype' in target or 'Data value' in target:
            structure[p_position] = structure[p_position].replace('#Unknown', 'owl:DatatypeProperty')
    
    # Is the type of the target involved in a restriction #Unknown?
    elif '#Unknown' in target:

        # Should the type of the target be a named class?
        if 'owl:ObjectProperty' in property:
            structure[t_position] = structure[t_position].replace('#Unknown', 'owl:Class')
        
        # Should the type of the target be a datatype?
        elif 'owl:DatatypeProperty' in property:
            structure[t_position] = structure[t_position].replace('#Unknown', 'rdfs:Datatype')