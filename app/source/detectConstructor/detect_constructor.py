import argparse
import re

# Dictionary whose:
#   - key: constructor detected in the file
#   - value: number of ocurrences of that constructor
constructors = {}

def main(structure_path):
    pattern_file = open(structure_path , "r", encoding='utf-8')
    line = pattern_file.readline()
    
    # Iterate until the end of the file
    while(line):
        # Skips the first two lines of the pattern
        pattern_file.readline()
        pattern_file.readline()
        line = pattern_file.readline()
        while(len(line) > 1):
            x = re.findall("owl:(\w*)", line)

            for y in x:
                if f'owl:{y}' in constructors:
                    constructors[f'owl:{y}'] += 1
                
                else:
                    constructors[f'owl:{y}'] = 1
            
            x = re.findall("rdfs:(\w*)", line)

            for y in x:
                if f'rdfs:{y}' in constructors:
                    constructors[f'rdfs:{y}'] += 1
                
                else:
                    constructors[f'rdfs:{y}'] = 1

            line = pattern_file.readline()
        
    print(constructors)
    pattern_file.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Detect what constructors are used in the structures')
    parser.add_argument('-structure', '--structure_path', 
                        type=str, 
                        help='Path to the file where the structures are specified')
    
    args = parser.parse_args()
    main(args.structure_path)