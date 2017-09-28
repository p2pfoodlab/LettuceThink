cmake_minimum_required(VERSION 2.8.3)
project(p2p)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
  sensor_msgs
  actionlib_msgs
  camera_info_manager
  OpenCV
  cv_bridge
  ${MESSAGE_DEPENDENCIES}
)

add_message_files(
  FILES
  Posi.msg
)

add_action_files(
  DIRECTORY action
  FILES goto.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
  actionlib_msgs
  ${MESSAGE_DEPENDENCIES}
)

catkin_package(
  CATKIN_DEPENDS actionlib_msgs message_runtime ${MESSAGE_DEPENDENCIES}
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)





