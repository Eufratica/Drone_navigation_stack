#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, TwistStamped

def callback(msg):
    # Cria a mensagem Stamped exigida pelo MAVROS
    stamped = TwistStamped()
    stamped.header.stamp = rospy.Time.now()
    stamped.header.frame_id = "base_link"
    stamped.twist = msg
    pub.publish(stamped)

if __name__ == '__main__':
    rospy.init_node('cmd_vel_converter', anonymous=True)
    
    # Escuta o Twist puro do move_base
    rospy.Subscriber('/cmd_vel_raw', Twist, callback)
    
    # Publica o TwistStamped exigido pelo MAVROS
    pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
    
    rospy.loginfo("Tradutor Twist -> TwistStamped ativo.")
    rospy.spin()