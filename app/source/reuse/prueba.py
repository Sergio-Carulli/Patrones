import os.path

if __name__ == "__main__":
    file1 = open("D:\\trabajo\\patrones_project\\nombres.txt" , "r", encoding='utf-8')
    line = file1.readline()
    nombres = []
    while(line):
        nombres.append(line.strip())
        line = file1.readline()
    file1.close()

    ontologies = os.listdir('D:\\trabajo\\patrones_project\\misionMaria\\ontologies')

    for ont_name in ontologies:
        # Get the path to the downloaded ontology
        ont_path = os.path.join('D:\\trabajo\\patrones_project\\misionMaria\\ontologies', ont_name)
        file1 = open(ont_path , "r", encoding='utf-8')
        file1_r = file1.read()
        
        for name in nombres:
            if name in file1_r:
                print(f'{name} in {ont_name}')
        
        file1.close()
