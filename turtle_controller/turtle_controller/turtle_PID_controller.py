#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn , Kill
from geometry_msgs.msg import Twist
from simple_pid import PID
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
        self.kill_cli = self.create_client(Kill,"/kill")
        while not self.kill_cli.wait_for_service(0.5):
            pass
        
        self.pid = PID(4.0,0.1,0.1,setpoint = 0)
        self.pid.output_limits = (-1.0, 1.0)

        self.pid_len = PID(2,0.1,0.01,setpoint = 180)
        self.pid_len.output_limits = (-1.0, 1.0)
        
        self.spawn_turtle()
       
        
    def kill_turtle(self,turtle_name):
        request_ = Kill.Request()
        request_.name = turtle_name
        future_ = self.kill_cli.call_async(request_)
        future_.add_done_callback(self.callback_turtle_kill)

    def callback_turtle_kill(self, future_):
        try:
            response = future_.result()
            self.get_logger().info("the turtle has been kill.")
            self.spawn_turtle()
        except Exception as e:
            self.get_logger().info(f"service call failed: {e}")


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
        dx = pose.x - self.turtle1_pose_x 
        dy = pose.y - self.turtle1_pose_y 

        hipo = math.sqrt(dx**2 + dy**2)
        target_theta = math.atan2(dy,dx)
        err_theta = target_theta - self.turtle1_pose_theta 

        while err_theta > math.pi:
            err_theta -= 2 * math.pi
        while err_theta < -math.pi:
            err_theta += 2 * math.pi

        self.get_logger().info(f"FARK:{err_theta}")


        if abs(err_theta)>=0.01:
            if err_theta < 0:
                self.pid.setpoint = -180
            else:
                self.pid.setpoint = 180

            angular_ = self.pid(err_theta)
        else:
            self.get_logger().info(f"rotation has been successful")     
            angular_ = 0.0
        if angular_ != 0.0:
            self.tw_loop(angular_)

        if angular_ == 0.0:
            if hipo> 0.1:
                linear_x = self.pid_len(hipo)
            else:
                self.kill_turtle("turtle2")
                linear_x= 0.0
                angular_ = 0.0
                hipo = 0
            if linear_x != 0.0:
                self.deneme_lin(linear_x)

    def tw_loop(self,angular_):
        msg_ = Twist()
        msg_.angular.z = angular_
        self.pub_.publish(msg_)


    def deneme_lin(self,linear_x):
        msg = Twist()
        msg.linear.x = linear_x
        self.pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = turtle_pid()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()