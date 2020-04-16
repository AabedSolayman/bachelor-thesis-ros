#include <ros/ros.h>
#include <rosgraph_msgs/Clock.h>
#include <lb_hardware_interface/lb_hardware_interface.h>
// ros_control
#include <controller_manager/controller_manager.h>




LegoBoostRobot::LegoBoostRobot(ros::NodeHandle& nh) : nh_(nh) {


  // Declare all JointHandles, JointInterfaces and JointLimitInterfaces of the robot.
  init();

  // Create the controller manager
  controller_manager_.reset(new controller_manager::ControllerManager(this, nh_));

  //Set the frequency of the control loop.
  loop_hz_=10;
  ros::Duration update_freq = ros::Duration(1.0/loop_hz_);

  //Run the control loop
  my_control_loop_ = nh_.createTimer(update_freq, &LegoBoostRobot::update, this);
}

​
LegoBoostRobot::~LegoBoostRobot() {
}

void LegoBoostRobot::init() {


 // Create joint_state_interface for the right and left wheels
  hardware_interface::JointStateHandle state_handle_right("right_wheel_joint", &joint_pos_[0], &joint_vel_[0], &joint_eff_[0]);
  jnt_state_interface.registerHandle(state_handle_right);

  hardware_interface::JointStateHandle state_handle_left("left_wheel_joint", &joint_pos_[1], &joint_vel_[1], &joint_eff_[1]);
  jnt_state_interface.registerHandle(state_handle_left);

 // Create joint velocity interface for the right and left wheels      
  hardware_interface::JointHandle vel_handle_right("right_wheel_joint", &joint_velocity_cmd[0]);
  jnt_vel_interface_.registerHandle(vel_handle_right);
  hardware_interface::JointHandle vel_handle_left("left_wheel_joint", &joint_velocity_cmd[1]);
  jnt_vel_interface_.registerHandle(vel_handle_left);


 // Register all joints interfaces    

  registerInterface(&jnt_state_interface);
  registerInterface(&jnt_vel_interface_);

}


//This is the control loop
void LegoBoostRobot::update(const ros::TimerEvent& e) {
    elapsed_time_ = ros::Duration(e.current_real - e.last_real);
    read();
    controller_manager_->update(ros::Time::now(), elapsed_time_);
    write(elapsed_time_);
}

void LegoBoostRobot::read() {​

  // Write the protocol (I2C/CAN/ros_serial/ros_industrial)used to get the current joint position and/or velocity and/or effort       

  //from robot.
  // and fill JointStateHandle variables joint_position_[i], joint_velocity_[i] and joint_effort_[i]

  read values from rosmsg 


}



void LegoBoostRobot::write(ros::Duration elapsed_time) {
  // Safety
  effortJointSaturationInterface.enforceLimits(elapsed_time);   // enforce limits for JointA and JointB
  positionJointSaturationInterface.enforceLimits(elapsed_time); // enforce limits for JointC

  send velocity and duration to the lego boost

  
  // Write the protocol (I2C/CAN/ros_serial/ros_industrial)used to send the commands to the robot's actuators.
  // the output commands need to send are joint_effort_command_[0] for JointA, joint_effort_command_[1] for JointB and 
  //joint_position_command_ for JointC.

}

int main(int argc, char** argv)
{

    //Initialze the ROS node.
    ros::init(argc, argv, "LegoBoostRobot_hardware_inerface_node");
    ros::NodeHandle nh;
    
    //Separate Sinner thread for the Non-Real time callbacks such as service callbacks to load controllers
    ros::MultiThreadedspinner(2); 
    
    
    // Create the object of the robot hardware_interface class and spin the thread. 
    LegoBoostRobot LegoBoostRobot(nh);
    spinner.spin();
    
    return 0;
}