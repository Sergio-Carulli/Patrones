import os
from flask import Flask, render_template
from app.source.generateFrontElements.utilities import read_csv_file, read_and_process_patterns,read_and_process_file_structure,read_and_process_file_structure_blank_nodes

app = Flask(__name__)

# Function to create the CSS file in the path specified by the user
def generate_style(styles_path):
    cwd = os.getcwd()
    # Path where the CSS template is located
    css_path = os.path.join(cwd, 'app', 'source', 'generateFrontElements', 'templates', 'main.css')
    # Path specified by the user where the CSS file is going to be generated
    main_path = os.path.join(styles_path, 'main.css')

    # Copy the CSS template into the path specified by the user
    style_file = open(main_path , "w", encoding='utf-8')
    with open(css_path) as css_file:
        style_file.write(css_file.read())
    style_file.close()

# Function to creathe the PatternType.html file in the path specified by the user.
# This HTML file contains:
#   - The patterns stored in the Patterns_type.txt file
#   - For each pattern, a SVG file is displayed with the representation of the pattern
#   - For each pattern, the structures used for detected a pattern, which are stored in the Structure_term_inferred_blank_nodes.txt file, are displayed
def generate_pattern_type_html(patterns_type_path, inferred_blank_nodes_path, images_path, html_path):
    # Path to the CSV file where the patterns type metadata are stored
    csv_type_data = read_csv_file(f'{patterns_type_path}.csv')
    # en el caso de patetrns_name se llama con False
    pattern_content_type, header_list = read_and_process_patterns(f'{patterns_type_path}.txt', csv_type_data, True, images_path)
    content_blank_nodes = read_and_process_file_structure_blank_nodes(inferred_blank_nodes_path)
    
    with app.app_context():
        if "error" in pattern_content_type:
            content = render_template('PatternType.html', pattern_content_type = {}, header_list = [], content_blank_nodes = {}, error_message = pattern_content_type["error"], error_message_structure = None)
        elif "error" in content_blank_nodes:
            content = render_template('PatternType.html', pattern_content_type = pattern_content_type, header_list = header_list, content_blank_nodes = {}, error_message = None, error_message_structure = content_blank_nodes["error"])
        else:
            content = render_template('PatternType.html', pattern_content_type = pattern_content_type, header_list = header_list, content_blank_nodes = content_blank_nodes, error_message = None, error_message_structure = None)

    pattern_file = open(os.path.join(html_path, 'PatternType.html') , "w", encoding='utf-8')

    pattern_file.write(content)

    pattern_file.close()

def generate_pattern_name_html(patterns_name_path, html_path):
    csv_name_data = read_csv_file(f'{patterns_name_path}.csv')
    pattern_content_name, header_list = read_and_process_patterns(f'{patterns_name_path}.txt', csv_name_data, False, None)
    
    with app.app_context():
        if "error" in pattern_content_name:
            content = render_template('PatternName.html', pattern_content_name = {}, header_list = [], error_message = pattern_content_name["error"])
        else:
            content = render_template('PatternName.html', pattern_content_name = pattern_content_name, header_list = header_list, error_message = None)

    pattern_file = open(os.path.join(html_path, 'PatternName.html') , "w", encoding='utf-8')

    pattern_file.write(content)

    pattern_file.close()

def generate_structures_html(inferred_blank_nodes_path, inferred_type_path, html_path):
    content_blank_nodes = read_and_process_file_structure_blank_nodes(inferred_blank_nodes_path)
        
    with app.app_context():
        if "error" in content_blank_nodes:
            content = render_template('Structure.html', error_message = content_blank_nodes["error"], content_blank_nodes = {}, content_type = {}, header_list = [])
        else:
            content_type, header_list = read_and_process_file_structure(inferred_type_path, content_blank_nodes)
            if "error" in content_type:
                content = render_template('Structure.html', error_message = content_type["error"], content_blank_nodes = content_blank_nodes, content_type = {}, header_list = [])
            else:
                content = render_template('Structure.html', content_type = content_type, content_blank_nodes = content_blank_nodes, header_list = header_list, error_message = None)

    pattern_file = open(os.path.join(html_path, 'Structure.html') , "w", encoding='utf-8')

    pattern_file.write(content)

    pattern_file.close()

# Function to create the web documentation in the patch specified by the user
def generate_documentation(styles_path, patterns_type_path, inferred_blank_nodes_path, images_path, html_path, patterns_name_path, inferred_type_path):
    # Generate CSS file
    generate_style(styles_path)
    # Generate PatternType.html
    generate_pattern_type_html(patterns_type_path, inferred_blank_nodes_path, images_path, html_path)
    # Generate PatternName.html
    generate_pattern_name_html(patterns_name_path, html_path)
    # Generate Structure.html
    generate_structures_html(inferred_blank_nodes_path, inferred_type_path, html_path)