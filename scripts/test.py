#!/usr/bin/env python3

import rospy
import sys
from interbotix_xs_modules.locobot import InterbotixLocobotXS

class Test():
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):

        # Initialize node
        rospy.init_node("motors")
        self.bot = InterbotixLocobotXS("locobot_wx250s", arm_model="mobile_wx250s", init_node=False)
        self.loop_rate = rospy.Rate(100)
        rospy.logwarn('XXX Started')
        self.start()


    def pickup(self):
        # pick up each object from left-to-right and drop it in a virtual basket on the left side of the robot
        x = 0.5
        y = 0.5
        z = 0.1
        self.bot.arm.set_ee_pose_components(x=x, y=y+0.01, z=z+0.05, pitch=0.5)
        self.bot.arm.set_ee_pose_components(x=x, y=y+0.01, z=z-0.02, pitch=0.5)
        self.bot.gripper.close()
        self.bot.arm.set_ee_pose_components(x=x, y=y, z=z+0.05, pitch=0.5)
        self.bot.arm.set_ee_pose_components(y=0.3, z=0.2)
        self.bot.gripper.open()
        self.bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        self.bot.arm.go_to_sleep_pose()


    def start(self):
        while not rospy.is_shutdown():
            self.bot.camera.pan_tilt_move(0, 0.75)
            self.pickup()
            self.loop_rate.sleep()


def main(args):   
    try:
        Test()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down motor node.")

if __name__ == '__main__':
    main(sys.argv)                      