#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class InfectedPlantsPublisher(Node):
    def __init__(self):
        super().__init__('infected_plants_publisher')

        # Create publisher
        self.publisher_ = self.create_publisher(String, '/detected_plants', 10)


        self.infected_plants = []

    def publish_data(self):
        msg = String()
        msg.data = json.dumps(self.infected_plants)  # Convert list to string
        self.publisher_.publish(msg)

        self.get_logger().info(f'Published: {self.infected_plants}')


def main(args=None):
    rclpy.init(args=args)
    node = InfectedPlantsPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
