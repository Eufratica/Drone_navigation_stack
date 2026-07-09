#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry

def callback(msg):
    try:
        idx = msg.name.index('husky') # Verifique se o nome é exatamente esse no Gazebo
        pub = rospy.Publisher('/gt/odom', Odometry, queue_size=10)
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = 'odom'
        odom.pose.pose = msg.pose[idx]
        pub.publish(odom)
    except ValueError:
        pass

rospy.init_node('gt_bridge')
rospy.Subscriber('/gazebo/model_states', ModelStates, callback)
rospy.spin()
