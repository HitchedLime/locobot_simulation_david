
import rospy 
from  nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion
import math 
import numpy as np

rospy.init_node("controller",disable_signals=True)
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
tilt_publisher = rospy.Publisher('/locobot/tilt_controller/command', Float64, queue_size=10)
pan_publisher = rospy.Publisher('/locobot/pan_controller/command', Float64, queue_size=10)
rate = rospy.Rate(10)
goal = Point()
goal.x = 5.5+1.5
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
            tilt_publisher.publish(0.0)
            pan_publisher.publish(-0.75)
        else:
          #  print("Goal found !")
            speed.linear.x = 0.00009
            speed.angular.z = 0.0
            tilt_publisher.publish(0.0)
            pan_publisher.publish(-0.75)
    else:
        
        speed.linear.x = 0.0
        speed.angular.z = -0.4
        tilt_publisher.publish(0.0)
        
        
        
        
        
        
        
       

    
    pub.publish(speed)
    rate.sleep()
   
