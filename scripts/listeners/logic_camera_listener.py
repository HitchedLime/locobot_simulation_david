import rospy
from locobot_simulation.msg import BoundingBoxes,LogicalImage

from geometry_msgs.msg import Twist 
import message_filters
rospy.init_node('listener_bounding_box', anonymous=True)
def callback(data1,data2):
    print("Received BoundingBoxes message:")
   # print(data2.pose.position)
    print(data2.models[0])
    for box in data1.bounding_boxes:
        print(f"  Class: {box.Class}")
        print(f"  Probability: {box.probability}")
        print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")



image_sub = message_filters.Subscriber('/gazebo/locobot/camera/logical_camera_image', LogicalImage)
info_sub = message_filters.Subscriber('/yolov5/detections', BoundingBoxes)
ts = message_filters.TimeSynchronizer([info_sub,image_sub ], 10)
ts.registerCallback(callback)


#rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()

