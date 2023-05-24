from owlready2 import *




from rdflib import Graph

# Create a new RDF graph
g = Graph()

# Parse the RDF data from the Turtle file
g.parse("/home/david/catkin_ws/src/locobot_simulation_david/scripts/listeners/Ontology/ontology1.ttl", format="turtle")

# Serialize the RDF graph as an OWL ontology in RDF/XML format and save it to a file
g.serialize("/home/david/catkin_ws/src/locobot_simulation_david/scripts/listeners/Ontology/output.owl", format="pretty-xml")

# Set the path to your local ontology repository
onto_path.append("scripts/listeners/Ontology/")

# Load an ontology from a local repository or from the internet
onto = get_ontology("scripts/listeners/Ontology/output.owl")
onto.load()

# Perform reasoning using the HermiT reasoner
sync_reasoner(infer_property_values = True, infer_data_property_values = True)

# Access the inferred facts and relationships


