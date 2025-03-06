import os
import csv

# Función para examinar si una imagen existe en la ruta 
def image_exists(image_path):
    return os.path.exists(image_path)

# Función para leer datos de un archivo CSV y convertirlos en una lista de diccionarios
def read_csv_file(filename):
    data = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row:
                    pattern_key = row[0].strip()
                    if pattern_key not in data:
                        data[pattern_key] = []
                    data[pattern_key].append(row)
    except FileNotFoundError:
        return "File not found."
    return data

# Función para leer un archivo txt y devolver un diccionario y una lista de las cabeceras
def read_and_process_patterns(filename, csv_data, pattern_type, images_path):
    data = {}
    content=[]
    diagram = ""
    times=""
    ontologies=""
    csv=[]
    value_csv={}
    found_owl_class_section = False
    header_list = []
    ontologiesAppears=""
    keyNameCsv=[]

    try:
        # Check if the file where the patterns are described exists
        if not os.path.exists(filename):
            error_name = "Patterns_type.txt" if pattern_type else "Patterns_name.txt"
            return {"error": f"The file {error_name} does not exist."}, []
        
        # Read the file where the patterns are described
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            # Is the file empty?
            if not content:
                error_name = "Patterns_type.txt" if pattern_type else "Patterns_name.txt"
                return {"error": f"The file {error_name} is empty."}, []
            patterns = content.split("Pattern ")
            if not patterns[0] :
                patterns.pop(0)

            # guardar los datos del txt
            for index, pattern in enumerate(patterns, start=1):
                pattern_key = f"Pattern {index}"
                header_list.append(pattern_key)
                lines = pattern.split('\n')
                found_owl_class_section = False
                diagram=""
                for line in lines:
                    line = line.strip()
                    if line.startswith("Ontologies in which it appears"):
                        ontologiesAppears = line.replace("Ontologies in which it appears","")
                        found_owl_class_section = True
                    elif found_owl_class_section and line:
                        diagram += line + "<br>"
                    elif "Times" in line:
                        times = line;
                    elif "Different ontologies" in line:
                        ontologies= line 
                
            # guardar el texto del csv
                #restaurar variables
                csv=[]
                value_csv={}

                #Separamos por ; y añadimos las claves al diccionario value_csv
                keyNameCsv = ontologiesAppears.split(";")
                for key in keyNameCsv:
                    key = key.strip()
                    if key:
                        value_csv[key] = []

                if pattern_key in csv_data:
                    for csv_row in csv_data[pattern_key]:
                        for structure in csv_row[3:]:
                            aux_structure = structure.split("-")[0]
                            # comprobamos si la stucture:
                            #  está contenida en el nombre de alguna key del diccionario
                            for key in value_csv.keys():
                                # si está contenida metemos la structure como valor de dicha key
                                if aux_structure in key:
                                    value_csv[key].append(structure)
                                    break
                    csv.append(value_csv)
                else:
                    value_csv = {"No data": ["No CSV data found for this pattern."]}

            # Verificar y añadir imagen
                if pattern_type:
                    image_file = f"{pattern_key}.svg"
                    image_path = os.path.join(images_path, image_file)
                    image_file = f'static/images/{image_file}'
                    #image_file = url_for("static", filename=f"images/{image_file}")
                    if not image_exists(image_path):
                        image_file = 'No image available for this pattern.'

            #añadir al diccionario de salida
                if pattern_type:
                    content =[diagram,times,ontologies,csv,image_file]
                    data.update({pattern_key:content})
                else:
                    content =[diagram,times,ontologies,csv]
                    data.update({pattern_key:content})
    except FileNotFoundError:
        error_name = "Patterns_type.txt" if pattern_type else "Patterns_name.txt"
        return {"error": f"The file {error_name} does not exist."}, []

    return data,header_list

# Función para leer Structure Blank Nodes
def read_and_process_file_structure_blank_nodes(filename):
    try:
        if not os.path.exists(filename):
            return {"error": f"The file Structure_term_inferred_blank_nodes.txt does not exist."}
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                return {"error": f"The file Structure_term_inferred_blank_nodes.txt is empty."}
        processed_content = ""
        structure_key = ""
        structure_list = {}
        foundFirstParagraph = False
        foundLineHeader = False

        for line in lines:
            line = line.strip()
            if line.startswith("Ontology"):
                foundFirstParagraph = True
                processed_content = ""
            elif foundFirstParagraph:
                if line.startswith("Structure:"):
                    structure_key = line.split(":")[1].strip()
                    foundLineHeader = True
                elif foundLineHeader and line:
                    processed_content += line + "<br>"
                elif line == "":
                    structure_list.update({structure_key: processed_content})
                    foundFirstParagraph = False
                    foundLineHeader = False
    except FileNotFoundError:
        return {"error": f"The file Structure_term_inferred_blank_nodes.txt does not exist."}
    return structure_list

# Función leer un archivo txt y devolver un diccionario y una lista de las cabeceras
def read_and_process_file_structure(filename, structure_blank_nodes_list):
    try:
        if not os.path.exists(filename):
            return {"error": f"The file {filename} does not exist."}, []
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                return {"error": f"The file {filename} is empty."}, []

        data = {}
        content = []
        ontology_name = ""
        diagram_inferred_type = ""
        header_list = []
        foundFirstParagraph = False
        foundLineHeader = False

        for line in lines:
            line = line.strip()
            if line.startswith("Ontology"):
                ontology_name = line.split(":")[1].strip()
                foundFirstParagraph = True
            elif foundFirstParagraph:
                if line.startswith("Structure:"):
                    structure_key = line.split(":")[1].strip()
                    foundLineHeader = True
                    header_list.append(structure_key)
                elif foundLineHeader and line:
                    diagram_inferred_type += line + "<br>"
                elif line == "":
                    foundFirstParagraph = False
                    foundLineHeader = False
                    if structure_key in structure_blank_nodes_list:
                        blank_nodes_content = structure_blank_nodes_list[structure_key]
                    else:
                        blank_nodes_content = "No data"
                    content = [diagram_inferred_type, blank_nodes_content, ontology_name]
                    data.update({structure_key: content})
                    diagram_inferred_type = ""
    except FileNotFoundError:
        return {"error": f"The file {filename} does not exist."}, []
    return data, header_list