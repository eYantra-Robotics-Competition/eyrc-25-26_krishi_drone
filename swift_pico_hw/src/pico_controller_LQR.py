#!/usr/bin/env python3

'''
This python file runs a ROS 2-node of name pico_control which holds the position of Swift Pico Drone on the given drone.
This node publishes and subsribes the following topics:

		PUBLICATIONS			SUBSCRIPTIONS
		/drone_command			/whycon/poses
		/position_error

Rather than using different variables, use list. eg : self.setpoint = [1,2,3], where index corresponds to x,y,z ...rather than defining self.x_setpoint = 1, self.y_setpoint = 2
CODE MODULARITY AND TECHNIQUES MENTIONED LIKE THIS WILL HELP YOU GAINING MORE MARKS WHILE CODE EVALUATION.	
'''

# Import Necessary Libraries for LQR
##############################################




##############################################
import math
from rc_msgs.msg import RCMessage
from rc_msgs.srv import CommandBool
from geometry_msgs.msg import PoseArray
from error_msg.msg import Error

import rclpy
from rclpy.node import Node

MIN_ROLL = 1000
BASE_ROLL = 1500
MAX_ROLL = 2000
SUM_ERROR_ROLL_LIMIT = 5000

MIN_PITCH = 1000
BASE_PITCH = 1500
MAX_PITCH = 2000
SUM_ERROR_PITCH_LIMIT = 5000

MIN_THROTTLE = 1250
BASE_THROTTLE = 1500   # 4.3
MAX_THROTTLE = 2000
SUM_ERROR_THROTTLE_LIMIT = 5000


class Swift_Pico(Node):
	def __init__(self):
		super().__init__('pico_controller')  # initializing ros node with name pico_controller

		self.m = 0.152  # Quadcopter mass (kg)
		self.g = 9.81 # Gravity (m/s^2)
  
  
  

  
		# Desired state [x, y, z, x_dot, y_dot, z_dot]
		# These Points are in meters and meters/second
		# and [-0.7, 0.0, 2.7, 0.0, 0.0, 0.0] corresponds to Whycon coordinates [x= -7, y= 0, z= 27]
  		self.desired_state = [-0.7, 0.0, 2.7, 0.0, 0.0, 0.0]   # Target state vector



		# Current state [x ,y ,z ,x_dot ,y_dot ,z_dot]
		#  whycon marker at the position of the drone given in the scene. Make the whycon marker associated with position_to_hold drone renderable and make changes accordingly
		self.current_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]              # Current position [x ,y ,z ,x_dot ,y_dot ,z_dot]


  
  
  
  
  
  
  
  
		##############################################################################################
		# Derive the system dynamics matrices A and B 
		# Define the A matrix and B matrix for the state-space representation of the quadcopter
		
		
		
		self.A =  # Define the A matrix
		
			

		self.B =  # Define the B matrix
		
		
		
		#####################################################################################################
		# Understand the the state vector and input vector
		# State vector: [x, y, z, x_dot, y_dot, z_dot] (Q matrix corresponds to these states)
		# Input vector: [roll, pitch, throttle]  (R matrix corresponds to these inputs)
		
		# Define the Q and R matrices for the LQR controller
		# Q matrix penalizes deviations from the desired state
		# R matrix penalizes control effor
		
		
		# The Q and R matrices for LQR are defined to balance state error and control effort
		# These Matrices are Diagonal Matrices
		# You need to tune the values in these matrices to get the desired performance
		
		
		self.Q =           #  Define the Q matrix
		
		self.R =           # Define the R matrix
		
		


		#####################################################################################################
		
		
		# Compute the LQR gain matrix K using the necessary library (explore the necessary library for this e.g: control etc.)
		
		# K matrix Gain is computed using the LQR method using the A, B, Q, R matrices defined above
		
		#Compute LQR gains 
		self.K =           # Calculate the LQR gain matrix K
		




		# Declaring a cmd of message type swift_msgs and initializing values
		self.cmd = RCMessage()
		self.cmd.rc_roll = 1500
		self.cmd.rc_pitch = 1500
		self.cmd.rc_yaw = 1500
		self.cmd.rc_throttle = 1400













		# Hint : Add variables for storing previous errors in each axis, like self.prev_error = [0,0,0] where corresponds to [pitch, roll, throttle]		#		 Add variables for limiting the values like self.max_values = [2000,2000,2000] corresponding to [roll, pitch, throttle]
		# self.min_values = [1000,1000,1000] corresponding to [pitch, roll, throttle]
		# You can change the upper limit and lower limit accordingly. 
		#----------------------------------------------------------------------------------------------------------


		#------------------------Add other ROS 2 Publishers here-----------------------------------------------------
  
  
		# # This is the sample time in which you need to run pid. Choose any time which you seem fit.
	
		self.sample_time = 0.01666  # in seconds
	
 
 
		# ===============================
		#  Publishers and Subscribers
		# ===============================
		# Publishing /drone_command, /position_error
		self.command_pub = self.create_publisher(RCMessage, '/drone_command', 10)
		self.pos_error_pub = self.create_publisher(Error, '/pos_error', 10)


		# Subscribing to /whycon/poses
		self.create_subscription(PoseArray, '/whycon/poses', self.whycon_callback, 1)
	
		self.arm()  # ARMING THE DRONE
  


		# Creating a timer to run the pid function periodically, refer ROS 2 tutorials on how to create a publisher subscriber(Python)





	def disarm(self):
		self.cmd.rc_roll = 1000
		self.cmd.rc_yaw = 1000
		self.cmd.rc_pitch = 1000
		self.cmd.rc_throttle = 1000
		self.cmd.rc_aux4 = 1000
		self.command_pub.publish(self.cmd)
		

	def arm(self):
		self.disarm()
		self.cmd.rc_roll = 1500
		self.cmd.rc_yaw = 1500
		self.cmd.rc_pitch = 1500
		self.cmd.rc_throttle = 1500
		self.cmd.rc_aux4 = 2000
		self.command_pub.publish(self.cmd)  # Publishing /drone_command


	# Whycon callback function
	# The function gets executed each time when /whycon node publishes /whycon/poses 
	def whycon_callback(self, msg):
		
  		self.current_state[0] = (msg.poses[0].position.x / 10)  # x position in meters
		#--------------------Set the remaining co-ordinates of the drone from msg----------------------------------------------

		# Calculate velocities (x_dot, y_dot, z_dot) from the position data
		# Hint : You can use the previous position and current position to calculate velocity
		# Velocity = (Current Position - Previous Position) / Sample Time
  
  
		# After the calculation of the velocities update them into the self.current_state variable accordingly
		# self.current_state[3] = x_dot
		# self.current_state[4] = y_dot
		# self.current_state[5] = z_dot

	
		#---------------------------------------------------------------------------------------------------------------


		# Hint : You can define a function for filtering the whycon data if you feel the need for it


	# This function maps angles to the RC controlller stick range
	def linear_map(self,x):
		y = ((1000/math.pi) * x) + 1500
		return y
	

	# This function maps the thrust force to the RC controller stick range
	def force_to_throttle_linear(self, thrust_force):
		hover_thrust = self.m * self.g 
		total_thrust = hover_thrust + thrust_force  
		max_thrust = 2.0 * hover_thrust 
		slope = (MAX_THROTTLE - BASE_THROTTLE) / (max_thrust - hover_thrust)
		throttle = BASE_THROTTLE + slope * (total_thrust - hover_thrust)
		return int(np.clip(throttle, MIN_THROTTLE, MAX_THROTTLE))






	def controller(self):
		# ===============================
		# 1. Compute State Error
		# =============================== 

		error = self.current_state - self.desired_state







		# ===============================
		# 2. Compute Control Input
		# ===============================

		# The U matrix is the control input matrix for the LQR controller
		# It is computed as the product of the state error and the LQR gain matrix K (u = -K * error)
  		
		u =               # Control input from LQR  (Explore How the Matrix Multiplication is done in the necessary library you are using)

		
		
  
  
  
  
  
  
  
  
  
  
  
		# The Clampped values of roll, pitch and throttle are then mapped to the RC controller stick range using the linear_map and force_to_throttle_linear functions defined above
		roll  = np.clip(-u[0], -math.pi/12, math.pi/12)
		pitch = np.clip(u[1], -math.pi/12, math.pi/12)
		

		self.cmd.rc_roll = int(self.linear_map(roll))
		self.cmd.rc_pitch = int(self.linear_map(pitch))
		self.cmd.rc_throttle = int(self.force_to_throttle_linear(-u[2]))





		# ===============================
		# Publish LQR error
		# ===============================

		# Publish LQR error
		pos_error = Error()
		pos_error.pitch_error = error[0]
  
		#------------------------------------------------------------------------------------------------------------------------
		# fill in the remaining error values for roll and throttle







		#------------------------------------------------------------------------------------------------------------------------
		self.command_pub.publish(self.cmd)
		# calculate throttle error, pitch error and roll error, then publish it accordingly
		self.pos_error_pub.publish(pos_error)



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
