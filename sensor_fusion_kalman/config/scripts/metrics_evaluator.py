#!/usr/bin/env python3
import rospy
import message_filters
import math
import numpy as np
import matplotlib.pyplot as plt
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped # Ajuste caso necessário
from tf.transformations import euler_from_quaternion

class MetricsEvaluator:
    def __init__(self):
        rospy.init_node('metrics_evaluator', anonymous=True)
        
        self.gt_x, self.gt_y = [], []
        self.est_x, self.est_y = [], []
        self.errors_pos = []
        
        # Assina o tópico do seu Husky e o tópico de Ground Truth (se houver)
        # Se você ainda não tem o /gt/odom, lembre-se de criar o relay
        sub_filtered = message_filters.Subscriber('/odometry/filtered', Odometry)
        sub_gt = message_filters.Subscriber('/gt/odom', Odometry) 
        
        self.ts = message_filters.ApproximateTimeSynchronizer([sub_filtered, sub_gt], queue_size=10, slop=0.1)
        self.ts.registerCallback(self.sync_callback)
        
        rospy.on_shutdown(self.save_results)
        rospy.loginfo("Calculadora de métricas pronta!")

    def sync_callback(self, msg_filt, msg_gt):
        x_est, y_est = msg_filt.pose.pose.position.x, msg_filt.pose.pose.position.y
        x_gt, y_gt = msg_gt.pose.pose.position.x, msg_gt.pose.pose.position.y
        
        error_pos = math.sqrt((x_gt - x_est)**2 + (y_gt - y_est)**2)
        
        self.gt_x.append(x_gt)
        self.gt_y.append(y_gt)
        self.est_x.append(x_est)
        self.est_y.append(y_est)
        self.errors_pos.append(error_pos)

    def save_results(self):
        if not self.errors_pos: return
        rmse = np.sqrt(np.mean(np.square(self.errors_pos)))
        print(f"\nRMSE Final: {rmse:.4f} metros")
        
        plt.figure()
        plt.plot(self.gt_x, self.gt_y, label='Real (Ground Truth)')
        plt.plot(self.est_x, self.est_y, label='Filtro de Kalman')
        plt.legend()
        plt.savefig('resultado_trajetoria.png')
        print("Gráfico salvo como resultado_trajetoria.png")

if __name__ == '__main__':
    MetricsEvaluator()
    rospy.spin()
