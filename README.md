# Detecting ontologies design patterns

Ontologies are formal knowledge models that describe concepts and relationships and enable data integration, information search, and reasoning. Ontology Design Patterns (ODPs) are reusable solutions intended to simplify ontology development and support the use of semantic technologies by ontology engineers. This work focuses on detecting design patterns in a set of ontologies of the user's choice.

## Description of the tool

1. The user can fill in a csv file with the name and URI of the published ontologies from which the design patterns will be detected. The tool will download these ontologies and store them locally, giving the file the name of the ontology indicated in the csv. This step is optional and can be omitted if the user already has the desired ontologies stored locally.
2. The content of each ontology is extracted by filtering out those terms that are the subject of a triple whose predicate is either "owl:equivalentClass" or "rdfs:subClassOf" and its object is a blank node. These structures are represented as trees in order to emphasize the different components of the blank nodes. The tool will generate two files:
  * A 
3. 

## How to execute the tool

The tool can be executed via the command line as follows:

```bash
app.py [-h] [-ontology ONTOLOGY_PATH] [-csv CSV_PATH] [-patterns {type,name,both}]
```

where:

* ONTOLOGY_PATH is the path to a folder where the ontologies are going to be downloaded. The patterns are going to be identified using the ontologies stored in this folder
* CSV_PATH is the path to the csv file indicating what ontologies are going to be downloaded.
* PATTERNS is a flag to indicate if the patterns are going to be created from the type of the terms or from the name of the terms or from both
