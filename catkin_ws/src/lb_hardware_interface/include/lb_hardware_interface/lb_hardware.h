#include <ros/ros.h>
// ros_control
#include <controller_manager/controller_manager.h>
#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/joint_state_interface.h>
#include <hardware_interface/robot_hw.h>
#include <realtime_tools/realtime_buffer.h>


#include <joint_limits_interface/joint_limits.h>
#include <joint_limits_interface/joint_limits_interface.h>
#include <boost/scoped_ptr.hpp>




// NaN
#include <limits>

// ostringstream
#include <sstream>


class LegoBoostRobot : public hardware_interface::RobotHW
{
public:
    LegoBoostRobot(ros::NodeHandle& nh);
    ~LegoBoostRobot();
    void init();
    void update(const ros::TimerEvent& e);
    void read();
    void write(ros::Duration elapsed_time);
    
    

    
protected:
  hardware_interface::JointStateInterface jnt_state_interface;
  hardware_interface::VelocityJointInterface jnt_vel_interface_;


  double joint_pos_[2];
  double joint_vel_[2];
  double joint_eff_[2];
  double joint_velocity_cmd[2];


  ros::NodeHandle nh_;
  ros::Timer my_control_loop_;
  ros::Duration elapsed_time_;
  double loop_hz_;
  boost::shared_ptr<controller_manager::ControllerManager> controller_manager_;



};



        // connect and register the joint state interface
        hardware_interface::JointStateHandle state_handle_right("right_wheel_joint", &joint_pos_[0], &joint_vel_[0], &joint_eff_[0]);
        jnt_state_interface.registerHandle(state_handle_right);

        hardware_interface::JointStateHandle state_handle_left("left_wheel_joint", &joint_pos_[1], &joint_vel_[1], &joint_eff_[1]);
        jnt_state_interface.registerHandle(state_handle_left);
        registerInterface(&jnt_state_interface);
        
        hardware_interface::JointHandle vel_handle_right("right_wheel_joint", &joint_velocity_cmd[0]);
        jnt_vel_interface_.registerHandle(vel_handle_right);

        hardware_interface::JointHandle vel_handle_left("left_wheel_joint", &joint_velocity_cmd[1]);
        jnt_vel_interface_.registerHandle(vel_handle_left);


        registerInterface(&jnt_vel_interface_);
