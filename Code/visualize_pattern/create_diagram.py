from create_diagram_element import *

# Global variable to store the content of the XML file
diagram = ''

# Function to create the XML diagram where the patterns are going to be visualizated
def create_diagram(pattern_path):
        generate_XML_headers()

        # Open the file with the detected patterns
        pattern_file = open(pattern_path , "r", encoding='utf-8')

        # Read the first pattern
        pattern, max_lenght, pattern_text, pattern_number = read_pattern(pattern_file)

        # Variable to store the starting Y axis of a new pattern. In order to not overlap the figures
        y_axis = 0

        # Iterate while there is at least one pattern unread
        while(len(pattern) > 0):
            y_axis = visualize_pattern(pattern, y_axis, max_lenght, pattern_text, pattern_number)
            # Read a new pattern
            pattern, max_lenght, pattern_text, pattern_number = read_pattern(pattern_file)

        # Close the csv file
        pattern_file.close()

        generate_footers()

        f = open('Visualization.xml', 'w', encoding='utf-8')
        f.write(diagram)
        f.close()

# Function to parse just one pattern into a list
# Different patterns are separated by blank lines        
def read_pattern(pattern_file):
    # List that will store each line of the pattern being read
    pattern = []

    # Skip the first four lines of the pattern (these lines just contain metadata)
    
    pattern_number = pattern_file.readline()
    pattern_file.readline()
    pattern_file.readline()
    pattern_file.readline()

    # Variable to store the length of the longest line
    max_lenght = 0

    # Read fifth line (already contains pattern data)
    line = pattern_file.readline()

    # Variable to store the pattern as text
    pattern_text = ''

    # Iterate the lines of the TXT file
    while(line):

        # Is a pattern line being read?
        if len(line) > 1:
            # Store the length of the longest line
            max_lenght = max(max_lenght, len(line))
            # Add structure line
            pattern.append(line)
            pattern_text += f'{line}&lt;br&gt;&amp;nbsp;'

        else:
            pattern_text = pattern_text[:-20]
            # In this case a blank line is being read, i.e. the end of the pattern has been reached
            break

        # Read a new line
        line = pattern_file.readline()
    
    return pattern, max_lenght, pattern_text, pattern_number

def visualize_pattern(pattern, y_axis, max_lenght, pattern_text, pattern_number):
    global diagram
    x_axis, y_axis_document = visualize_document(pattern_text, max_lenght, len(pattern), y_axis, pattern_number)

    try:
        x_axis, figure_id = visualize_beggining(pattern, x_axis, y_axis)
    
    except:
        diagram += create_cloud("No chowlk&lt;br&gt;notation", x_axis, y_axis)
        return max(y_axis, y_axis_document) + 60
    
    index = 2
    pattern_len = len(pattern)
    # Iterate the structure
    while index < pattern_len:
        # Read a line of the pattern
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Does the line represents the beggining of a restriction?
        if 'owl:Restriction' in line:
            # Get the line where the restriction ends
            index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        elif 'owl:oneOf' in line:
            # Get the line where the enumeration ends
            index, y_axis = iterate_enumeration(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
            # Get the line where the intersection ends
            index, y_axis = iterate_intersection(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        elif 'owl:complementOf' in line:
            # Get the line where the intersection ends
            index, y_axis = iterate_complement(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        else:
            # Get the next line
            index += 1

    return max(y_axis, y_axis_document) + 60

def iterate_complement(index, pattern, pattern_len, father_deep, figure_id, x_axis, y_axis):
    global diagram
    # Variable to store the type of the target involved in a resctriction
    target = ''
    # Variable to store the identifier of the figure which represents the target of a resctriction.
    # This variable is filled if the target of a restriction is another blank node.
    target_id = ''
    # Iterate the structure
    while index < pattern_len:
        # Read a line of the structure
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Is the line outside the restriction?
        if deep <= father_deep:
            # Return the position where the restriction ends
            return index, y_axis

        if 'owl:Restriction' in line:
            # Create the figure to represent the beggining of a new restriction
            figure, target_id, figure_width = create_empty_box(x_axis + 200, y_axis)
            arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
            diagram += f'{figure}{arrow}'
            # Get the line where the restriction ends
            index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
        
        else:
            target = line

            if index + 1 < pattern_len:
                line = pattern[index + 1]
                deep = get_deep(line)

                if deep > father_deep:

                    if 'owl:oneOf' in line:
                        # Create the figure to represent the beggining of a new enumeration
                        figure, target_id, figure_width = create_hexagon('&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis + 200, y_axis)
                        # Create the arrow linking the figure to the intersection
                        arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    elif 'owl:intersectionOf' in line:
                        # Create the figure to represent the beggining of a new enumeration
                        figure, target_id, figure_width = create_ellipse('⨅', x_axis + 200, y_axis)
                        # Create the arrow linking the figure to the intersection
                        arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    elif 'owl:unionOf' in line:
                        # Create the figure to represent the beggining of a new enumeration
                        figure, target_id, figure_width = create_ellipse('⨆', x_axis + 200, y_axis)
                        # Create the arrow linking the figure to the intersection
                        arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    elif 'owl:complementOf' in line:
                        # Create the figure to represent the beggining of a new enumeration
                        figure, target_id, figure_width = create_empty_box(x_axis + 200, y_axis)
                        # Create the arrow linking the figure to the intersection
                        arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

            # Create the figure representing a member of the intersection
            figure, target_id, figure_width = create_box(clean_term(target.strip()), x_axis + 200, y_axis)
            # Create the arrow linking the figure to the intersection
            arrow = create_dashed_arrow('&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', figure_id, target_id)
            diagram += f'{figure}{arrow}'
            index += 1
    
    # Return a number which is greater than the number of lines in the list
    return index, y_axis

def iterate_intersection(index, pattern, pattern_len, father_deep, figure_id, x_axis, y_axis):
    global diagram

    # Iterate the structure
    while index < pattern_len:
        # Read a line of the structure
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Is the line outside the intersection or union of classes?
        if deep <= father_deep:
            # Return the line where the intersection/union ends
            return index, y_axis - 60
        
        # Does the line represents an element of the intersection or union of classes?
        elif 'rdf:first' in line:
            # Get the position of the next line
            index += 1
            line = pattern[index]
            deep = get_deep(line)

            if 'owl:Restriction' in line:
                # Create the figure to represent the beggining of a new restriction
                figure, target_id, figure_width = create_empty_box(x_axis + 60, y_axis)
                # Create the arrow linking the figure to the intersection
                arrow = create_empty_dashed_arrow(figure_id, target_id)
                diagram += f'{figure}{arrow}'
                # Get the line where the restriction ends
                index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, target_id, x_axis + 60 + figure_width, y_axis)
                y_axis += 60
            
            else:

                if index + 1 < pattern_len:
                    line = pattern[index + 1]
                    deep = get_deep(line)

                    if deep > father_deep:

                        if 'owl:oneOf' in line:
                            # Create the figure to represent the beggining of a new enumeration
                            figure, target_id, figure_width = create_hexagon('&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis + 60, y_axis)
                            # Create the arrow linking the figure to the intersection
                            arrow = create_empty_dashed_arrow(figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            y_axis += 60
                            continue

                        elif 'owl:intersectionOf' in line:
                            # Create the figure to represent the beggining of a new enumeration
                            figure, target_id, figure_width = create_ellipse('⨅', x_axis + 60, y_axis)
                            # Create the arrow linking the figure to the intersection
                            arrow = create_empty_dashed_arrow(figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            y_axis += 60
                            continue

                        elif 'owl:unionOf' in line:
                            # Create the figure to represent the beggining of a new enumeration
                            figure, target_id, figure_width = create_ellipse('⨆', x_axis + 60, y_axis)
                            # Create the arrow linking the figure to the intersection
                            arrow = create_empty_dashed_arrow(figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            y_axis += 60
                            continue

                        elif 'owl:complementOf' in line:
                            # Create the figure to represent the beggining of a new enumeration
                            figure, target_id, figure_width = create_empty_box(x_axis + 60, y_axis)
                            # Create the arrow linking the figure to the intersection
                            arrow = create_empty_dashed_arrow(figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            y_axis += 60
                            continue


                # Create the figure representing a member of the intersection
                box, box_id, box_width = create_box(clean_term(pattern[index].strip()), x_axis + 60, y_axis)
                # Create the arrow linking the figure to the intersection
                arrow = create_empty_dashed_arrow(figure_id, box_id)
                diagram += f'{box}{arrow}'
                y_axis += 60

        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return index, y_axis - 60

def visualize_document(pattern_text, width_lenght, height_lenght, y_pos, pattern_number):
    global diagram

    #document, x_axis, y_axis_document = create_document(pattern_text, width_lenght, height_lenght, 0, y_pos)
    document, x_axis, y_axis_document = create_document2(pattern_text, width_lenght, height_lenght, 0, y_pos, pattern_number)
    y_axis_document += y_pos
    diagram += document

    return x_axis + 20, y_axis_document

def visualize_beggining(pattern, x_axis, y_axis):
    global diagram

    subject = clean_term(pattern[0].strip())
    predicate = clean_term(pattern[1].strip())
    object = clean_term(pattern[2].strip())

    box, box_id, box_width = create_box(subject, x_axis, y_axis)
    x_axis += len(predicate) * 8 + box_width

    if 'owl:Restriction' in object:
        figure, figure_id, figure_width = create_empty_box(x_axis, y_axis)
    
    elif 'owl:Class' in object or 'rdfs:Datatype' in object:

        object = clean_term(pattern[3].strip())

        if 'owl:oneOf' in object:
            figure, figure_id, figure_width = create_hexagon('&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis, y_axis)

        elif 'owl:intersectionOf' in object:
            figure, figure_id, figure_width = create_ellipse('⨅', x_axis, y_axis)
        
        elif 'owl:unionOf' in object:
            figure, figure_id, figure_width = create_ellipse('⨆', x_axis, y_axis)
        
        elif 'owl:complementOf' in object:
            figure, figure_id, figure_width = create_empty_box(x_axis, y_axis)
        
        else:
            raise Exception('Structure corrupted')
    
    else:
        raise Exception('Structure corrupted')

    x_axis += figure_width

    if 'rdfs:subClassOf' in predicate:
        arrow = create_block_arrow(box_id, figure_id)

    elif 'owl:equivalentClass' in predicate:
        arrow = create_double_block_dashed_arrow('&amp;lt;&amp;lt;owl:equivalentClass&amp;gt;&amp;gt;', box_id, figure_id)

    elif 'owl:disjointWith' in predicate:
        arrow = create_double_block_dashed_arrow('&amp;lt;&amp;lt;owl:disjointWith&amp;gt;&amp;gt;', box_id, figure_id)
    
    else:
        arrow = create_arrow(predicate, box_id, figure_id)

    diagram += f'{box}{figure}{arrow}'

    return x_axis, figure_id

def iterate_enumeration(index, pattern, pattern_len, father_deep, figure_id, x_axis, y_axis):
    global diagram

    # Iterate the structure
    while index < pattern_len:
        # Read a line of the structure
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Is the line outside the enumeration?
        if deep <= father_deep:
            # Return the line where the enumeration ends
            return index, y_axis - 60
        
        # Does the line represents an element of the enumeration?
        elif 'rdf:first' in line:
            # Get the position of the next line
            index += 1
            # Create the figure representing a member of the enumeration
            box, box_id, box_width = create_box(clean_term(pattern[index].strip()), x_axis + 60, y_axis)
            # Create the arrow linking the figure to the enumeration
            arrow = create_empty_dashed_arrow(figure_id, box_id)
            diagram += f'{box}{arrow}'
            y_axis += 60

        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return index, y_axis - 60

def iterate_restriction(index, pattern, pattern_len, father_deep, figure_id, x_axis, y_axis):

    # Variable to store the type of a property involved in a resctriction
    property = ''
    # Variable to store the type of the target involved in a resctriction
    target = ''
    # Variable to store the type of the resctriction
    type = ''

    aux = True

    anonymous_type = 0
    anonymous_index = 0
    anonymous_deep = 0

    # Iterate the structure
    while index < pattern_len:
        # Read a line of the structure
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Is the line outside the restriction?
        if deep <= father_deep:
            # Create the figures representing the restriction
            y_axis = visualize_restriction(clean_term(property.strip()), clean_term(target.strip()), type, figure_id, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
            # Return the position where the restriction ends
            return index, y_axis

        # Does the line represents an element of the restriction?
        if deep == father_deep + 1:
            # We are reading an element of the restriction (e.g. someValuesFrom, onProperty etc)

            # Does the line represents the property?
            if 'owl:onProperty' in line:
                # In the next line the property type is defined (e.g. owl:ObjectProperty, #Unknown, etc)
                # Get the position of the next line
                index += 1
                # Get the property type
                property = pattern[index]
            
            # Does the line represents the target?
            elif 'owl:someValuesFrom' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                index += 1
                # Get the target type
                target = pattern[index]
                # Get the restriction type
                type = '(some)'
            
            # Does the line represents the target?
            elif 'owl:allValuesFrom' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                index += 1
                # Get the target type
                target = pattern[index]
                # Get the restriction type
                type = '(all)'
            
            # Does the line represents the target?
            elif 'owl:onClass' in line or 'owl:onDataRange' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                index += 1
                # Get the target type
                target = pattern[index]

            elif 'owl:cardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '(N1..N1)'

            elif 'owl:qualifiedCardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '[N1..N1]'
            
            elif 'owl:maxCardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '(0..N2)'

            elif 'owl:maxQualifiedCardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '[0..N2]'
            
            elif 'owl:minCardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '(N1..N)'
            
            elif 'owl:minQualifiedCardinality' in line:
                # Get the position of the next line
                index += 1
                # Get the restriction type
                type = '[N1..N]'
            
            # Does the line represents the target?
            elif 'owl:hasValue' in line:
                # In the next line the target type is defined (e.g. owl:Class, #Unknown, etc)
                # Get the position of the next line
                index += 1
                # Get the target type
                target = pattern[index]
                # Get the restriction type
                type = '(value)'
                
            else:
                # Get the position of the next line
                index += 1
        
        elif aux:
            global diagram

            # Does the line represents the beggining of a restriction?
            if 'owl:Restriction' in line:
                aux = False
                anonymous_type = 1
                anonymous_index = index + 1
                anonymous_deep = deep

            elif 'owl:oneOf' in line:
                aux = False
                anonymous_type = 2
                anonymous_index = index + 1
                anonymous_deep = deep

            elif 'owl:intersectionOf' in line:
                aux = False
                anonymous_type = 3
                anonymous_index = index + 1
                anonymous_deep = deep

            elif 'owl:unionOf' in line:
                aux = False
                anonymous_type = 4
                anonymous_index = index + 1
                anonymous_deep = deep

            elif 'owl:complementOf' in line:
                aux = False
                anonymous_type = 5
                anonymous_index = index + 1
                anonymous_deep = deep
            
            elif 'owl:withRestrictions' in line:
                aux = False
                anonymous_type = 6
                anonymous_index = index + 1
                anonymous_deep = deep
            
            elif 'owl:datatypeComplementOf' in line:
                aux = False
                anonymous_type = 7
                anonymous_index = index + 1
                anonymous_deep = deep

            else:
                # Get the position of the next line
                index += 1
        
        else:
            index += 1

    # In this case we have reached the end of the structure
    # Create the figures representing the restriction
    y_axis = visualize_restriction(clean_term(property.strip()), clean_term(target.strip()), type, figure_id, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
    
    # Return a number which is greater than the number of lines in the list
    return index, y_axis

def visualize_restriction(property, target, type, figure_id, previous_x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len):
    global diagram

    # Variable to store the property with the chowlk format. For example:
    #   - Pattern format: owl:FunctionalProperty, owl:ObjectProperty
    #   - Chowlk format: (F) owl:ObjectProperty
    cleaned_property = ''

    datatype_property = False

    # It is neccesary to check if the property has additional types defined. This additional types are separated
    # through simple commas ','
    if ',' in property:

        # Variable to store if a main property type is defined. It can be the cased that the user has defined
        # the property as rdfs:Property
        property_not_defined = True

        # Parse pattern format to chowlk format

        if 'owl:FunctionalProperty' in property:
            cleaned_property += '(F) '
        
        if 'owl:InverseFunctionalProperty' in property:
            cleaned_property += '(IF) '
        
        if 'owl:SymmetricProperty' in property:
            cleaned_property += '(S) '
        
        if 'owl:TransitiveProperty' in property:
            cleaned_property += '(T) '

        if 'owl:ObjectProperty' in property:
            cleaned_property += 'owl:ObjectProperty '
            property_not_defined = False
        
        if 'owl:DatatypeProperty' in property:
            cleaned_property += 'owl:DatatypeProperty '
            datatype_property = True
            property_not_defined = False
        
        if property_not_defined:
            cleaned_property += 'rdf:Property '
    
    else:
        # Just the type of the property is defined
        cleaned_property = property

        if 'owl:DatatypeProperty' in property:
            datatype_property = True

    # Calculate the x axis where the next box is going to be located
    x_axis = (len(cleaned_property) + len(type)) * 8 + previous_x_axis

    if anonymous_type == 1:
        figure, target_id, figure_width = create_empty_box(x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the restriction ends
        index, y_axis = iterate_restriction(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)

    elif anonymous_type == 2:

        if datatype_property:
            box, target_id, box_width = create_box(f'{type} {cleaned_property}: {target}', previous_x_axis - 60, y_axis + 30)
            diagram += box
            diagram += create_cloud("No chowlk&lt;br&gt;notation", x_axis, y_axis)
            return y_axis
        
        else:
            # Create the figure to represent the beggining of a new enumeration
            figure, target_id, figure_width = create_hexagon('&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis, y_axis)
            diagram += f'{figure}'
            # Get the line where the enumeration ends
            index, y_axis = iterate_enumeration(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)

    
    elif anonymous_type == 3:
        # Create the figure to represent the beggining of a new enumeration
        figure, target_id, figure_width = create_ellipse('⨅', x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)
    
    
    elif anonymous_type == 4:
        # Create the figure to represent the beggining of a new enumeration
        figure, target_id, figure_width = create_ellipse('⨆', x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)
            
    
    elif anonymous_type == 5:
        # Create the figure to represent the beggining of a new restriction
        figure, target_id, figure_width = create_empty_box(x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the restriction ends
        index, y_axis = iterate_complement(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)

    else:

        if datatype_property:
            y_axis += 30
            # Create the figure representing the target involved
            if target:
                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                box, target_id, box_width = create_box(f'{type} {cleaned_property}: {target}', previous_x_axis - 60, y_axis)

            else:
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                box, target_id, box_width = create_box(f'{type} {cleaned_property}', previous_x_axis - 60, y_axis)
            
            diagram += box

            if anonymous_type == 6 or anonymous_type == 7:
                diagram += create_cloud("No chowlk&lt;br&gt;notation", x_axis, y_axis - 30)
                return y_axis
        
        else:

            # Create the figure representing the target involved
            if target:
                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                box, target_id, box_width = create_box(target, x_axis, y_axis)

            else:
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                box, target_id, box_width = create_empty_box(x_axis, y_axis)
            
            diagram += box
    
    if not datatype_property:
        # Create the figure representing the property involved
        arrow = create_arrow(f'{type} {cleaned_property}', figure_id, target_id)
        diagram += arrow
    
    return y_axis

# Function to get the value of the term from the last occurrence of the '|' character      
def clean_term(term):
    index = term.rfind('|') + 1
    return term[index:]

# Function to generate the headers of the XML file.
# Drawio.io needs this headers in order to correctly proccesed the diagram.
def generate_XML_headers():
    global diagram
    diagram =   '<?xml version="1.0" encoding="UTF-8"?>\n'\
                '<mxfile host="" modified="" agent="" version="" etag="" type="">\n'\
                '  <diagram id="diagram1" name="Página-1">\n'\
                '    <mxGraphModel dx="1221" dy="713" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="100" pageHeight="100" math="0" shadow="0">\n'\
                '      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n'

# Function to generate the footers of the XML file.
# Drawio.io needs this footers in order to correctly proccesed the diagram.
def generate_footers():
    global diagram
    diagram = diagram + '      </root>\n'\
                        '    </mxGraphModel>\n'\
                        '  </diagram>\n'\
                        '</mxfile>\n'

# Function to calculate the deep of a structure line.
# The deep is represented by the number of times '|' appears in a line.
def get_deep(line):
    # Variable to store the line deep
    deep = 0

    # Iterate each character of the line
    for char in line:

        # Does the char represent ' '?
        if char == ' ':
            # This means there is a '|' ahead
            continue

        # Does the char represent '|'?
        elif char == '|':
            # Increase the line deep
            deep += 1

        else:
            # In this case the term has been reached and the line deep has been calculated
            break
    
    # Return the line deep
    return deep