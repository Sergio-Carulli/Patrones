from create_diagram_element import create_box
from create_diagram_element import create_arrow
from create_diagram_element import create_empty_box

# Global variable to store the content of the XML file
diagram = ''

# Function to create the XML diagram where the patterns are going to be visualizated
def create_diagram(pattern_path):
        generate_XML_headers()

        # Open the file with the detected patterns
        pattern_file = open(pattern_path , "r", encoding='utf-8')

        # Read the first pattern
        pattern = read_pattern(pattern_file)

        # Iterate while there is at least one pattern unread
        while(len(pattern) > 0):
            print(pattern)
            visualize_pattern(pattern)
            # Read a new pattern
            pattern = read_pattern(pattern_file)
        print(pattern)

        # Close the csv file
        pattern_file.close()

        generate_footers()

        f = open('Visualization.xml', 'w', encoding='utf-8')
        f.write(diagram)
        f.close()
        """try:
            generate_XML_headers()
            namespaces_width, namespaces_height = generate_namespaces(namespaces)
            metadata_height = generate_metadata(g, namespaces_width)

            first_y = max(namespaces_height, metadata_height) + 80

            first_x = generate_classes_hierarchy(g, first_y)
            first_x = generate_object_properties(g, first_y, first_x)
            generate_datatype_properties_2(g, first_y, first_x)
            #generate_datatype_properties(g, first_y, first_x)
            generate_footers()

            f = open(output_path, 'w', encoding='utf-8')
            f.write(diagram)
            f.close()
        except Exception as error:
            print(f"Error: {error}")
            traceback.print_exc()"""

# Function to parse just one pattern into a list
# Different patterns are separated by blank lines        
def read_pattern(pattern_file):
    # List that will store each line of the pattern being read
    pattern = []

    # Skip the first four lines of the pattern (these lines just contain metadata)
    pattern_file.readline()
    pattern_file.readline()
    pattern_file.readline()
    pattern_file.readline()

    # Read fifth line (already contains pattern data)
    line = pattern_file.readline()

    # Iterate the lines of the TXT file
    while(line):

        # Is a pattern line being read?
        if len(line) > 1:
            # Add structure line
            pattern.append(line)

        else:
            # In this case a blank line is being read, i.e. the end of the pattern has been reached
            break

        # Read a new line
        line = pattern_file.readline()
    
    return pattern

def visualize_pattern(pattern):
    global diagram
    width, figure_id = visualize_beggining(clean_term(pattern[0].strip()), clean_term(pattern[1].strip()), clean_term(pattern[2].strip()))
    
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
            index = iterate_restriction(index + 1, pattern, pattern_len, deep, figure_id)
        
        else:
            # Get the next line
            index += 1

    return

def visualize_beggining(subject, predicate, object):
    global diagram
    box, box_id, box_width = create_box(subject, 0, 0)
    width = len(predicate) * 8 + box_width

    if 'owl:Restriction' in object:
        box2, box2_id, box2_width = create_empty_box(width, 0)
        width += box2_width
        arrow = create_arrow(predicate, box_id, box2_id)
        diagram += f'{box}{box2}{arrow}'

    return width, box2_id

def iterate_restriction(index, pattern, pattern_len, father_deep, figure_id):
    # Variable to store the type of a property involved in a resctriction
    property = ''
    # Variable to store the type of the target involved in a resctriction
    target = ''
    # Variable to store the type of the resctriction
    type = ''

    # Iterate the structure
    while index < pattern_len:
        # Read a line of the structure
        line = pattern[index]
        # Get the deep of the line (the number of "  |")
        deep = get_deep(line)

        # Is the line outside the restriction?
        if deep <= father_deep:
            # Visualizate the restriction
            visualize_restriction()
            # Return the position where the restriction ends
            return index

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
                type = '(some)'
            
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
        
        else:

            # Does the line represents the beggining of a restriction?
            if 'owl:Restriction' in line:
                # Get the line where the restriction ends
                # index = iterate_restriction(index + 1, pattern, pattern_len, deep)
                index += 1
            
            else:
                # Get the position of the next line
                index += 1

    # In this case we have reached the end of the structure
    # Infer the "Unknown" types
    visualize_restriction()
    # Return a number which is greater than the number of lines in the list
    return index

def visualize_restriction():
    return

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