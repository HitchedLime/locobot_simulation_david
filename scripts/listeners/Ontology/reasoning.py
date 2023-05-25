from owlready2 import *
from rdflib import Graph

# Create a new RDF graph
g = Graph()

# # Parse the RDF data from the Turtle file
g.parse("/home/david/catkin_ws/src/locobot_simulation_david/scripts/listeners/Ontology/ontology1.ttl", format="turtle")

# # Serialize the RDF graph as an OWL ontology in RDF/XML format and save it to a file
 
g.serialize("/home/david/catkin_ws/src/locobot_simulation_david/scripts/listeners/Ontology/output.owl", format="pretty-xml")

# # Set the path to your local ontology repository
onto_path.append("scripts/listeners/Ontology/")

# Load an ontology from a local repository or from the internet
onto = get_ontology("scripts/listeners/Ontology/output.owl")
onto.load()

# Define the ex namespace prefix
ex = onto.get_namespace("http://example.org/")
owl = onto.get_namespace("http://www.w3.org/2002/07/owl")
rdf = onto.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns")
rdfs = onto.get_namespace("http://www.w3.org/2000/01/rdf-schema")
xsd = onto.get_namespace("http://www.w3.org/2001/XMLSchema")


with onto:

# Define your SWRL rule using the owlready2 Imp class
    rule = Imp(namespace=ex)
    rule.set_as_rule("hasPoint(?individual1, ?point), hasPoint(?individual2, ?point), differentFrom(?individual1, ?individual2) -> sameAs(?individual1, ?individual2)")






    # Perform reasoning using the  reasoner
    sync_reasoner(infer_property_values = True)

    
    query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?individual
WHERE {
    ?individual rdf:type/rdfs:subClassOf* <http://example.org/Chair> .
}
"""
    x =list(default_world.sparql(query))
    print(x)

onto.save(file="changed", format="rdfxml")
