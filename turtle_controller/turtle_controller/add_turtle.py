#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from my_tasks.msg import Turtleinfo
from my_tasks.msg import AllTurtles
import random
import time

class add_turtles(Node):
    def __init__(self):
        super().__init__("add_turtle_node")
        self.client_ = self.create_client(Spawn,"/spawn")
        while not self.client_.wait_for_service(0.5):
            self.get_logger().warn("waiting for Spawn service")
        self.timer_ = self.create_timer(0.1,self.spawn_turtle)
        self.publisher_ = self.create_publisher(AllTurtles, 'all_turtles', 10)
        self.turtles=[]
        self.count = 1
      
    def spawn_turtle(self):
        request = Spawn.Request()
        random.seed(time.time())
        self.random_x = random.uniform(1.0,10.0)
        self.random_y = random.uniform(1.0,10.0)
        request.x = self.random_x
        request.y = self.random_y
        request.theta = 0.0
        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_turtle_spawn)

    def callback_turtle_spawn(self, future):
        try:
            response = future.result()
            turtle_info = Turtleinfo()
            turtle_info.name = f"turtle_{self.count}"
            turtle_info.x_location = self.random_x
            turtle_info.y_location=self.random_y
            turtle_info.orientation = 0.0

            self.turtles.append(turtle_info)
            all_turtles=AllTurtles()
            all_turtles.turtles = self.turtles
            self.publisher_.publish(all_turtles)


            self.get_logger().info(f"spawning turtle: {self.count}")
            self.count += 1 
        except Exception as e:
            self.get_logger().info(f"service call failed: {e}")        
def main(args=None):
    rclpy.init(args=args)
    node = add_turtles()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()