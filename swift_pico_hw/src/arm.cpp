#include <chrono>
#include <cstdlib>
#include <memory>

#include "rc_msgs/srv/command_bool.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class Swift_Pico : public rclcpp::Node
{
    public:
        Swift_Pico() : Node("pico_controller") //initializing ros node with name pico_controller
        {
           
            client = this->create_client<rc_msgs::srv::CommandBool>("/drone/cmd/arming");
            while (!client->wait_for_service(1s)) {
                RCLCPP_INFO(this->get_logger(), "Arming service not available, waiting again,,,,");
            }

            auto request = std::make_shared<rc_msgs::srv::CommandBool::Request>();
            request->value = true;

            auto result = client->async_send_request(request);
            /*this->get_node_base_interface() is a method provided by the rclcpp::Node class. 
            It retrieves a pointer to the Node Base Interface, which is one of the internal interfaces that rclcpp::Node implements.
            The Node Base Interface is a foundational interface that provides access to certain core functionalities of the node, 
            such as spinning, managing execution, and interacting with the ROS 2 executor.When you call rclcpp::spin_until_future_complete or similar functions, 
            they require this base interface to operate on the node in a generic way. 
            It's used in contexts where the function doesn't need the full Node object but only the basic functionality provided by this interface.*/
             if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), result) == rclcpp::FutureReturnCode::SUCCESS)
            {
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), result.get()->data.c_str());
            }         
        }

    private:
        
        rclcpp::Client<rc_msgs::srv::CommandBool>::SharedPtr client;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Swift_Pico>());
    rclcpp::shutdown();
    return 0;
}


