from create_diagram_element import *
from create_svg import create_svg

# Global variable to store the content of the XML file
diagram = ''
# Global variable to create unique identifiers for each figure
figure_identifier = 0

# Function to create the XML diagram where the patterns are going to be visualizated.
# This XML file has to follow the drawio.io structure (since this application is going to open the XML).
def create_diagram(pattern_path):
        
        # Create the neccesary headers of the XML which contains the visualization
        generate_XML_headers()
        # Open the file with the detected patterns
        pattern_file = open(pattern_path , "r", encoding='utf-8')
        # Read the first pattern
        pattern, max_lenght, pattern_text, pattern_number = read_pattern(pattern_file)
        # Variable to store the starting Y axis of a new pattern (to not overlap the figures)
        y_axis = 0

        # Iterate while there is at least one pattern unread
        while(len(pattern) > 0):
            # Create the visualization of the pattern
            y_axis = visualize_pattern(pattern, y_axis, max_lenght, pattern_text, pattern_number)
            create_svg(pattern, pattern_number)
            # Read a new pattern
            pattern, max_lenght, pattern_text, pattern_number = read_pattern(pattern_file)

        # Close the the file with the detected patterns (the end has been reached)
        pattern_file.close()
        # Create the neccesary footers of the XML which contains the visualization
        generate_footers()

        # Write the results
        f = open('Visualization.xml', 'w', encoding='utf-8')
        f.write(diagram)
        f.close()

# Function to parse just one pattern into a list. Different patterns are separated by blank lines.
# When a blank node is read this function returns:
#   - The pattern parsed into a list (in order to iterate the pattern)
#   - The pattern as a raw string (in order to create a document figure)
#   - The length of the longest pattern line (in order to calculate the width of the document figure)
#   - The unique identifier of the pattern    
def read_pattern(pattern_file):
    # List that will store each line of the pattern being read
    pattern = []

    # The first line contains the identifier of the pattern
    pattern_identifier = pattern_file.readline().strip()
    # The following three lines contain metadata (Skip them)
    pattern_file.readline()
    pattern_file.readline()
    pattern_file.readline()

    # Variable to store the length of the longest line
    max_lenght = 0

    # Read fifth line (already contains pattern data)
    line = pattern_file.readline()
    # Variable to store the pattern as text
    pattern_text = ''

    # Iterate the lines of the TXT file until a blank node is read (i.e. until the end of a pattern has been reached)
    while(line and len(line) > 1):
        # Check if the line that is being read is longer than the previous lines
        max_lenght = max(max_lenght, len(line))
        # Add structure line
        pattern.append(line)
        # Add structure line as raw text
        pattern_text += f'{line.strip()}&lt;br&gt;&amp;nbsp;'
        # Read a new line
        line = pattern_file.readline()
    
    # It is neccesary to remove the last "&lt;br&gt;&amp;nbsp;", which represents a line break
    return pattern, max_lenght, pattern_text[:-20], pattern_identifier

# This function will create for each pattern the necessary XML code in order to visualizate them using drawio.io
def visualize_pattern(pattern, y_axis, max_lenght, pattern_text, pattern_number):
    # Declare global variables (in order to change them)
    global diagram

    # Create a vertical container element in order to write the pattern as raw text
    x_axis, y_axis_document = visualize_document(pattern_text, max_lenght, len(pattern), y_axis, pattern_number)

    try:
        # Create the elements that represents the beginning of a pattern
        x_axis, figure_id = visualize_beginning(pattern, x_axis, y_axis)
    
    except:
        # In this case a exception has been raised indicating that there is no Chowlk notation to represents the pattern

        # Declare global variables (in order to change them)
        global figure_identifier

        # Create a new cloud element and add it to the diagram
        figure_identifier += 1
        diagram += create_cloud(figure_identifier, "No chowlk&lt;br&gt;notation", x_axis, y_axis)

        # Return where the new pattern should start checking what is higher: 
        # the figure representing the pattern as raw text or the figure representing the pattern
        return max(y_axis, y_axis_document) + 60
    
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
            index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        # Does the line represents the beginning of an enumeration?
        elif 'owl:oneOf' in line:
            # Get the line where the enumeration ends
            index, y_axis = iterate_enumeration(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        # Does the line represents the beginning of an intersection/union?
        elif 'owl:intersectionOf' in line or 'owl:unionOf' in line:
            # Get the line where the intersection/union ends
            index, y_axis = iterate_intersection(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        # Does the line represents the beginning of a complement?
        elif 'owl:complementOf' in line:
            # Get the line where the intersection ends
            index, y_axis = iterate_complement(index + 1, pattern, pattern_len, deep, figure_id, x_axis, y_axis)
        
        else:
            # Get the next line
            index += 1

    # Return where the new pattern should start checking what is higher: 
    # the figure representing the pattern as raw text or the figure representing the pattern
    return max(y_axis, y_axis_document) + 60

# This function will create the figures that correspond to a complement class description.
# An complement class description is represented in Chowlk notation through:
#   - A blank box which represents the beginning of the complement. This blank box has been created previously and its identifier is "father_id"
#   - The class description, which can be either a named class or another blank node.
#   - An arrow, whose value is "<<owl:complementOf>>", which connects the class description to the blank box.
# In order to classify the class description the following rules are applied:
#   1) When a 'owl:Restriction' statement is being read, the class description is a restriction.
#   2) When another element is being read (e.g. owl:Class) and the end of the complement has not been reached, 
#       then the next line represents the beginning of a blank node.
#   3) When another element is being read (e.g. owl:Class) and the end of the complement has been reached,
#        then the class description is a named class
# This function returns:
#   - The position of the list where the enumeration ends
#   - The Y axis where the next element should be placed so it does not overlap with the class description (which is now the lowest element)
def iterate_complement(index, pattern, pattern_len, father_deep, father_id, x_axis, y_axis):
    # Declare global variables (in order to change them)
    global diagram, figure_identifier

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
            # Create the identifier of the figure which represents the beginning of a restriction
            figure_identifier += 1
            target_id = f'class-{figure_identifier}'
            # Create the arrow which represents this complement
            # This arrow connects the blank box, which represents the beginning of this complement, to the figure which represents the beginning of a restriction
            figure_identifier += 1
            diagram += create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
            # Get the line where the restriction ends
            index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, target_id, x_axis + 200, y_axis)
        
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
                        # Create an hexagon to represent the beginning of a new enumeration
                        figure_identifier += 1
                        figure, target_id, figure_width = create_hexagon(figure_identifier, '&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis + 200, y_axis)
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the hexagon, which represents the beginning of an enumeration
                        figure_identifier += 1
                        arrow = create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the enumeration ends
                        index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    # Does the line represents the beginning of an intersection?
                    elif 'owl:intersectionOf' in line:
                        # Create the ellipse to represent the beginning of an intersection
                        figure_identifier += 1
                        figure, target_id, figure_width = create_ellipse(figure_identifier, '⨅', x_axis + 200, y_axis)
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the ellipse, which represents the beginning of an intersection
                        figure_identifier += 1
                        arrow = create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the intersection ends
                        index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    # Does the line represents the beginning of an union?
                    elif 'owl:unionOf' in line:
                        # Create the ellipse to represent the beginning of an union
                        figure_identifier += 1
                        figure, target_id, figure_width = create_ellipse(figure_identifier, '⨆', x_axis + 200, y_axis)
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the ellipse, which represents the beginning of an union
                        figure_identifier += 1
                        arrow = create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the union ends
                        index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

                    # Does the line represents the beginning of a complement?
                    elif 'owl:complementOf' in line:
                        # Create the blank box to represent the beginning of a complement
                        figure_identifier += 1
                        figure, target_id, figure_width = create_empty_box(figure_identifier, x_axis + 200, y_axis)
                        # Create the arrow which represents this complement
                        # This arrow connects the blank box, which represents the beginning of this complement, to the blank box, which represents the beginning of a complement
                        figure_identifier += 1
                        arrow = create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
                        diagram += f'{figure}{arrow}'
                        # Get the line where the complement ends
                        index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 200, y_axis)
                        continue

            # In this case the class description represents a named class
            # Create the box to represent a named class
            figure_identifier += 1
            figure, target_id, figure_width = create_box(figure_identifier, clean_term(target), x_axis + 200, y_axis)
            # Create the arrow which represents this complement
            # This arrow connects the blank box, which represents the beginning of this complement, to the box, which represents a named class
            figure_identifier += 1
            arrow = create_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:complementOf&amp;gt;&amp;gt;', father_id, target_id)
            diagram += f'{figure}{arrow}'

            # Get the next line
            index += 1
    
    # Return a number which is greater than the number of lines in the list and the next Y axis
    return index, y_axis

# This function will create the figures that correspond to an intersection of class description.
# An intersection of class description is represented in Chowlk notation through:
#   - An ellipse which represents the beginning of the intersection. This ellipse has been created previously and its identifier is "father_id"
#   - When a "rdf:first" statemnet is being read, the next element represents a class description, which can be either a named class or another blank node.
#   - Dashed arrows connecting each class description to the hexagon
# In order to classify the class description the following rules are applied:
#   1) When a 'owl:Restriction' statement is being read, the class description is a restriction.
#   2) When another element is being read (e.g. owl:Class) and the end of the intersection has not been reached, 
#       then the next line represents the beginning of a blank node.
#   3) When another element is being read (e.g. owl:Class) and the end of the intersection has been reached,
#        then the class description is a named class
# This function returns:
#   - The position of the list where the intersection ends
#   - The Y axis where the next element should be placed so it does not overlap with the class description (which is now the lowest element)
def iterate_intersection(index, pattern, pattern_len, father_deep, figure_id, x_axis, y_axis):
    # Declare global variables (in order to change them)
    global diagram, figure_identifier

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
                # Create the identifier of the figure which represents the beginning of a restriction
                figure_identifier += 1
                target_id = f'class-{figure_identifier}'
                # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the figure which represents the beginning of a restriction
                figure_identifier += 1
                diagram += create_empty_dashed_arrow(figure_identifier, figure_id, target_id)
                # Get the line where the restriction ends
                index, y_axis = iterate_restriction(index + 1, pattern, pattern_len, deep, target_id, x_axis + 60, y_axis)
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
                            # Create an hexagon to represent the beginning of a new enumeration
                            figure_identifier += 1
                            figure, target_id, figure_width = create_hexagon(figure_identifier, '&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis + 60, y_axis)
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the hexagon, which represents the beginning of a enumeration
                            figure_identifier += 1
                            arrow = create_empty_dashed_arrow(figure_identifier, figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the enumeration ends
                            index, y_axis = iterate_enumeration(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the enumeration
                            y_axis += 60
                            continue

                        # Does the line represents the beginning of an intersection?
                        elif 'owl:intersectionOf' in line:
                            figure_identifier += 1
                            # Create an ellipse to represent the beginning of a new intersection
                            figure, target_id, figure_width = create_ellipse(figure_identifier, '⨅', x_axis + 60, y_axis)
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the ellipse, which represents the beginning of an intersection
                            figure_identifier += 1
                            arrow = create_empty_dashed_arrow(figure_identifier, figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the intersection ends
                            index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the intersection
                            y_axis += 60
                            continue

                        # Does the line represents the beginning of an union?
                        elif 'owl:unionOf' in line:
                            figure_identifier += 1
                            # Create an ellipse to represent the beginning of a new union
                            figure, target_id, figure_width = create_ellipse(figure_identifier, '⨆', x_axis + 60, y_axis)
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the ellipse, which represents the beginning of an union
                            figure_identifier += 1
                            arrow = create_empty_dashed_arrow(figure_identifier, figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the union ends
                            index, y_axis = iterate_intersection(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the union
                            y_axis += 60
                            continue

                        # Does the line represents the beginning of a complement?
                        elif 'owl:complementOf' in line:
                            figure_identifier += 1
                            # Create a blank box to represent the beginning of a new complement
                            figure, target_id, figure_width = create_empty_box(figure_identifier, x_axis + 60, y_axis)
                            figure_identifier += 1
                            # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the blank box, which represents the beginning of a complement
                            arrow = create_empty_dashed_arrow(figure_identifier, figure_id, target_id)
                            diagram += f'{figure}{arrow}'
                            # Get the line where the complement ends
                            index, y_axis = iterate_complement(index + 2, pattern, pattern_len, deep, target_id, x_axis + figure_width + 60, y_axis)
                            # Calculate the Y axis where the next element should be placed so it does not overlap with the complement
                            y_axis += 60
                            continue

                # In this case the class description represents a named class
                # Create the box to represent a named class
                figure_identifier += 1
                box, box_id, box_width = create_box(figure_identifier, clean_term(pattern[index]), x_axis + 60, y_axis)
                # Create the arrow which connects the ellipse, which represents the beginning of this intersection/union, to the box, which represents the named class
                figure_identifier += 1
                arrow = create_empty_dashed_arrow(figure_identifier, figure_id, box_id)
                diagram += f'{box}{arrow}'
                # Calculate the Y axis where the next element should be placed so it does not overlap with the named class
                y_axis += 60

        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list
    return index, y_axis - 60

# This function will create a vertical container in order to represent the pattern as raw text.
# This function returns the X and Y axes where the next element should be placed so it does not overlap with
# the vertical container.
def visualize_document(pattern_text, width_lenght, height_lenght, y_axis, pattern_number):
    # Declare global variables (in order to change them)
    global diagram, figure_identifier

    # Create a new vertical container element
    figure_identifier += 1
    vertical_container, x_axis, y_axis_document = create_vertical_container(figure_identifier, pattern_text, width_lenght, height_lenght, 0, y_axis, pattern_number)
    # Add the new element to the diagram
    diagram += vertical_container

    return x_axis + 20, y_axis_document + y_axis

# This function will create the figures that correspond to the beginning of a pattern.
# The beginning of a pattern contains the following elements:
#   - Subject: The term is either a class or a datatype. Therefhore this term is always represented as a box
#   - Predicate: This term represents a class axiom. This term is represented as a special type of arrow (depending of the class axiom)
#   - Object: This term represents a blank node. The type of the figure depends on the blank node
# This function returns:
#   - The identifier of the element which represents the beginning of a blank node
#   - The X axis where the next element should be placed so it does not overlap with the element which represents the beginning of the blank node (which is now the rightmost element)
def visualize_beginning(pattern, x_axis, y_axis):
    # Declare global variables (in order to change them)
    global diagram, figure_identifier

    # Get the terms related to the beginning of a pattern
    subject = clean_term(pattern[0])
    predicate = clean_term(pattern[1])
    object = clean_term(pattern[2])

    # Create a new box, which represents the subject
    figure_identifier += 1
    box, box_id, box_width = create_box(figure_identifier, subject, x_axis, y_axis)

    # Calculate the X axis where the next element should be placed so it does not overlap with the box and 
    # it leaves enough space for the arrow
    x_axis += len(predicate) * 8 + box_width

    # The next lines will create the figure of the object
    # Does the object represents a restriction?
    if 'owl:Restriction' in object:
        # The visualization of a restriction must be done after analyzing the type of the restriction.
        # This is because the element which represents the beginning of the restriction changes depending of the type.

        # Create the identifier of the element which will represent the origin of a restriction
        figure_identifier += 1
        figure_id = f'class-{figure_identifier}'
    
    # Does the object represents another kind of blank node?
    elif 'owl:Class' in object or 'rdfs:Datatype' in object:

        # Get the line with the header (in order to know the type of the blank node)
        object = clean_term(pattern[3])

        # Does the object represent an enumeration?
        if 'owl:oneOf' in object:
            # Create a new hexagon element to represent the beginning of an enumeration
            figure_identifier += 1
            figure, figure_id, figure_width = create_hexagon(figure_identifier, '&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis, y_axis)

        # Does the object represent an intersection?
        elif 'owl:intersectionOf' in object:
            # Create a new ellipse element to represent the beginning of an intersection
            figure_identifier += 1
            figure, figure_id, figure_width = create_ellipse(figure_identifier, '⨅', x_axis, y_axis)
        
        # Does the object represent an union?
        elif 'owl:unionOf' in object:
            # Create a new ellipse element to represent the beginning of an union
            figure_identifier += 1
            figure, figure_id, figure_width = create_ellipse(figure_identifier, '⨆', x_axis, y_axis)
        
        # Does the object represent a complement?
        elif 'owl:complementOf' in object:
            # Create a new empty box element to represent the beginning of a complement
            figure_identifier += 1
            figure, figure_id, figure_width = create_empty_box(figure_identifier, x_axis, y_axis)
        
        else:
            # There is no Chowlk notation to represent this pattern
            raise Exception('There is no Chowlk notation')
        
        # Add the new element, which represents the beginning of the blank node, to the diagram
        diagram += figure
        # Calculate the X axis where the next element should be placed so it does not overlap with the element
        # which represents the beginning of the blank node (which is now the rightmost element)
        x_axis += figure_width
    
    else:
        # This should not happen (the object always represents a blank node)
        raise Exception('Structure corrupted')

    # The next lines will create the figure of the predicate
    # Does the predicate represents a sub-class?
    if 'rdfs:subClassOf' in predicate:
         # Create a new arrow element to represent the class axiom
        figure_identifier += 1
        arrow = create_block_arrow(figure_identifier, box_id, figure_id)

    # Does the predicate represents an equivalent class?
    elif 'owl:equivalentClass' in predicate:
        # Create a new arrow element to represent the class axiom
        figure_identifier += 1
        arrow = create_double_block_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:equivalentClass&amp;gt;&amp;gt;', box_id, figure_id)

    # Does the predicate represents a disjoint class?
    elif 'owl:disjointWith' in predicate:
        # Create a new arrow element to represent the class axiom
        figure_identifier += 1
        arrow = create_double_block_dashed_arrow(figure_identifier, '&amp;lt;&amp;lt;owl:disjointWith&amp;gt;&amp;gt;', box_id, figure_id)
    
    else:
        # This should not happens
        figure_identifier += 1
        arrow = create_arrow(figure_identifier, predicate, box_id, figure_id)

    # Add the elements which represent the subject and the predicate to the diagram
    diagram += f'{box}{arrow}'

    return x_axis, figure_id

# This function will create the figures that correspond to an enumeration of individuals or data values.
# An enumeration is represented in Chowlk notation through:
#   - An hexagon which represents the beginning of the enumeration. This hexagon has been created previously and its identifier is "father_id"
#   - When a "rdf:first" statemnet is being read, the next element represents an individual or a data value involved in the enumeration. 
#       These terms are represented through special boxes.
#   - Dashed arrows connecting each box to the hexagon.
# This function returns:
#   - The position of the list where the enumeration ends
#   - The Y axis where the next element should be placed so it does not overlap with the last element of the enumeration (which is now the lowest element)
def iterate_enumeration(index, pattern, pattern_len, father_deep, father_id, x_axis, y_axis):
    # Declare global variables (in order to change them)
    global diagram, figure_identifier

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
            figure_identifier += 1

            # Does the element represent a data value?
            if 'Data value' in pattern[index]:
                # Create the figure representing a data value (i.e. a box whose name is between "")
                box, box_id, box_width = create_quot_box(figure_identifier, 'Data Value', x_axis + 60, y_axis)
            
            else:
                # Create the figure representing an individual (i.e. an underlined box)
                box, box_id, box_width = create_underlined_box(figure_identifier, clean_term(pattern[index]), x_axis + 60, y_axis)

            # Create the arrow connecting the box to the hexagon representing the beginning of the enumeration
            figure_identifier += 1
            arrow = create_empty_dashed_arrow(figure_identifier, father_id, box_id)
            # Add the new elements to the diagram
            diagram += f'{box}{arrow}'
            # Calculate the Y axis where the next element should be placed so it does not overlap with the box
            y_axis += 60

        else:
            # Get the position of the next line
            index += 1
    
    # In this case we have reached the end of the structure
    # Return a number which is greater than the number of lines in the list and the next Y axis
    return index, y_axis - 60

# ME QUEDA PONER COMENTARIOS EN ESTA FUNCION Y LA SIGUIENTE
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
        deep = line.count('  |')

        # Is the line outside the restriction?
        if deep <= father_deep:
            # Create the figures representing the restriction
            y_axis = visualize_restriction(clean_term(property), clean_term(target), type, figure_id, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
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
    # Create the figures representing the restriction
    y_axis = visualize_restriction(clean_term(property), clean_term(target), type, figure_id, x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len)
    
    # Return a number which is greater than the number of lines in the list
    return index, y_axis

def visualize_restriction(property, target, type, figure_id, previous_x_axis, y_axis, anonymous_type, anonymous_index, anonymous_deep, pattern, pattern_len):
    global diagram, figure_identifier
    
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
    x_axis = (len(cleaned_property) + len(type)) * 8 + previous_x_axis + 60 # CAMBIAR el 60

    if anonymous_type == 1:
        diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)
        figure_identifier += 1
        target_id = f'class-{figure_identifier}'
        """figure, target_id, figure_width = create_empty_box(figure_identifier, x_axis, y_axis)
        diagram += f'{figure}'"""
        # Get the line where the restriction ends
        index, y_axis = iterate_restriction(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis, y_axis)

    elif anonymous_type == 2:

        if datatype_property:
            diagram += create_empty_box_2(figure_id, (len(f'{type} {cleaned_property}: {target}')) * 6.2, previous_x_axis, y_axis)
            figure_identifier += 1
            box, target_id, box_width = create_box(figure_identifier, f'{type} {cleaned_property}: {target}', previous_x_axis, y_axis + 30)
            diagram += box
            figure_identifier += 1
            diagram += create_cloud(figure_identifier, "No further chowlk &lt;br&gt;notation", x_axis, y_axis)
            return y_axis
        
        else:
            diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)
            # Create the figure to represent the beginning of a new enumeration
            figure_identifier += 1
            figure, target_id, figure_width = create_hexagon(figure_identifier, '&amp;lt;&amp;lt;owl:oneOf&amp;gt;&amp;gt;', x_axis, y_axis)
            diagram += f'{figure}'
            # Get the line where the enumeration ends
            index, y_axis = iterate_enumeration(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)

    
    elif anonymous_type == 3:
        diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)
        figure_identifier += 1
        # Create the figure to represent the beginning of a new enumeration
        figure, target_id, figure_width = create_ellipse(figure_identifier, '⨅', x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)
    
    
    elif anonymous_type == 4:
        diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)
        figure_identifier += 1
        # Create the figure to represent the beginning of a new enumeration
        figure, target_id, figure_width = create_ellipse(figure_identifier, '⨆', x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the enumeration ends
        index, y_axis = iterate_intersection(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)
            
    
    elif anonymous_type == 5:
        diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)
        figure_identifier += 1
        # Create the figure to represent the beginning of a new restriction
        figure, target_id, figure_width = create_empty_box(figure_identifier, x_axis, y_axis)
        diagram += f'{figure}'
        # Get the line where the restriction ends
        index, y_axis = iterate_complement(anonymous_index, pattern, pattern_len, anonymous_deep, target_id, x_axis + figure_width, y_axis)

    else:

        if datatype_property:

            y_axis += 30

            # Create the figure representing the target involved
            if target:
                figure_identifier += 1
                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                if type == '(value)':
                    diagram += create_empty_box_2(figure_id, (len(f'{type} {cleaned_property}: &quot;{target}&quot;')) * 6.2, previous_x_axis, y_axis -30)
                    box, target_id, box_width = create_box(figure_identifier, f'{type} {cleaned_property}: &quot;{target}&quot;', previous_x_axis, y_axis)

                else:
                    diagram += create_empty_box_2(figure_id, (len(f'{type} {cleaned_property}: {target}')) * 6.2, previous_x_axis, y_axis -30)
                    box, target_id, box_width = create_box(figure_identifier, f'{type} {cleaned_property}: {target}', previous_x_axis, y_axis)

            else:
                figure_identifier += 1
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                diagram += create_empty_box_2(figure_id, (len(f'{type} {cleaned_property}')) * 6.2, previous_x_axis, y_axis -30)
                box, target_id, box_width = create_box(figure_identifier, f'{type} {cleaned_property}', previous_x_axis, y_axis)
            
            diagram += box

            if anonymous_type == 6 or anonymous_type == 7:
                figure_identifier += 1
                diagram += create_cloud(figure_identifier, "No further chowlk &lt;br&gt;notation", x_axis, y_axis - 30)
                return y_axis
        
        else:
            diagram += create_empty_box_2(figure_id, 60, previous_x_axis, y_axis)

            # Create the figure representing the target involved
            if target:
                figure_identifier += 1
                # In this case a restriction with target is being read (e.g. qualified cardinality restriction, etc)
                if type == '(value)':
                    box, target_id, box_width = create_underlined_box(figure_identifier, target, x_axis, y_axis)

                else:
                    box, target_id, box_width = create_box(figure_identifier, target, x_axis, y_axis)

            else:
                figure_identifier += 1
                # In this case a restriction without target is being read (e.g. cardinality restriction, etc)
                box, target_id, box_width = create_empty_box(figure_identifier, x_axis, y_axis)
            
            diagram += box
    
    if not datatype_property:
        figure_identifier += 1
        # Create the figure representing the property involved
        arrow = create_arrow(figure_identifier, f'{type} {cleaned_property}', figure_id, target_id)
        diagram += arrow
    
    return y_axis

# Function to get the value of the term from the last occurrence of the '|' character.
# Moreover, the whitespaces at the beginning and ending of the string are removed.
def clean_term(term):
    index = term.rfind('|') + 1
    return term[index:].strip()

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