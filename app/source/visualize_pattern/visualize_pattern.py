import argparse
from app.source.visualize_pattern.create_diagram import create_diagram

def main(pattern_path):
    create_diagram(pattern_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Visualize an ontology pattern using Chowlk notation')
    parser.add_argument('-pattern', '--pattern_path', 
                        type=str, 
                        help='Path to the file where the patterns are specified')
    
    args = parser.parse_args()
    main(args.pattern_path)