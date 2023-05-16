


import rospy
from geometry_msgs.msg import Twist

class DriveForwardNode(object):
    def __init__(self):
        rospy.init_node('drive_forward')
        self.pub = rospy.Publisher('/locobot/mobile_base/commands/velocity', Twist, queue_size=1)
        self.twist = Twist()
        self.twist.linear.x = 1.0
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0

        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.5
        self.twist.angular.z = 0.0
        self.rate = rospy.Rate(100) #publishin rate 

    def run(self):
        while not rospy.is_shutdown():
            topic1_msg = self.twist
            rospy.loginfo('Publishing command: {}'.format(topic1_msg))
            self.pub.publish(topic1_msg)
             # Sleep to maintain the publishing rate
            self.rate.sleep()

if __name__ == '__main__':
    node = DriveForwardNode()
    node.run()
