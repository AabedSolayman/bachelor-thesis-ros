#include "ros/ros.h"
#include <tf2/LinearMath/Quaternion.h>
#include "obstacle_detector/Obstacles.h"
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/Point.h"
#include "math.h"

class PoseFinder {

private:
	geometry_msgs::Point pointTop;
	geometry_msgs::Point pointBottom;
	geometry_msgs::Pose robotPose_;
	double yawRad = 0;
	tf2::Quaternion robotOrientation;
	ros::Publisher posePublisher;
	ros::Subscriber subTop;
	ros::Subscriber sub_bottom;
	ros::NodeHandle n;

public:
	PoseFinder() {

		subTop = n.subscribe("/lidar_top/raw_obstacles", 1000,
				&PoseFinder::obstaclesTopCallback, this);

		sub_bottom = n.subscribe("/lidar_bottom/raw_obstacles", 1000,
				&PoseFinder::obstaclesTopCallback, this);

		posePublisher = n.advertise<geometry_msgs::Pose>("robot_pose", 1000);

		ros::spin();

	}

	void obstaclesTopCallback(
			const obstacle_detector::Obstacles::ConstPtr &msg) {
		pointTop = msg->circles[0].center;

	}

	void obstaclesBottomCallback(
			const obstacle_detector::Obstacles::ConstPtr &msg) {
		pointBottom = msg->circles[0].center;
	}

	void robotPosePublisher() {
		while (ros::ok()) {
			posePublisher.publish(robotPose());
			ros::spinOnce();
			ros::Rate loop_rate(10);
			loop_rate.sleep();

		}
	}

	geometry_msgs::Pose robotPose() {
		robotPose_.position.x = (pointTop.x - pointBottom.x) / 2;
		robotPose_.position.y = (pointTop.y - pointBottom.y) / 2;

		yawRad = atan2(robotPose_.position.y, robotPose_.position.x);

		robotOrientation.setRPY(0, 0, yawRad);

		robotPose_.orientation = robotOrientation;

		return robotPose_;
	}

};

int main(int argc, char **argv) {

	ros::init(argc, argv, "pose_detector");

	PoseFinder pF;

	return 0;
}
