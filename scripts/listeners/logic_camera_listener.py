import rospy
from locobot_simulation.msg import BoundingBoxes

def callback(data):
    print("Received BoundingBoxes message:")
    for box in data.bounding_boxes:
        print(f"  Class: {box.Class}")
        print(f"  Probability: {box.probability}")
        print(f"  Coordinates: ({box.xmin}, {box.ymin}) - ({box.xmax}, {box.ymax})")

rospy.init_node('listener', anonymous=True)
rospy.Subscriber('/yolov5/detections', BoundingBoxes, callback)
rospy.spin()