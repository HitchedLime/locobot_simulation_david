import rospy
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
import sys


def  teleport_location(x,y,z):
    
    rospy.init_node('set_model_state')
    rospy.wait_for_service('/gazebo/set_model_state')
    set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    model_state = ModelState()
    model_state.model_name = 'locobot'
    model_state.pose.position.x = x
    model_state.pose.position.y = y
    model_state.pose.position.z = z

    set_model_state(model_state)

if __name__ == "__main__":
    teleport_location(0,0,0)