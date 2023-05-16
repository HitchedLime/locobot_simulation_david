import rospy
from locobot_simulation.msg import BoundingBoxes,LogicalImage 
import message_filters

import math
import re 
rospy.init_node('listener_bounding_box', anonymous=True)

def euclidean_distance(array):
    # calculates distance from robot assuming that robot is  at origin every step
    distance = 0
    for value in array:
        distance +=pow(value,2)
        
    return math.sqrt(distance)

def callback(data1,data2):
    print("Received BoundingBoxes message:")
    real_camera_bbox=[]
    for box in data1.bounding_boxes:
        print(f"  Class: {box.Class}")
        print(f"  Probability: {box.probability}")
        print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")
        real_camera_bbox.append(box.Class)
        print("Real cam")

    
    for box in data2.models:
       #removes numbers  from string 
        class_name= re.sub(r'[0-9]+', '', box.type)
       
        if(class_name.lower()  in real_camera_bbox):
            print("Fake Cam")
            print(f"  Class: {box.type}")
            print(f"  Coordinate x: ({box.pose.position.x})")
            print(f"  Coordinate y: ({box.pose.position.y})")
            print(f"  Coordinate z: ({box.pose.position.z})")
            distance = euclidean_distance([box.pose.position.x,box.pose.position.y,box.pose.position.z])
            print(f" Distance : ({distance})")
   


image_sub = message_filters.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage)
info_sub = message_filters.Subscriber('/yolov5/detections', BoundingBoxes)
ts = message_filters.TimeSynchronizer([info_sub,image_sub ], 10)
ts.registerCallback(callback)


#rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()

