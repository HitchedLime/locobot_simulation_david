from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD

def make_onotology():
    g = Graph()


    ex = Namespace("http://example.org/")


    g.bind("ex", ex)


    g.add((ex.Chair, RDF.type, OWL.Class))
    g.add((ex.Suitcase, RDF.type, OWL.Class))

    # Define the object property
    g.add((ex.next_to, RDF.type, OWL.ObjectProperty))
    g.add((ex.next_to, RDFS.domain, ex.Chair))
    g.add((ex.next_to, RDFS.range, ex.Suitcase))

    # Define the data property
    g.add((ex.coordinates, RDF.type, OWL.DatatypeProperty))
    g.add((ex.coordinates, RDFS.domain, ex.Chair))
    g.add((ex.coordinates, RDFS.range, XSD.string))
    return g 


if __name__ == "__main__":
    g=make_onotology()
    
    print(g.serialize(format="turtle"))




