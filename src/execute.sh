roslaunch chefbot_bringup robot_standalone.launch && roslaunch robot_pose_ekf robot_pose_ekf.launch && roslaunch chefbot_bringup amcl_demo.launch map_file:=/home/bpn/ex2.yaml && roslaunch chefbot_bringup view_navigation.launch && roslaunch robot_localization ekf_template.launch && rostopic echo /odom && rostopic echo /imu/data


