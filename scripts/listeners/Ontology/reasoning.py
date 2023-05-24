from owlready2 import *

# Set the path to your local ontology repository
#onto_path.append("/path/to/your/local/ontology/repository")

# Load an ontology from a local repository or from the internet
onto = get_ontology("http://www.lesfleursdunormal.fr/static/_downloads/pizza_onto.owl")
onto.load()

# Perform reasoning using the HermiT reasoner
sync_reasoner()

# Access the inferred facts and relationships
for instance in onto.instances():
    print(f"{instance} is a {instance.__class__}"