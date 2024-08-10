#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    move_turtle_= Node(
        package ="turtle_controller",
        executable ="turtle1_controller",
        name ="turtle1_controller",
        output ="screen",
    )

    turtlesim_= Node(
        package="turtlesim",
        executable ="turtlesim_node",
        name ="turtlesim",
    )

    return LaunchDescription([
        turtlesim_,
        move_turtle_,
    ])
