#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    turtle_pid_rotat= Node(
        package ="turtle_controller",
        executable ="turtle_PID",
        name ="turtle_PID_controller",
    )


    turtlesim_= Node(
        package="turtlesim",
        executable ="turtlesim_node",
        name ="turtlesim",
    )

    return LaunchDescription([
        turtle_pid_rotat,
        turtlesim_
    ])
