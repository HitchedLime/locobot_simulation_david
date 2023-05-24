import rdflib

# Create a new rdflib Graph object
g = rdflib.Graph()

# Load the ttl file into the graph object
result = g.parse("/home/david/catkin_ws/src/locobot_simulation_david/scripts/listeners/Ontology/ontology1.ttl", format='ttl')

# Define your SPARQL query
query = """
    PREFIX ex: <http://example.org#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?individual1 ?individual2
    WHERE {
        ?individual1 owl:sameAs ?individual2
    }
"""

# Execute the query against the graph object
results = g.query(query)

# Iterate over the results and print them
for row in results:
    print(row)
