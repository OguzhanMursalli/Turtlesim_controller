#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    add_turtle_= Node(
        package ="turtle_controller",
        executable ="turtle_add_node",
        name ="turtle_add_node",
    )


    turtlesim_= Node(
        package="turtlesim",
        executable ="turtlesim_node",
        name ="turtlesim",
    )

    return LaunchDescription([
        add_turtle_,
        turtlesim_
    ])
