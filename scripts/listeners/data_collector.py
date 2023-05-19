import rospy
from locobot_simulation.msg import BoundingBoxes,LogicalImage 
import message_filters
from  nav_msgs.msg import Odometry
import math
import re 
rospy.init_node('listener_bounding_box', anonymous=True)

object_position =[]


    

def euclidean_distance(array):
    # calculates distance from robot assuming that robot is  at origin every step
    distance = 0
    for value in array:
        distance +=pow(value,2)
        
    return math.sqrt(distance)

def callback(data1,data2,data3):
    #print("Received BoundingBoxes message:")
    x= data3.pose.pose.position.x
    y= data3.pose.pose.position.y
    print(f" robot current location {x,y}")
        
    real_camera_bbox=[]
    for box in data1.bounding_boxes:
        print("Real cam")
        print(f"  Class: {box.Class}")
        print(f"  Probability: {box.probability}")
        print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")
        real_camera_bbox.append(box.Class)
        

    
    for box in data2.models:
       #removes numbers  from string 
        class_name= re.sub(r'[0-9]+', '', box.type)
        class_name= class_name.lower()
        
        if(class_name  in real_camera_bbox):
            print("Fake Cam")
            print(f"  Class: {box.type}")
            # print(f"  Coordinate x: ({box.pose.position.x})")
            # print(f"  Coordinate y: ({box.pose.position.y})")
            # print(f"  Coordinate z: ({box.pose.position.z})")
            distance = euclidean_distance([box.pose.position.x,box.pose.position.y,box.pose.position.z])
            print(f" Distance : ({distance})")
            object_position.append((class_name.lower(),distance))
   

odometry_sub =message_filters.Subscriber("/locobot/odom",Odometry)
image_sub = message_filters.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage)
info_sub = message_filters.Subscriber('/yolov5/detections', BoundingBoxes)
ts = message_filters.TimeSynchronizer([info_sub,image_sub,odometry_sub ], 100)
ts.registerCallback(callback)


#rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()

