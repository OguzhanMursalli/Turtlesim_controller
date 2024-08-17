#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn 
from geometry_msgs.msg import Twist
import random
import time
import math 

class turtle_pid(Node):
    def __init__(self):
        super().__init__("TurtlePID")

        self.sub_1 = self.create_subscription(Pose,"/turtle1/pose",self.turtle1_callback,10)
        self.sub_2 = self.create_subscription(Pose,"/turtle2/pose",self.turtle2_callback,10)
        self.pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.client_ = self.create_client(Spawn,"/spawn")
        while not self.client_.wait_for_service(0.5):
            self.get_logger().warn("waiting for Spawn service")
        self.spawn_turtle()
       
        
        

    def spawn_turtle(self):
        request = Spawn.Request()
        random.seed(time.time())
        self.random_x = random.uniform(1.0,10.0)
        self.random_y = random.uniform(1.0,10.0)
        self.random_t = 0.0
        request.x = self.random_x
        request.y = self.random_y
        request.theta = self.random_t 
        request.name = "turtle2"
        self.get_logger().info(f"Spawning turtle at x: {self.random_x}, y: {self.random_y}, theta: {self.random_t}")
    
        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_turtle_spawn)

    def callback_turtle_spawn(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"spawning turtle")
        except Exception as e:
            self.get_logger().info(f"service call failed: {e}")        
     
        
    def turtle1_callback(self,pose: Pose):
        
        self.turtle1_pose_x = pose.x
        self.turtle1_pose_y = pose.y
        self.turtle1_pose_theta = pose.theta 
       
        
    def turtle2_callback(self,pose:Pose):
        integral_theta = 0.0
        before_err_theta = 0.0
        dx = pose.x - self.turtle1_pose_x 
        dy = pose.y - self.turtle1_pose_y 
        target_theta = math.atan2(dy,dx)
        err_theta = target_theta - self.turtle1_pose_theta
        
        while err_theta > math.pi:
            err_theta -= 2 * math.pi
        while err_theta < -math.pi:
            err_theta += 2 * math.pi
        self.get_logger().info(f"FARK:{err_theta}")
        Kp_theta = 1
        Ki_theta = 0.1
        Kd_theta = 0.01
        integral_theta += err_theta
        derivate_theta = err_theta - before_err_theta

        if abs(err_theta)>=0.01:
            angular_ = Kp_theta*err_theta + Ki_theta*integral_theta + Kd_theta*derivate_theta
            before_err_theta = err_theta
        else:
            self.get_logger().info(f"rotation has been successful")
            angular_ = 0.0
        self.tw_loop(angular_)

    def tw_loop(self,angular_):
        msg_ = Twist()
        msg_.angular.z = angular_
        self.pub_.publish(msg_)

def main(args=None):
    rclpy.init(args=args)
    node = turtle_pid()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()