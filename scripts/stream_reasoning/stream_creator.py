#!/usr/bin/env python

import rospy
import rdflib
import cv2
from sensor_msgs.msg import Image
from msg import LogicalImage
from cv_bridge import CvBridge, CvBridgeError

class KnowledgeGraphBuilder:
    def __init__(self):
        # Initialize node
        rospy.init_node('knowledge_graph_builder_node', anonymous=True)

        # Set up subscribers
        rospy.Subscriber('logical_camera', LogicalImage, self.logical_camera_callback)
        rospy.Subscriber('camera/image_raw', Image, self.camera_callback)

        # Set up cv_bridge for image conversion
        self.bridge = CvBridge()

        # Set up RDF graph and namespaces
        self.graph = rdflib.Graph()
        self.owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
        self.rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
        self.owl2rl = rdflib.Namespace("http://www.w3.org/2002/03owlt/rl#")

    def logical_camera_callback(self, data):
        # Extract information from LogicalCameraImage
        for obj in data.models:
            # Create RDF triples for object detection
            subj = rdflib.URIRef('http://example.com/object#' + obj.type)
            pred = self.rdf.type
            obj = self.owl.Thing
            self.graph.add((subj, pred, obj))

            # Add timestamp to RDF graph
            timestamp = rdflib.Literal(rospy.get_time())
            pred = rdflib.URIRef('http://example.com/timestamp')
            self.graph.add((subj, pred, timestamp))

    def camera_callback(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("Error converting Image message: {0}".format(e))
            return

        # Save image to file
        timestamp_str = '{:.6f}'.format(rospy.get_time())
        filename = 'screenshot_{0}.png'.format(timestamp_str)
        cv2.imwrite(filename, cv_image)

        # Add screenshot to RDF graph
        subj = rdflib.URIRef('http://example.com/image#' + timestamp_str)
        pred = self.rdf.type
        obj = rdflib.URIRef('http://xmlns.com/foaf/0.1/Image')
        self.graph.add((subj, pred, obj))

        # Add timestamp to screenshot RDF graph
        timestamp = rdflib.Literal(rospy.get_time())
        pred = rdflib.URIRef('http://example.com/timestamp')
        self.graph.add((subj, pred, timestamp))

        # Link object detection to screenshot in RDF graph
        for subj in self.graph.subjects(self.rdf.type, self.owl.Thing):
            pred = rdflib.URIRef('http://example.com/has_screenshot')
            obj = rdflib.URIRef('http://example.com/image#' + timestamp_str)
            self.graph.add((subj, pred, obj))

if __name__ == '__main__':
   
    pass