# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(FATAL_ERROR "Could not find messages which '/home/legoboost/catkin_ws/src/legoboost_roboter/msg/Obstacles.msg' depends on. Did you forget to specify generate_messages(DEPENDENCIES ...)?
Cannot locate message [SegmentObstacle]: unknown package [obstacle_detector] on search path [{'legoboost_roboter': ['/home/legoboost/catkin_ws/src/legoboost_roboter/msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg']}]")
message(STATUS "legoboost_roboter: 3 messages, 0 services")

set(MSG_I_FLAGS "-Ilegoboost_roboter:/home/legoboost/catkin_ws/src/legoboost_roboter/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(legoboost_roboter_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_custom_target(_legoboost_roboter_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "legoboost_roboter" "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" "geometry_msgs/Point:geometry_msgs/Vector3"
)

get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_custom_target(_legoboost_roboter_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "legoboost_roboter" "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" "geometry_msgs/Point"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/legoboost_roboter
)
_generate_msg_cpp(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/legoboost_roboter
)

### Generating Services

### Generating Module File
_generate_module_cpp(legoboost_roboter
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/legoboost_roboter
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(legoboost_roboter_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(legoboost_roboter_generate_messages legoboost_roboter_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_cpp _legoboost_roboter_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_cpp _legoboost_roboter_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(legoboost_roboter_gencpp)
add_dependencies(legoboost_roboter_gencpp legoboost_roboter_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS legoboost_roboter_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/legoboost_roboter
)
_generate_msg_eus(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/legoboost_roboter
)

### Generating Services

### Generating Module File
_generate_module_eus(legoboost_roboter
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/legoboost_roboter
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(legoboost_roboter_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(legoboost_roboter_generate_messages legoboost_roboter_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_eus _legoboost_roboter_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_eus _legoboost_roboter_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(legoboost_roboter_geneus)
add_dependencies(legoboost_roboter_geneus legoboost_roboter_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS legoboost_roboter_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/legoboost_roboter
)
_generate_msg_lisp(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/legoboost_roboter
)

### Generating Services

### Generating Module File
_generate_module_lisp(legoboost_roboter
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/legoboost_roboter
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(legoboost_roboter_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(legoboost_roboter_generate_messages legoboost_roboter_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_lisp _legoboost_roboter_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_lisp _legoboost_roboter_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(legoboost_roboter_genlisp)
add_dependencies(legoboost_roboter_genlisp legoboost_roboter_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS legoboost_roboter_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/legoboost_roboter
)
_generate_msg_nodejs(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/legoboost_roboter
)

### Generating Services

### Generating Module File
_generate_module_nodejs(legoboost_roboter
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/legoboost_roboter
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(legoboost_roboter_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(legoboost_roboter_generate_messages legoboost_roboter_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_nodejs _legoboost_roboter_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_nodejs _legoboost_roboter_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(legoboost_roboter_gennodejs)
add_dependencies(legoboost_roboter_gennodejs legoboost_roboter_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS legoboost_roboter_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter
)
_generate_msg_py(legoboost_roboter
  "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter
)

### Generating Services

### Generating Module File
_generate_module_py(legoboost_roboter
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(legoboost_roboter_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(legoboost_roboter_generate_messages legoboost_roboter_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_py _legoboost_roboter_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/legoboost/catkin_ws/src/legoboost_roboter/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(legoboost_roboter_generate_messages_py _legoboost_roboter_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(legoboost_roboter_genpy)
add_dependencies(legoboost_roboter_genpy legoboost_roboter_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS legoboost_roboter_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/legoboost_roboter)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/legoboost_roboter
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(legoboost_roboter_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(legoboost_roboter_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/legoboost_roboter)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/legoboost_roboter
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(legoboost_roboter_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(legoboost_roboter_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/legoboost_roboter)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/legoboost_roboter
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(legoboost_roboter_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(legoboost_roboter_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/legoboost_roboter)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/legoboost_roboter
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(legoboost_roboter_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(legoboost_roboter_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/legoboost_roboter
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(legoboost_roboter_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(legoboost_roboter_generate_messages_py geometry_msgs_generate_messages_py)
endif()
