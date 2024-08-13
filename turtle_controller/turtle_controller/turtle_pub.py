#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from my_tasks.srv import TurtleMove


class rob_controller(Node):
    def __init__(self):
        super().__init__("turtle_node")
        self.srv=self.create_service(TurtleMove,"turtle_Move",self.srv_callback)
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.get_logger().info("turtle_node has been started.")
        self.counter_ = 0


    def srv_callback(self,request,response):       
        self.counter_ = 0
        self.linear_x = request.x
        self.linear_y = request.y
        self.timer = self.create_timer(1.0,self.timer_callback)
        response.success = True
        return response

    def timer_callback(self):
        msg = Twist()
        if self.counter_ == 0:
            msg.linear.x = self.linear_x
            self.cmd_vel_pub_.publish(msg)
            self.counter_= 1

        elif self.counter_ == 1:
            msg.linear.y = self.linear_y
            self.cmd_vel_pub_.publish(msg)
            self.counter_ = 2
            
        elif self.counter_ == 2:
            self.timer.cancel()
            self.timer = None
            self.counter_ = 0
            self.get_logger().info("Movement completed.")

def main(args=None):
    rclpy.init(args=args)
    node = rob_controller()
    rclpy.spin(node)
    rclpy.shutdown()