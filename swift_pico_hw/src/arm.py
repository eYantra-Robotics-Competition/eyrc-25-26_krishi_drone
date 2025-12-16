#!/usr/bin/env python3

from rc_msgs.srv import CommandBool
import rclpy
from rclpy.node import Node

class Swift_Pico(Node):
	
    def __init__(self):
        super().__init__('pico_controller')  # initializing ros node with name pico_controller
        self.cli = self.create_client(CommandBool, "/drone/cmd/arming")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Arming service not available, waiting again,,,,')
        self.req = CommandBool.Request()

        future = self.send_request() # ARMING THE DRONE
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info(response.data)

    def send_request(self):
        self.req.value = True
        return self.cli.call_async(self.req)
    

def main(args=None):
	rclpy.init(args=args)
	swift_pico = Swift_Pico()

	try:
		rclpy.spin(swift_pico)
	except KeyboardInterrupt:
		swift_pico.get_logger().info('KeyboardInterrupt, shutting down.\n')
	finally:
		swift_pico.destroy_node()
		rclpy.shutdown()

if __name__ == '__main__':
	main()