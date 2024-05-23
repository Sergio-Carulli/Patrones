# Detecting ontologies design patterns

Ontologies are formal knowledge models that describe concepts and relationships and enable data integration, information search, and reasoning. Ontology Design Patterns (ODPs) are reusable solutions intended to simplify ontology development and support the use of semantic technologies by ontology engineers. This work focuses on detecting design patterns in a set of ontologies of the user's choice.

## Description of the tool

1. The user can fill in a csv file with the name and URI of the published ontologies from which the design patterns will be detected. The tool will download these ontologies and store them locally, giving the file the name of the ontology indicated in the csv. This step is optional and can be omitted if the user already has the desired ontologies stored locally.
2. The content of each ontology is extracted by filtering out those terms that are the subject of a triple whose predicate is either "owl:equivalentClass", "rdfs:subClassOf" or "owl:disjointWith" and its object is a blank node. These structures are represented as trees in order to emphasize the different components of the blank nodes. The tool will generate two files:
  * Structure_term_name: A file where the term URIs are specified.
  * Structure_term_type: A file where the type of the terms are specified instead of their URIs.
3. Sometimes the type of a term can not be specified due to different errors in the ontology:
  * The term is defined in the ontology but the owner has not specified a type.
  * The term is a reused term but the origin ontology could not be loaded.
  * The term is a reused term and the origin ontology could be loaded, but the owner has not specified a type.
  In these cases the types is #Unknwon. However, in order to maintain the maximum number of useful structures the following inferences are applied:
  * Restrictions: In the restrictions there are two key elements (the property and the type of the restriction). If one of these key elements is not #Unknown, the type of the other element can be infer.
  * Intersection and union of classes: The elements involved in an intersection or union must be classes. Blank nodes are always recognized, because they have to be defined in the ontology. Therefhore, the type of the terms, which have been identified as #Unknwon, inside an intersection or union or classes must be named classes (owl:Class).
  * Complement class: The element involved in a complement must be a class. Blank nodes are always recognized, because they have to be defined in the ontology. Therefhore, the type of the term, which have been identified as #Unknwon, inside a complement must be named classes (owl:Class).
  * Enumeration: The elements involved in an enumeration can be either individuals or data values. Data values are always recognized as "Data value". Therefhore, the type of the term, which have been identified as #Unknwon, inside a oneOf must be named individuals (owl:NamedIndividual).
  Moreover, in some cases the type of a blank node can not be specified due to there is not an explicit declaration of the blank node. In these cases the type is #Blank node. However, in order to maintain the maximum number of useful structures the blank node type is inferred.
  The structures resulting from applying the inference process explained above are written in a file called Structure_term_inferred_type and Structure_term_inferred_blank_nodes.
4. Finally, patterns are identified through finding equals structures. The only condition for identifying a pattern is that there are at least two structures with the same content. The tool will generate two files:
  * Patterns_name: A file which contains the patterns which have been found through the Structure_term_inferred_blank_nodes.
  * Patterns_type: A file which contains the patterns which have been found through the Structure_term_inferred_type file.

## How to execute the tool

The tool can be executed via the command line as follows:

```bash
app.py [-h] [-ontology ONTOLOGY_PATH] [-csv CSV_PATH] [-output OUTPUT_PATH] [-patterns {type,name,both}] [-flatten {yes,no}]
```

where:

* ONTOLOGY_PATH is the path to a folder where the ontologies are going to be downloaded. The patterns are going to be identified using the ontologies stored in this folder
* CSV_PATH is the path to the csv file indicating what ontologies are going to be downloaded. This parameter is optional. If this parameter is not specified, it is assumed that the ontologies are already downloaded and are located in ONTOLOGY_PATH.
* OUTPUT_PATH is the path a folder where the output is going to be stored. This parameter is optional. If this parameter is not specified, it is assumed that the output is going to be stored in the current directory.
* PATTERNS is a flag to indicate if the patterns are going to be created from the type of the terms or from the name of the terms or from both. This parameter is optional. By default the patterns are going to be creaded just by the type of the terms.
* FLATTEN is a flag to indicate if the collections are going to be flattened if they only contain named classes. This parameter is optional. By default the collections are not going to be flattened.
