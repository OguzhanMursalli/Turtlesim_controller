#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class rob_controller(Node):
    def __init__(self):
        super().__init__("turtle_node")
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer_=self.create_timer(1,self.timer_callback)
        self.get_logger().info("turtle_node has been started.")
        self.counter_ = 0
    def timer_callback(self):
        self.counter_ +=1
        msg= Twist()
        if self.counter_ == 1:
            msg.linear.x = float(input("x deger: "))
            self.cmd_vel_pub_.publish(msg)
        elif self.counter_ ==2:
            msg.linear.y = float(input("y deger: "))
            self.cmd_vel_pub_.publish(msg)
        else:
            self.counter_ = 0
def main(args=None):
    rclpy.init(args=args)
    node = rob_controller()
    rclpy.spin(node)
    rclpy.shutdown()