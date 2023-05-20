import rospy
from locobot_simulation.msg import BoundingBoxes,LogicalImage 
import message_filters
from  nav_msgs.msg import Odometry
from rdflib import Graph

import re 
import random


from Ontology.ontology_initialization import add_to_graph
from geometry.distance_angles import euclidean_distance,angle_between_vectors,law_of_cosines

rospy.init_node('listener_bounding_box', anonymous=True)




print("ontology loaded")





def callback(data1,data2,data3):
    #print("Received BoundingBoxes message:")
    x= data3.pose.pose.position.x
    y= data3.pose.pose.position.y
    print(f" robot current location {x,y}")
    g = Graph()
    g.parse("scripts/listeners/Ontology/ontology.ttl", format="turtle")   
    real_camera_bbox=[]
    idetified_objects =[]
    for box in data1.bounding_boxes:
        print("Real cam")
        print(f"  Class: {box.Class}")
        print(f"  Probability: {box.probability}")
        print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")
        real_camera_bbox.append(box.Class)
        idetified_objects.append({"label":box.Class,"identifier":random.randint(0,10000)})

        

    
    for box in data2.models:
       #removes numbers  from string 
        class_name= re.sub(r'[0-9]+', '', box.type)
        class_name= class_name.lower()
        array_of_object=[]
        for identifier in  idetified_objects:
            if(identifier['label']==re.sub(r'[0-9]+', '',box.type).lower()):      
                main_objec_identifier= identifier['identifier']
           
        if(class_name  in real_camera_bbox):
            #for the first model
            distance_from_robot = euclidean_distance([box.pose.position.x,box.pose.position.y,box.pose.position.z])
            u =  [box.pose.position.x,box.pose.position.y,box.pose.position.z]
            for box_model2 in data2.models:
                if(box.type !=box_model2.type and box_model2.type !="cafe" and box.type != "cafe"):
                    v=[box_model2.pose.position.x,box_model2.pose.position.y,box_model2.pose.position.z]
                    box_model2_distance = euclidean_distance([box_model2.pose.position.x,box_model2.pose.position.y,box_model2.pose.position.z])
                    angle  = angle_between_vectors(u,v)
                    
                    print(f" distance between the objects :{box.type} and {box_model2.type} {law_of_cosines(distance_from_robot,box_model2_distance,angle)}")
                    for idetifier  in idetified_objects:
                        if(idetifier['label']==re.sub(r'[0-9]+', '',box_model2.type).lower()):
                            array_of_object.append({"distance":law_of_cosines(distance_from_robot,box_model2_distance,angle),"object_identifier":idetifier["identifier"]})
                        
                    print("Fake Cam")
                #print(f"  Class: {box.type}")
                # print(f"  Coordinate x: ({box.pose.position.x})")
                # print(f"  Coordinate y: ({box.pose.position.y})")
                # print(f"  Coordinate z: ({box.pose.position.z})")

                # distance_from_robot = euclidean_distance([box.pose.position.x,box.pose.position.y,box.pose.position.z])
                # print(f" Distance : ({distance_from_robot})")
                    instace_add = {"label":class_name,"distance_from_robot":distance_from_robot,"distace_from_object":array_of_object,"idetifier":main_objec_identifier}
                    add_to_graph(instace_add,g)
    g.serialize(destination="ontology.ttl", format="turtle")

            
   

odometry_sub =message_filters.Subscriber("/locobot/odom",Odometry)
image_sub = message_filters.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage)
info_sub = message_filters.Subscriber('/yolov5/detections', BoundingBoxes)
ts = message_filters.TimeSynchronizer([info_sub,image_sub,odometry_sub ], 100)
ts.registerCallback(callback)


#rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()

