from Code.visualize_pattern.create_svg_element import *

max_x = 0
max_y = 30
# Global variable to store the content of the svg file
svg = []

def create_svg(pattern, pattern_identifier):
    # Resets the global variables (they are not empty if there has been a previous iteration)
    global svg, max_x, max_y
    svg = []
    max_x = 0
    max_y = 30

    x_axis, y_axis = 0.5, 0

    x_axis, y_axis, chowlk_notation = visualize_beginning(pattern, x_axis, y_axis)

    if chowlk_notation:
        # Variable to store the position of the list it is being read.
        # The first position of interest represents the blank node after the predicate axiom 
        index = 2
        # Variable to store the length of the list
        pattern_len = len(pattern)

        # Iterate the pattern
        while index < pattern_len:
            # Read a line of the pattern
            line = pattern[index]
            # Get the deep of the line (the number of "  |")
            deep = line.count('  |')

            # Does the line represents the beginning of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, x_axis, y_axis)

            # Does the line represents the beginning of an enumeration?
            elif 'owl:oneOf' in line:
                # Get the line where the enumeration ends
                index, y_axis = iterate_enumeration(index + 1, pattern, pattern_len, deep, x_axis, y_axis)
            
            # Does the line represents the beginning of an intersection?
            elif 'owl:intersectionOf' in line:
                # Get the line where the intersection ends
                index, y_axis = iterate_intersection(index + 1, pattern, pattern_len, deep, x_axis, y_axis, '⨅')
            
            # Does the line represents the beginning of an union?
            elif 'owl:unionOf' in line:
                # Get the line where the union ends
                index, y_axis = iterate_intersection(index + 1, pattern, pattern_len, deep, x_axis, y_axis, '⨆')
            
            # Does the line represents the beginning of a complement?
            elif 'owl:complementOf' in line:
                # Get the line where the intersection ends
                index, y_axis = iterate_complement(index + 1, pattern, pattern_len, deep, x_axis, y_axis)

            else:
                index += 1

    else:
        element = create_cloud(0.5, 30, 'No chowlk<br />notation')
        svg.append(element)
        max_x = 123
        max_y = 82

    # Create svg file
    f = open(pattern_identifier, 'w', encoding='utf-8')
    create_headers(f)
    f.writelines(svg)
    create_footers(f)
    f.close()
    return

def iterate_restriction(index, pattern, pattern_len, father_deep, x_axis, y_axis):
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
        deep = line.count('  |')

        # Is the line outside the restriction?
        if deep <= father_deep:
            # In this case we have reached the end of the structure
            y_axis = visualize_restriction(clean_term(property), clean_term(target), type, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
            # Return the position where the restriction ends

            return index, y_axis

        # Does the line represents an element of the restriction?
        elif deep == father_deep + 1:
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

            # Does the line represents the beginning of a restriction?
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
    y_axis = visualize_restriction(clean_term(property), clean_term(target), type, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
            
    # Return a number which is greater than the number of lines in the list
    return index, y_axis

def visualize_restriction(property, target, type, previous_x_axis, previous_y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len):
    global max_x, max_y
    
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
        element, width = create_empty_box(previous_x_axis, previous_y_axis)
        svg.append(element)
        x_axis += width
        previous_x_axis += width
        # Get the line where the restriction ends
        index, y_axis = iterate_restriction(anonymous_index, pattern, pattern_len, anonymous_deep, x_axis, previous_y_axis)
    
    elif anonymous_type == 2:

        if datatype_property:
            element, width = create_empty_box_2((len(f'{type} {cleaned_property}: {target}')) * 6.2, previous_x_axis, previous_y_axis)
            svg.append(element)
            element, width = create_box(f'{type} {cleaned_property}: {target}', previous_x_axis, previous_y_axis + 30)
            svg.append(element)
            y_axis = previous_y_axis + 30
            element = create_cloud(previous_x_axis + width, y_axis, 'No further chowlk <br />notation')
            svg.append(element)
            max_x = max(max_x, previous_x_axis + width + 130)
            max_y = max(max_y, y_axis + 50)
        
        else:
            element, width = create_empty_box(previous_x_axis, previous_y_axis)
            svg.append(element)
            x_axis += width
            previous_x_axis += width
            # Get the line where the enumeration ends
            index, y_axis = iterate_enumeration(anonymous_index, pattern, pattern_len, anonymous_deep, x_axis, previous_y_axis)

    
    elif anonymous_type == 3:
        element, width = create_empty_box(previous_x_axis, previous_y_axis)
        svg.append(element)
        x_axis += width
        previous_x_axis += width
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, x_axis, previous_y_axis, '⨅')
    
    
    elif anonymous_type == 4:
        element, width = create_empty_box(previous_x_axis, previous_y_axis)
        svg.append(element)
        x_axis += width
        previous_x_axis += width
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, x_axis, previous_y_axis, '⨆')
            
    
    elif anonymous_type == 5:
        element, width = create_empty_box(previous_x_axis, previous_y_axis)
        svg.append(element)
        x_axis += width
        previous_x_axis += width
        # Get the line where the restriction ends
        index, y_axis = iterate_complement(anonymous_index, pattern, pattern_len, anonymous_deep, x_axis, previous_y_axis)

    else:
        y_axis = previous_y_axis

        if datatype_property:
            y_axis += 30

            # Create the figure representing the target involved
            if target:

                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                if type == '(value)':
                    element, width = create_empty_box_2((len(f'{type} {cleaned_property}: &quot;{target}&quot;')) * 6.2, previous_x_axis, y_axis -30)
                    svg.append(element)
                    element, width = create_box(f'{type} {cleaned_property}: &quot;{target}&quot;', previous_x_axis, y_axis)

                else:
                    element, width = create_empty_box_2((len(f'{type} {cleaned_property}: {target}')) * 6.2, previous_x_axis, y_axis -30)
                    svg.append(element)
                    element, width = create_box(f'{type} {cleaned_property}: {target}', previous_x_axis, y_axis)

            else:
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                element, width = create_empty_box_2((len(f'{type} {cleaned_property}')) * 6.2, previous_x_axis, y_axis -30)
                svg.append(element)
                element, width = create_box(f'{type} {cleaned_property}', previous_x_axis, y_axis)
            
            svg.append(element)
            max_x = max(max_x, previous_x_axis + width)
            max_y = max(max_y, y_axis + 30)

            if anonymous_type == 6 or anonymous_type == 7:
                element = create_cloud(previous_x_axis + width, y_axis, 'No further chowlk <br />notation')
                svg.append(element)
                max_x = max(max_x, previous_x_axis + width + 130)
                max_y = max(max_y, y_axis + 50)
        
        else:
            element, width = create_empty_box(previous_x_axis, y_axis)
            svg.append(element)
            previous_x_axis += width
            x_axis += width
            #max_x = max(max_x, previous_x_axis + width)

            # Create the figure representing the target involved
            if target:

                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                if type == '(value)':
                    element, width = create_underlined_box(target, x_axis, y_axis)

                else:
                    element, width = create_box(target, x_axis, y_axis)

            else:
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                element, width = create_empty_box(x_axis, y_axis)
            
            max_x = max(max_x, x_axis + width)
            max_y = max(max_y, y_axis + 30)
            #f.write(element)
            svg.append(element)
    
    if not datatype_property:
        # Create the figure representing the property involved
        element = create_arrow(f'{type} {cleaned_property}', previous_x_axis, x_axis, previous_y_axis + 15)
        svg.append(element)
    
    return y_axis

def iterate_enumeration(index, pattern, pattern_len, father_deep, x_axis, previous_y_axis):
    global max_x, max_y
    y_axis = previous_y_axis
    element, width = create_hexagon('&lt;&lt;owl:oneOf&gt;&gt;', x_axis, y_axis, len('&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;') * 3.3)
    svg.append(element)
    x_axis += width
    max_x = max(max_x, x_axis)
    max_y = max(max_y, y_axis + 30)

    first_arrow = True


    # Iterate the pattern
    while index < pattern_len:
        # Read a line of the pattern
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the enumeration?
        if deep <= father_deep:
            # Return the position where the enumeration ends and the next Y axis
            return index, y_axis - 60
        
        # Does the line represents that the next line contains an element of the enumeration?
        elif 'rdf:first' in line:
            # Get the position of the next line
            index += 1
            # Create the figure representing a member of the enumeration

            # Does the element represent a data value?
            if 'Data value' in pattern[index]:
                # Create the figure representing a data value (i.e. a box whose name is between "")
                element, width = create_quot_box('Data Value', x_axis + 60, y_axis)
            
            else:
                # Create the figure representing an individual (i.e. an underlined box)
                element, width = create_underlined_box(clean_term(pattern[index]), x_axis + 60, y_axis)

            # Add the new box to the diagram
            svg.append(element)

            # Create the arrow connecting the box to the hexagon representing the beginning of the enumeration
            if first_arrow:
                first_arrow = False
                element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
            
            else:
                element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)
            
            # Add the new arrow to the diagram
            svg.append(element)

            # Calculate the Y axis where the next element should be placed so it does not overlap with the box
            max_x = max(max_x, x_axis + width + 60)
            max_y = max(max_y, y_axis + 30)
            y_axis += 60
            
        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list and the next Y axis
    return index, y_axis - 60

def iterate_intersection(index, pattern, pattern_len, father_deep, x_axis, previous_y_axis, intersection_union):
    global max_x, max_y
    y_axis = previous_y_axis
    first_arrow = True

    element, width = create_ellipse(intersection_union, x_axis, y_axis)
    x_axis += width
    max_x = max(max_x, x_axis)
    max_y = max(max_y, y_axis + 30)
    svg.append(element)

    # Iterate the pattern
    while index < pattern_len:
        # Read a line of the pattern
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the intersection/union of classes?
        if deep <= father_deep:
            # Return the line where the intersection/union ends
            return index, y_axis - 60
        
        # Does the line represents that the next line contains an element of the intersection/union?
        elif 'rdf:first' in line:
            # Get the position of the next line
            index += 1
            # Read the next line of the pattern
            line = pattern[index]
            # Get the deep of the next line (the number of "  |")
            deep = line.count('  |')

            # Does the line represents the beginning of a restriction?
            if 'owl:Restriction' in line:
                # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the figure which represents the beginning of a restriction
                if first_arrow:
                    first_arrow = False
                    element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
                
                else:
                    element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)

                svg.append(element)    
                # Get the line where the restriction ends
                index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, x_axis + 60, y_axis)
                # Calculate the Y axis where the next element should be placed so it does not overlap with the restriction
                y_axis += 60
            
            else:
                # In this case the class description is either a named class or a blank node which is not a restriction

                # Is there a next line?
                if index + 1 < pattern_len:
                    # Read the next line of the pattern
                    line = pattern[index + 1]
                    # Get the deep of the next line (the number of "  |")
                    deep = line.count('  |')

                    # Is the line inside the intersection/union?
                    if deep > father_deep:

                        # Does the line represents the beginning of an enumeration?
                        if 'owl:oneOf' in line:
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the hexagon, which represents the beginning of a enumeration
                            if first_arrow:
                                first_arrow = False
                                element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
                            
                            else:
                                element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)
                            
                            svg.append(element)
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, x_axis  + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the enumeration
                            y_axis += 60
                            continue

                        # Does the line represents the beginning of an intersection or union?
                        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                            intersection_union = '⨅' if 'owl:intersectionOf' in line else '⨆'
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the ellipse, which represents the beginning of an intersection
                            if first_arrow:
                                first_arrow = False
                                element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
                            
                            else:
                                element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)
                            
                            svg.append(element)
                            # Get the line where the intersection ends
                            index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, x_axis + 60, y_axis, intersection_union)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the intersection
                            y_axis += 60
                            continue

                        # Does the line represents the beginning of a complement?
                        elif 'owl:complementOf' in line:
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the blank box, which represents the beginning of a complement
                            if first_arrow:
                                first_arrow = False
                                element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
                            
                            else:
                                element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)
                            
                            svg.append(element)
                            # Get the line where the complement ends
                            index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, x_axis + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the complement
                            y_axis += 60
                            continue

                # In this case the class description represents a named class
                # Create the box to represent a named class
                element, width = create_box(clean_term(pattern[index]), x_axis + 60, y_axis)
                svg.append(element)

                # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the box, which represents the named class
                if first_arrow:
                    first_arrow = False
                    element = create_empty_dashed_arrow(x_axis, x_axis + 60, y_axis + 15)
                
                else:
                    element = create_empty_orthogonal_dashed_arrow(x_axis, x_axis + 60, previous_y_axis + 15, y_axis + 15)

                svg.append(element)

                # Calculate the Y axis where the next element should be placed so it does not overlap with the named class
                max_x = max(max_x, x_axis + width + 60)
                max_y = max(max_y, y_axis + 30)
                y_axis += 60
                

        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return index, y_axis - 60

def iterate_complement(index, pattern, pattern_len, father_deep, x_axis, y_axis):
    global max_x, max_y

    element, width = create_empty_box(x_axis, y_axis)
    svg.append(element)
    x_axis += width

    # Iterate the pattern
    while index < pattern_len:
        # Read a line of the pattern
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = line.count('  |')

        # Is the line outside the complement?
        if deep <= father_deep:
            # Return the position where the complement ends and the next Y axis
            return index, y_axis

        # Does the line represents the beginning of a restriction?
        elif 'owl:Restriction' in line:
            # Create the arrow which represents this complement
            # This arrow connects the blank box, which represents the beginning of this complement, to the figure which represents the beginning of a restriction
            element = create_dashed_arrow('&lt;&lt;owl:complementOf&gt;&gt;', x_axis, x_axis + 200, y_axis + 15)
            svg.append(element)
            # Get the line where the restriction ends
            index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, x_axis + 200, y_axis)
        
        else:
            # In this case the class description is either a named class or a blank node which is not a restriction
            # This variable store the line where the class description starts
            target = line

            # Is there a next line?
            if index + 1 < pattern_len:
                # Read the next line of the pattern
                line = pattern[index + 1]
                # Get the deep of the next line (the number of "  |")
                deep = line.count('  |')

                # Is the line inside the complement?
                if deep > father_deep:

                    # Does the line represents the beginning of an enumeration?
                    if 'owl:oneOf' in line:
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the hexagon, which represents the beginning of an enumeration
                        element = create_dashed_arrow('&lt;&lt;owl:complementOf&gt;&gt;', x_axis, x_axis + 200, y_axis + 15)
                        svg.append(element)
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, x_axis + 200, y_axis)
                        continue

                    # Does the line represents the beginning of an intersection or an union?
                    elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
                        intersection_union = '⨅' if 'owl:intersectionOf' in line else '⨆'
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the ellipse, which represents the beginning of an intersection
                        element = create_dashed_arrow('&lt;&lt;owl:complementOf&gt;&gt;', x_axis, x_axis + 200, y_axis + 15)
                        svg.append(element)
                        # Get the line where the intersection ends
                        index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, x_axis + 200, y_axis, intersection_union)
                        continue

                    # Does the line represents the beginning of a complement?
                    elif 'owl:complementOf' in line:
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the blank box, which represents the beginning of a complement
                        element = create_dashed_arrow('&lt;&lt;owl:complementOf&gt;&gt;', x_axis, x_axis + 200, y_axis + 15)
                        svg.append(element)
                        # Get the line where the complement ends
                        index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, x_axis + 200, y_axis)
                        continue

            # In this case the class description represents a named class
            # Create the box to represent a named class
            element, width = create_box(clean_term(target), x_axis + 200, y_axis)
            max_x = max(max_x, x_axis + 200 + width)
            max_y = max(max_y, y_axis + 30)
            svg.append(element)
            # Create the arrow which represents this complement
            # This arrow connects the blank box, which represents the beginning of this complement, to the box, which represents a named class
            element = create_dashed_arrow('&lt;&lt;owl:complementOf&gt;&gt;', x_axis, x_axis + 200, y_axis + 15)
            svg.append(element)

            # Get the next line
            index += 1
    
    # Return a number which is greater than the number of lines in the list and the next Y axis
    return index, y_axis

# Function to generate the headers of the svg file
def create_headers(f):
    headers =   '<?xml version="1.0" encoding="UTF-8"?>\n'\
                '<!-- Do not edit this file with editors other than draw.io -->\n'\
                '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'\
                f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="{max_x + 1}px" height="{max_y + 1}px" viewBox="-0.5 -0.5 {max_x + 1} {max_y + 1}">\n'\
                '   <defs/>\n'\
                '   <g>\n'
    f.write(headers)

# Function to generate the footers of the svg file
def create_footers(f):
    footers =   '   </g>\n'\
                '</svg>'
    f.write(footers)

# Function to get the value of the term from the last occurrence of the '|' character.
# Moreover, the whitespaces at the beginning and ending of the string are removed.
def clean_term(term):
    index = term.rfind('|') + 1
    return term[index:].strip()

def visualize_beginning(pattern, x_axis, y_axis):
    # Get the terms related to the beginning of a pattern
    subject = clean_term(pattern[0])
    predicate = clean_term(pattern[1])
    object = pattern[2]

    first_element, width = create_box(subject, x_axis, y_axis) 
    x_axis += width

    # Check if there is chowlk notation to represent the beginning of the pattern
    if 'owl:Class' in object or 'rdfs:Datatype' in object:
        object = pattern[3]

        if 'owl:oneOf' not in object and 'owl:intersectionOf' not in object and 'owl:unionOf' not in object and 'owl:complementOf' not in object:
            return x_axis, y_axis, False
    
    elif 'owl:Restriction' not in object:
        return x_axis, y_axis, False

    # The next lines will create the figure of the predicate
    if 'rdfs:subClassOf' in predicate:
        element, x_axis = create_block_arrow(predicate, x_axis, y_axis + 15)
    
    elif 'owl:equivalentClass' in predicate:
        element, x_axis = create_double_block_dashed_arrow('&lt;&lt;owl:equivalentClass&gt;&gt;', x_axis, len(predicate) * 8 + x_axis, y_axis + 15)

    # Does the predicate represents a disjoint class?
    elif 'owl:disjointWith' in predicate:
        element, x_axis = create_double_block_dashed_arrow('&lt;&lt;owl:disjointWith&gt;&gt;', x_axis, len(predicate) * 8 + x_axis, y_axis + 15)
    
    else:
        return x_axis, y_axis, False
    
    svg.append(first_element)
    svg.append(element)

    return x_axis, y_axis, True