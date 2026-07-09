#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry

pub = None

def callback(data):
    global pub
    try:
        idx = -1
        for i, name in enumerate(data.name):
            if 'husky' in name.lower() or 'robot' in name.lower():
                idx = i
                break
        
        if idx != -1:
            odom = Odometry()
            odom.header.stamp = rospy.Time.now()
            odom.header.frame_id = "odom"
            odom.child_frame_id = "base_link"
            
            odom.pose.pose = data.pose[idx]
            odom.twist.twist = data.twist[idx]
            
            pub.publish(odom)
    except Exception as e:
        pass

if __name__ == '__main__':
    rospy.init_node('ponte_gazebo_to_gt')
    pub = rospy.Publisher('/gt/odom', Odometry, queue_size=10)
    rospy.Subscriber('/gazebo/model_states', ModelStates, callback)
    rospy.loginfo("Ponte ativada! /gt/odom reestabelecido com sucesso.")
    rospy.spin()
