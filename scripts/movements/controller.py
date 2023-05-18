
import rospy 
from  nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion
import math 
import numpy as np
rospy.init_node("controller")
x=0
y=0
theta =0
def callback(data):
    global x 
    global y 
    global theta
    x= data.pose.pose.position.x
    y= data.pose.pose.position.y
    rotation = data.pose.pose.orientation
    (_,_,theta) = euler_from_quaternion([rotation.x,rotation.y,rotation.z,rotation.w])

speed =Twist()
sub = rospy.Subscriber("/locobot/odom",Odometry,callback)
pub = rospy.Publisher('/locobot/mobile_base/commands/velocity', Twist, queue_size=1)
rate = rospy.Rate(10)
goal = Point()
goal.x = 6
goal.y = 0
while not rospy.is_shutdown():
    

    distace_x  = goal.x - x
    distace_y  = goal.y - y

    distance_to_goal = np.sqrt(distace_x*distace_x + distace_y *distace_y )
    if (distance_to_goal >= 1.5):
        print(f"Distance to goal {distance_to_goal}")

    # how much is robot steering away
        angle_goal = math.atan2(distace_y,distace_x)
        if (abs(angle_goal-theta)>0.1):
            
          #  print("Looking for goal ...")
            speed.linear.x = 0.0
            speed.angular.z = 0.3
        else:
          #  print("Goal found !")
            speed.linear.x = 0.4
            speed.angular.z = 0.0
    else:
        speed.linear.x = 0.0
        speed.angular.z = 0.0
        
        
       

    
    pub.publish(speed)
    rate.sleep()
   
