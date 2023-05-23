import rospy
from locobot_simulation.msg import BoundingBoxes,LogicalImage 
import message_filters
from  nav_msgs.msg import Odometry
from rdflib import Graph
from gazebo_msgs.msg import ModelStates
import re 
import random


from Ontology.ontology_initialization import add_to_graph
from geometry.distance_angles import euclidean_distance,angle_between_vectors,law_of_cosines,third_point

rospy.init_node('listener_bounding_box', anonymous=True)



data1=[]
data2=[]
data3=[]

def callback3(data):
    global data3
    #print(f"Data 3 ")
    data3.append(data)


   
       

def callback2(data):
    global data2
    #print(f"Data 2 ")
    data2.append(data)

def callback1(data):
    global data1
    #print(f"Data 1 ")
    data1.append(data)
    callback(data1,data2,data3)
    

def callback(data_yolo,data_logic,data_odo):
    
    if(data_yolo and data_logic and data_odo ):
       # print("Received BoundingBoxes message:")
        data1=data_yolo[-1]
        data2=data_logic[-1]
        data3=data_odo[-1]
        x= data3.pose.pose.position.x
        y= data3.pose.pose.position.y
        # print(f" robot current location {x,y}")
        g = Graph()
        g.parse("scripts/listeners/Ontology/ontology1.ttl", format="turtle")   
        real_camera_bbox=[]
        idetified_objects =[]
        for box in data1.bounding_boxes:
            # print("Real cam")
            # print(f"  Class: {box.Class}")
            # print(f"  Probability: {box.probability}")
            # print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")
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
                        
                       # print(f" distance between the objects :{box.type} and {box_model2.type} {law_of_cosines(distance_from_robot,box_model2_distance,angle)}")
                        for idetifier  in idetified_objects:
                            if(idetifier['label']==re.sub(r'[0-9]+', '',box_model2.type).lower()):
                                array_of_object.append({"distance":law_of_cosines(distance_from_robot,box_model2_distance,angle),"object_identifier":idetifier["identifier"]})
                            
                       # print("Fake Cam")
                    #print(f"  Class: {box.type}")
                    # print(f"  Coordinate x: ({box.pose.position.x})")
                    # print(f"  Coordinate y: ({box.pose.position.y})")
                    # print(f"  Coordinate z: ({box.pose.position.z})")

                    # distance_from_robot = euclidean_distance([box.pose.position.x,box.pose.position.y,box.pose.position.z])
                    # print(f" Distance : ({distance_from_robot})")
                        instace_add = {"label":class_name,"distace_from_object":array_of_object,"idetifier":main_objec_identifier,"position":third_point(x,y,0,0,euclidean_distance([box_model2.pose.position.x,box_model2.pose.position.y]))}
                        add_to_graph(instace_add,g)
        g.serialize(destination="scripts/listeners/Ontology/ontology1.ttl", format="turtle")

            
            
   

# odometry_sub =message_filters.Subscriber("/locobot/odom",Odometry)
# image_sub = message_filters.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage)
# info_sub = message_filters.Subscriber('/yolov5/detections', BoundingBoxes)
# ts = message_filters.TimeSynchronizer([info_sub,image_sub,odometry_sub], 10)
# ts.registerCallback(callback)

def cb_once(data):
    for i in range(len(data.name)):
        model_name = data.name[i]
        model_pose = data.pose[i]
        model_twist = data.twist[i]
        print(model_name)
        # access position and orientation from pose
        x = model_pose.position.x
        y = model_pose.position.y
        z = model_pose.position.z
    sub_once .unregister()

global sub_once 
sub_once = rospy.Subscriber('/gazebo/model_states', ModelStates, cb_once)




odometry_sub =rospy.Subscriber("/locobot/odom",Odometry,callback3)
image_sub = rospy.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage,callback2)
info_sub = rospy.Subscriber('/yolov5/detections', BoundingBoxes,callback1)

#callback(data1,data2,data3)
#rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()

