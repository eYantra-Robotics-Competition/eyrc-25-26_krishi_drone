cmake_minimum_required(VERSION 3.8)
project(swift_pico_hw)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rc_msgs REQUIRED)
find_package(pid_msg REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)
find_package(OpenCV REQUIRED)


#add executables
add_executable(arm_cpp src/arm.cpp)
add_executable(pico_controller_cpp src/pico_controller.cpp)

#add dependencies
ament_target_dependencies(arm_cpp rclcpp rc_msgs)
ament_target_dependencies(pico_controller_cpp rclcpp rc_msgs pid_msg geometry_msgs)

# Install executables
install(
  TARGETS 
  arm_cpp 
  pico_controller_cpp
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

#Install scripts
install(PROGRAMS
  src/pico_controller.py
  src/arm.py
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
