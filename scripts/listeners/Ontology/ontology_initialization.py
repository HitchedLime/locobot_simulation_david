from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import random

def add_to_graph(data :dict,g:Graph )-> None:
    """
    Parameter:  adds data to graph 

    """

    match = [{"supercategory": "person", "id": 1, "name": "person"}, {"supercategory": "vehicle", "id": 2, "name": "bicycle"}, {"supercategory": "vehicle", "id": 3, "name": "car"}, {"supercategory": "vehicle", "id": 4, "name": "motorcycle"}, {"supercategory": "vehicle", "id": 5, "name": "airplane"}, {"supercategory": "vehicle", "id": 6, "name": "bus"}, {"supercategory": "vehicle", "id": 7, "name": "train"}, {"supercategory": "vehicle", "id": 8, "name": "truck"}, {"supercategory": "vehicle", "id": 9, "name": "boat"}, {"supercategory": "outdoor", "id": 10, "name": "traffic light"}, {"supercategory": "outdoor", "id": 11, "name": "fire hydrant"}, {"supercategory": "outdoor", "id": 13, "name": "stop sign"}, {"supercategory": "outdoor", "id": 14, "name": "parking meter"}, {"supercategory": "outdoor", "id": 15, "name": "bench"}, {"supercategory": "animal", "id": 16, "name": "bird"}, {"supercategory": "animal", "id": 17, "name": "cat"}, {"supercategory": "animal", "id": 18, "name": "dog"}, {"supercategory": "animal", "id": 19, "name": "horse"}, {"supercategory": "animal", "id": 20, "name": "sheep"}, {"supercategory": "animal", "id": 21, "name": "cow"}, {"supercategory": "animal", "id": 22, "name": "elephant"}, {"supercategory": "animal", "id": 23, "name": "bear"}, {"supercategory": "animal", "id": 24, "name": "zebra"}, {"supercategory": "animal", "id": 25, "name": "giraffe"}, {"supercategory": "accessory", "id": 27, "name": "backpack"}, {"supercategory": "accessory", "id": 28, "name": "umbrella"}, {"supercategory": "accessory", "id": 31, "name": "handbag"}, {"supercategory": "accessory", "id": 32, "name": "tie"}, {"supercategory": "accessory", "id": 33, "name": "suitcase"}, {"supercategory": "sports", "id": 34, "name": "frisbee"}, {"supercategory": "sports", "id": 35, "name": "skis"}, {"supercategory": "sports", "id": 36, "name": "snowboard"}, {"supercategory": "sports", "id": 37, "name": "sports ball"}, {"supercategory": "sports", "id": 38, "name": "kite"}, {"supercategory": "sports", "id": 39, "name": "baseball bat"}, {"supercategory": "sports", "id": 40, "name": "baseball glove"}, {"supercategory": "sports", "id": 41, "name": "skateboard"}, {"supercategory": "sports", "id": 42, "name": "surfboard"}, {"supercategory": "sports", "id": 43, "name": "tennis racket"}, {"supercategory": "kitchen", "id": 44, "name": "bottle"}, {"supercategory": "kitchen", "id": 46, "name": "wine glass"}, {"supercategory": "kitchen", "id": 47, "name": "cup"}, {"supercategory": "kitchen", "id": 48, "name": "fork"}, {"supercategory": "kitchen", "id": 49, "name": "knife"}, {"supercategory": "kitchen", "id": 50, "name": "spoon"}, {"supercategory": "kitchen", "id": 51, "name": "bowl"}, {"supercategory": "food", "id": 52, "name": "banana"}, {"supercategory": "food", "id": 53, "name": "apple"}, {"supercategory": "food", "id": 54, "name": "sandwich"}, {"supercategory": "food", "id": 55, "name": "orange"}, {"supercategory": "food", "id": 56, "name": "broccoli"}, {"supercategory": "food", "id": 57, "name": "carrot"}, {"supercategory": "food", "id": 58, "name": "hot dog"}, {"supercategory": "food", "id": 59, "name": "pizza"}, {"supercategory": "food", "id": 60, "name": "donut"}, {"supercategory": "food", "id": 61, "name": "cake"}, {"supercategory": "furniture", "id": 62, "name": "chair"}, {"supercategory": "furniture", "id": 63, "name": "couch"}, {"supercategory": "furniture", "id": 64, "name": "potted plant"}, {"supercategory": "furniture", "id": 65, "name": "bed"}, {"supercategory": "furniture", "id": 67, "name": "dining table"}, {"supercategory": "furniture", "id": 70, "name": "toilet"}, {"supercategory": "electronic", "id": 72, "name": "tv"}, {"supercategory": "electronic", "id": 73, "name": "laptop"}, {"supercategory": "electronic", "id": 74, "name": "mouse"}, {"supercategory": "electronic", "id": 75, "name": "remote"}, {"supercategory": "electronic", "id": 76, "name": "keyboard"}, {"supercategory": "electronic", "id": 77, "name": "cell phone"}, {"supercategory": "appliance", "id": 78, "name": "microwave"}, {"supercategory": "appliance", "id": 79, "name": "oven"}, {"supercategory": "appliance", "id": 80, "name": "toaster"}, {"supercategory": "appliance", "id": 81, "name": "sink"}, {"supercategory": "appliance", "id": 82, "name": "refrigerator"}, {"supercategory": "indoor", "id": 84, "name": "book"}, {"supercategory": "indoor", "id": 85, "name": "clock"}, {"supercategory": "indoor", "id": 86, "name": "vase"}, {"supercategory": "indoor", "id": 87, "name": "scissors"}, {"supercategory": "indoor", "id": 88, "name": "teddy bear"}, {"supercategory": "indoor", "id": 89, "name": "hair drier"}, {"supercategory": "indoor", "id": 90, "name": "toothbrush"}]
    for  dictionary in  match:
        if(dictionary['name']== data['label']):
            identifier_name= random.randint(0,100000)

            item = ex[f"{dictionary['name']}{identifier_name}"]
            x,y =data['position']
            point=ex[f"point{identifier_name}"]
            g.add((item, RDF.type, ex[f"{dictionary['name'].capitalize()}"]))
           
            
            
            g.add((item, ex.hasX, Literal(float(x))))
            g.add((item, ex.hasY, Literal(float(y))))
            g.add((item, ex.hasDistance, Literal(0)))
            g.add((item, ex.hasIdentifier, Literal(str(data['idetifier']))))
            
    #g.serialize("output.owl", format="xml")
    print(g.serialize(format="turtle"))


from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Define namespaces
ex = Namespace("http://example.org/")

# Create a new graph

g = Graph()
g.bind("ex", ex)
g.bind("owl", OWL)
# Define the "Chair" class
g.add((ex.Chair, RDF.type, OWL.Class))
g.add((ex.Suitcase, RDF.type, OWL.Class))

# Define the "Point" class
# g.add((ex.Point, RDF.type, RDFS.Class))

# # Define the "x" and "y" properties
# g.add((ex.x, RDF.type, RDF.Property))
# g.add((ex.x, RDFS.domain, ex.Point))
# g.add((ex.x, RDFS.range, XSD.double))

# g.add((ex.y, RDF.type, RDF.Property))
# g.add((ex.y, RDFS.domain, ex.Point))
# g.add((ex.y, RDFS.range, XSD.double))

# Define the "hasPoint" data property


g.add((ex.hasY, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasY, RDFS.domain, ex.Chair))
g.add((ex.hasY, RDFS.domain, ex.Suitcase))
g.add((ex.hasY, RDFS.range, XSD.double))


g.add((ex.hasX, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasX, RDFS.domain, ex.Chair))
g.add((ex.hasX, RDFS.domain, ex.Suitcase))
g.add((ex.hasX, RDFS.range, XSD.double))

# Define the "hasIdentifier" data property
g.add((ex.hasIdentifier, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasIdentifier, RDFS.domain, ex.Chair))
g.add((ex.hasIdentifier, RDFS.domain, ex.Suitcase))
g.add((ex.hasIdentifier, RDFS.range, XSD.string))

# Define the "hasDistance" data property
g.add((ex.hasDistance, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasDistance, RDFS.domain, ex.Chair))
g.add((ex.hasDistance, RDFS.domain, ex.Suitcase))
g.add((ex.hasDistance, RDFS.range, XSD.integer))





my_chair = URIRef("http://example.org/myChair")
g.add((my_chair, RDF.type, ex.Chair))
g.add((my_chair, ex.hasDistance, Literal(5)))
g.add((my_chair, ex.hasIdentifier, Literal("chair")))
my_point = URIRef("http://example.org/myPoint")

g.add((my_chair,ex.hasX,Literal(69)))
g.add((my_chair,ex.hasY,Literal(420)))
# Associate the Chair instance with the Point instance
g.add((my_chair, ex.hasPoint, my_point))

if __name__ == "__main__":
    
    namespaces = list(g.namespaces())
    
    g.serialize(destination="ontology.ttl", format="turtle")


    
 

    print(g.serialize(format="turtle"))




